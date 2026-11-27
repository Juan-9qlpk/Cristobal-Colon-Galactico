import random

from django.core.management.base import BaseCommand
from faker import Faker

from america.models import Nave, Usuario


class Command(BaseCommand):
    help = "Genera usuarios y naves de prueba"

    def handle(self, *args, **options):
        faker = Faker("es_ES")

        for _ in range(20):
            Usuario.objects.create(
                nombre=faker.first_name(),
                apellidos=faker.last_name(),
                misiones_largas=random.choice([True, False]),
                explorador_cortas_distancias=random.choice([True, False]),
                conflictivo=random.choice([True, False]),
                cocinero=random.choice([True, False]),
                mantenimiento=random.choice([True, False]),
            )

        for tamano in Nave.Tamano.values:
            Nave.objects.create(
                nombre=f"Nave {faker.last_name()}",
                tamano=tamano,
            )

        self.stdout.write(
            self.style.SUCCESS("Se han creado 20 usuarios y 3 naves.")
        )