import json

from django.test import TestCase

from .models import Usuario

from django.core.management import call_command

from .models import Nave

class UsuarioAPITest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre="Dani",
            apellidos="Prueba",
            cocinero=True
        )

    def test_listar_usuarios(self):
        respuesta = self.client.get("/api/usuarios/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)
        self.assertEqual(respuesta.json()[0]["nombre"], "Dani")

    def test_consultar_usuario(self):
        respuesta = self.client.get(
            f"/api/usuarios/{self.usuario.id}/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["nombre"], "Dani")

    def test_consultar_usuario_inexistente(self):
        respuesta = self.client.get("/api/usuarios/9999/")

        self.assertEqual(respuesta.status_code, 404)

    def test_crear_usuario(self):
        datos = {
            "nombre": "Juanma",
            "apellidos": "Prueba",
            "mantenimiento": True
        }

        respuesta = self.client.post(
            "/api/usuarios/crear/",
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 201)
        self.assertTrue(Usuario.objects.filter(nombre="Juanma").exists())

    def test_crear_usuario_sin_nombre(self):
        datos = {"apellidos": "Prueba"}

        respuesta = self.client.post(
            "/api/usuarios/crear/",
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)

    def test_modificar_usuario(self):
        datos = {"cocinero": False, "mantenimiento": True}

        respuesta = self.client.patch(
            f"/api/usuarios/{self.usuario.id}/modificar/",
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.usuario.refresh_from_db()

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(self.usuario.cocinero)
        self.assertTrue(self.usuario.mantenimiento)

    def test_eliminar_usuario(self):
        respuesta = self.client.delete(
            f"/api/usuarios/{self.usuario.id}/eliminar/"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(
            Usuario.objects.filter(id=self.usuario.id).exists()
        )


class FactoriaTest(TestCase):

    def test_factoria_crea_usuarios_y_naves(self):
        call_command("factoria")

        self.assertEqual(Usuario.objects.count(), 20)
        self.assertEqual(Nave.objects.count(), 3)

        tamanos = set(Nave.objects.values_list("tamano", flat=True))
        self.assertEqual(
            tamanos,
            {"PEQUENA", "MEDIANA", "GRANDE"}
        )

