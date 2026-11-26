from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:id>/", views.consultar_usuario, name="consultar_usuario"),
    path("usuarios/<int:id>/modificar/",views.modificar_usuario,name="modificar_usuario"),
    path("usuarios/<int:id>/eliminar/",views.eliminar_usuario,name="eliminar_usuario"),
]