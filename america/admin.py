from django.contrib import admin
from .models import Exoplaneta, Mision, Nave, Tripulacion, Usuario

admin.site.register(Usuario)
admin.site.register(Nave)
admin.site.register(Mision)
admin.site.register(Tripulacion)
admin.site.register(Exoplaneta)