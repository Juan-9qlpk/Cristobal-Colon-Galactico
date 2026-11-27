import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from america.models import Exoplaneta, Mision, Nave, Rol, Tripulacion, Usuario


class Command(BaseCommand):
    help = "Genera datos de prueba para las expediciones"

    @transaction.atomic
    def handle(self, *args, **options):
        faker = Faker("es_ES")
        usuarios = []

        # Creamos usuarios con distintas características.
        for _ in range(20):
            usuario = Usuario.objects.create(
                nombre=faker.first_name(),
                apellidos=faker.last_name(),
                misiones_largas=random.choice([True, False]),
                explorador_cortas_distancias=random.choice([True, False]),
                conflictivo=random.choice([True, False]),
                cocinero=random.choice([True, False]),
                mantenimiento=random.choice([True, False]),
            )
            usuarios.append(usuario)

        # Creamos una nave de cada tamaño.
        naves = {}
        for tamano in Nave.Tamano.values:
            naves[tamano] = Nave.objects.create(
                nombre=f"Nave {faker.last_name()}",
                tamano=tamano,
            )

        # Misión pequeña finalizada con éxito: 1 capitán y 3 tripulantes.
        mision_exitosa = Mision.objects.create(
            nombre="Exploración exitosa",
            nave=naves[Nave.Tamano.PEQUENA],
            finalizada=True,
            exito=True,
        )
        self.crear_tripulacion(mision_exitosa, usuarios[:4], 1)

        Exoplaneta.objects.create(nombre="Nueva Tierra", mision=mision_exitosa)
        Exoplaneta.objects.create(nombre="Estrella Azul", mision=mision_exitosa)

        # Misión mediana finalizada sin éxito: 1 capitán y 7 tripulantes.
        mision_fallida = Mision.objects.create(
            nombre="Exploración fallida",
            nave=naves[Nave.Tamano.MEDIANA],
            finalizada=True,
            exito=False,
        )
        self.crear_tripulacion(mision_fallida, usuarios[4:12], 1)

        # Misión grande en curso: 2 capitanes y 9 tripulantes.
        # Algunos participaron en misiones anteriores ya finalizadas.
        mision_en_curso = Mision.objects.create(
            nombre="Exploración en curso",
            nave=naves[Nave.Tamano.GRANDE],
        )
        self.crear_tripulacion(mision_en_curso, usuarios[:11], 2)

        self.stdout.write(
            self.style.SUCCESS(
                "Se han creado 20 usuarios, 3 naves, 3 misiones "
                "y 2 exoplanetas."
            )
        )

    def crear_tripulacion(self, mision, usuarios, numero_capitanes):
        for posicion, usuario in enumerate(usuarios):
            if posicion < numero_capitanes:
                rol = Rol.CAPITAN
            else:
                rol = Rol.TRIPULANTE

            Tripulacion.objects.create(
                mision=mision,
                usuario=usuario,
                rol=rol,
            )