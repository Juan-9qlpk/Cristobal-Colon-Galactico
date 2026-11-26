from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)

    # Características y habilidades del usuario
    misiones_largas = models.BooleanField(default=False)
    explorador_cortas_distancias = models.BooleanField(default=False)
    conflictivo = models.BooleanField(default=False)
    cocinero = models.BooleanField(default=False)
    mantenimiento = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Nave(models.Model):
    class Tamano(models.TextChoices):
        PEQUENA = "PEQUENA", "Pequeña"
        MEDIANA = "MEDIANA", "Mediana"
        GRANDE = "GRANDE", "Grande"

    nombre = models.CharField(max_length=100)
    tamano = models.CharField(max_length=10, choices=Tamano.choices)

    def __str__(self):
        return f"{self.nombre} ({self.get_tamano_display()})"