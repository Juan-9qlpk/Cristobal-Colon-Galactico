import json

from django.test import TestCase
from django.db.models import ProtectedError
from .models import Usuario, Nave, Mision, Tripulacion, Exoplaneta, Rol

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



## supongo que creare mi propia clase para la parte de test de misiones?
class MisionTest(TestCase):

    def setUp(self):
        ## datos de cacharreo con libre eleccion jajajaja
        self.nave = Nave.objects.create(nombre="Islote", tamano="PEQUENA")
        self.otra_nave = Nave.objects.create(nombre="Isla", tamano="PEQUENA")

        self.capitan = Usuario.objects.create(nombre="Cristobal", apellidos="Colon")
        self.tripulante1 = Usuario.objects.create(nombre="YASUO ARE U TURK", apellidos="TURK?")
        self.tripulante2 = Usuario.objects.create(nombre="Manager", apellidos="Fiestero Ptro")
        self.tripulante3 = Usuario.objects.create(nombre="Franchescooooooo", apellidos="FIAUUUUUUM")
        self.extra = Usuario.objects.create(nombre="Parpaapap", apellidos="parapapa")

        self.datos_mision = {
            "nombre": "BIENVENIDO A LA ISLA",
            "nave": self.nave.id,
            "capitanes": [self.capitan.id],
            "tripulantes": [self.tripulante1.id, self.tripulante2.id, self.tripulante3.id],
        }

    def test_crear_mision(self):
        mision = Mision.objects.create(nombre="Explorasao", nave=self.nave)

        self.assertFalse(mision.finalizada)
        self.assertIsNone(mision.exito)
        ## creo mision alo bruto compruebo que se inicia como no finalizada es decir en false
        ## y que exito e snull

    def test_no_se_puede_borrar_nave_con_misiones(self):
        Mision.objects.create(nombre="Explorasao", nave=self.nave)

        with self.assertRaises(ProtectedError): ## copiado de la parte de jugadores en lso apuntes
            self.nave.delete() ## No se puede borrar una nave que tenga misiones lanza la excepcion de arriba

    def test_asignar_mision(self):
        respuesta = self.client.post("/api/misiones/asignar/",
            data=self.datos_mision,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Mision.objects.count(), 1)
        self.assertEqual(Tripulacion.objects.count(), 4)
        ## si sale 1 objeto de mision y 4 tripulantes funca todo ya que se cumplen los
        ## req para una mision

    def test_navent(self):
        datos = {
            "nombre": "Naven't?",
            "capitanes": [self.capitan.id],
            "tripulantes": [self.tripulante1.id, self.tripulante2.id, self.tripulante3.id],
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)
        ## no se cumplen los requisitos de la nave ya que no se asignan todos los datos necesarios

    def test_muchas_personas(self):
        datos = {
            "nombre": "India",
            "nave": self.nave.id,
            "capitanes": [self.capitan.id],
            "tripulantes": [self.tripulante1.id, self.tripulante2.id,
                            self.tripulante3.id, self.extra.id],
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)
        ## falla porque asignamos mas tripualntes de la cuenta como dijimos que el capi contaba como tripulacion
        ## y la nave es peqeuna falla

    def test_meter_capitanes(self):
        datos = {
            "nombre": "CAPI",
            "nave": self.nave.id,
            "capitanes": [self.capitan.id, self.tripulante1.id],
            "tripulantes": [self.tripulante2.id, self.tripulante3.id],
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 0)
        ## falla al meter 2 capis en una nave pequeña solo la nave grand epuede tener 2

    def test_mision_usuario(self):
        self.client.post("/api/misiones/asignar/",
            data=self.datos_mision,
            content_type="application/json")

        datos = {
            "nombre": "RECONQUISTEN LA ISLA",
            "nave": self.otra_nave.id,
            "capitanes": [self.capitan.id],
            "tripulantes": [self.tripulante1.id, self.tripulante2.id, self.tripulante3.id],
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Mision.objects.count(), 1)
        ## se asigna la mision al usuario ocmo cumple todos los campos no hay ningun problema y
        ## sale hacia delante despues intenta reasignar otra mision a un usuario que ya la tiene asignada
        ## corrceto tira error revienta

    def test_finalizar_y_guardar(self):
        mision = Mision.objects.create(nombre="ISLITAAA", nave=self.nave)
        datos = {"exito": True, "exoplanetas": ["Turk alert", "Isla premium"]}

        respuesta = self.client.post("/api/misiones/" + str(mision.id) + "/finalizar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 200)
        mision = Mision.objects.get(id=mision.id)
        self.assertTrue(mision.finalizada)
        self.assertTrue(mision.exito)
        self.assertEqual(mision.exoplanetas.count(), 2)
        ## creo una mision y exoplanetas
        ## compruebo si esta finalizada y ha tenido exito la mision
        ## y si hay 2 exoplanetas si la mision esta finalzada con exito
        ## tras la peticion y tiene los exoplanetas sale tgodo correcto

    def test_guardar_planetoides(self):
        mision = Mision.objects.create(nombre="ISLITAAA", nave=self.nave)
        datos = {"exito": False, "exoplanetas": ["Turk alert"]}

        respuesta = self.client.post("/api/misiones/" + str(mision.id) + "/finalizar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 400)
        mision = Mision.objects.get(id=mision.id)
        self.assertFalse(mision.finalizada)
        ## crea una mision e intenta finalizarla,
        ## da 400 porque solo se guardan planetas si la mision tiene exito
        ## y la mision sigue sin finalizar porque la peticion ha fallado

    def test_no_finalizar_dos_veces(self):
        mision = Mision.objects.create(nombre="RE RECONQUISTAR LA ISLA", nave=self.nave, finalizada=True, exito=True)

        respuesta = self.client.post("/api/misiones/" + str(mision.id) + "/finalizar/",
            data={"exito": False},
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)
        mision = Mision.objects.get(id=mision.id)
        self.assertTrue(mision.exito)
        ## peticion para finalizar una mision finalizada la creo desde inicio como finalizada kek
        ## en la peticion tirara un error ya que no sse puede finalizar una mision finalizada
        ## el status code 400 lo he copiado de los apuntes imo era 404 ya que no deberia
        ## de encontrarlo y sale ese error pero ta bien lo dejo asi ua que si lo encuentra
        ## lo que pasa es que da error al finalizar

    def test_preguntar_tripulacion(self):
        mision = Mision.objects.create(nombre="TRABAJADORES ISLA", nave=self.nave)
        Tripulacion.objects.create(mision=mision, usuario=self.capitan, rol=Rol.CAPITAN)
        Tripulacion.objects.create(mision=mision, usuario=self.tripulante1, rol=Rol.TRIPULANTE)

        respuesta = self.client.get("/api/misiones/" + str(mision.id) + "/tripulacion/")

        self.assertEqual(respuesta.status_code, 200)
        tripulacion = respuesta.json()["datos"]["tripulacion"]
        self.assertEqual(len(tripulacion), 2)
        self.assertEqual(tripulacion[0]["nombre"], "Cristobal")
        self.assertEqual(tripulacion[0]["rol"], Rol.CAPITAN)
        ## creo mision y meto a la tripulacion ajaj no meto todos me salto mis propios requisitos
        ## y consulto la tripulacion en la peiticon
        ## el array que me devuelve debe tener 2 de longitud por los datos que he metido
        ## 1 capi y un 1 tripulacion simplemente compruebo si el capitan coincide en parametros con
        ## nombre y rol

    def test_planetas_capi(self):
        mision1 = Mision.objects.create(nombre="reconquistar la isla parte 1", nave=self.nave, finalizada=True, exito=True)
        Tripulacion.objects.create(mision=mision1, usuario=self.capitan, rol=Rol.CAPITAN)
        Exoplaneta.objects.create(nombre="turk-alert", mision=mision1)

        mision2 = Mision.objects.create(nombre="reconquistar la isla parte 2", nave=self.nave, finalizada=True, exito=True)
        Tripulacion.objects.create(mision=mision2, usuario=self.tripulante1, rol=Rol.CAPITAN)
        Tripulacion.objects.create(mision=mision2, usuario=self.capitan, rol=Rol.TRIPULANTE)
        Exoplaneta.objects.create(nombre="turk-alert2", mision=mision2)

        respuesta = self.client.get("/api/capitanes/" + str(self.capitan.id) + "/exoplanetas/")

        self.assertEqual(respuesta.status_code, 200)
        nombres = [planeta["nombre"] for planeta in respuesta.json()["datos"]]
        self.assertEqual(nombres, ["turk-alert"])
        ## Cristobal es capi en la mision 1 y tripulante en la 2
        ## solo debe salir el planeta de la mision 1 turk-alert

## casi me olvido xd los tests de ls otras naves
    def test_nave_mediana(self):
        nave_mediana = Nave.objects.create(nombre="Barco", tamano="MEDIANA")

        capitan = Usuario.objects.create(nombre="Capi", apellidos="Mediano")

        tripulantes = []
        for i in range(7):
            usuario = Usuario.objects.create(nombre="Mediano" + str(i), apellidos="Prueba")
            tripulantes.append(usuario.id)

        datos = {
            "nombre": "MISION DE TAMANO MEDIO",
            "nave": nave_mediana.id,
            "capitanes": [capitan.id],
            "tripulantes": tripulantes,
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Mision.objects.count(), 1)
        self.assertEqual(Tripulacion.objects.count(), 8)
        ## nave mediana con 1 capitan y 7 tripulantes esto hace un total de 8 personitas
        ## esta dentro del rango de 8 a 10 asi que se crea la mision

    def test_nave_grande(self):
        nave_grande = Nave.objects.create(nombre="Barcaza", tamano="GRANDE")

        capitan1 = Usuario.objects.create(nombre="Capi1", apellidos="Grande")
        capitan2 = Usuario.objects.create(nombre="Capi2", apellidos="Grande")

        tripulantes = []
        for i in range(9):
            usuario = Usuario.objects.create(nombre="Grande" + str(i), apellidos="Prueba")
            tripulantes.append(usuario.id)

        datos = {
            "nombre": "MISION GRANDE",
            "nave": nave_grande.id,
            "capitanes": [capitan1.id, capitan2.id],
            "tripulantes": tripulantes,
        }

        respuesta = self.client.post("/api/misiones/asignar/",
            data=datos,
            content_type="application/json")

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Mision.objects.count(), 1)
        self.assertEqual(Tripulacion.objects.filter(rol=Rol.CAPITAN).count(), 2)
        ## nave grande con 2 capitanes y 9 tripulantes lo que suman 11 personas en total
        ## lleva los 2 capitanes que necesita y llega al minimo de 11 asi que se crea la mision