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

class Mision(models.Model):
    ## el protect en nave lo que me permite es evitar que se borre si tiene una mision activa
    nombre = models.CharField(max_length=100)
    nave = models.ForeignKey(Nave, on_delete=models.PROTECT, related_name="misiones")
    finalizada = models.BooleanField(default=False)
    exito = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.nombre

class Rol(models.TextChoices): ## esto es lo que he encontrado como enum de kotlin, literalmente busque enum kotlin en python
    CAPITAN = "capitan"
    TRIPULANTE = "tripulante"

class Tripulacion(models.Model):
    ## un usuario puede estar en varias misiones pero no al mismo tiempo
    ## la cosa es que en cada mision puede tener un rol diferente
    ## asi que necesito guardar los datos de la mision, el usuario y su rol
    ## en la misión que pasó
    ## es basicamente una tabla usuario_misiones donde añades rol, que viene de rol
    ## para saber que rol cumple
    mision = models.ForeignKey(Mision, on_delete=models.CASCADE, related_name="tripulacion")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tripulaciones")
    rol = models.CharField(max_length=10, choices=Rol.choices)

    def __str__(self):
        return str(self.usuario) + ", " + self.rol + ", " + str(self.mision)

class Exoplaneta(models.Model):
    nombre = models.CharField(max_length=100)
    mision = models.ForeignKey(Mision, on_delete=models.CASCADE, related_name="exoplanetas")

    def __str__(self):
        return self.nombre