from django.urls import path

from . import views

urlpatterns = [
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:id>/", views.consultar_usuario, name="consultar_usuario"),
    path("usuarios/<int:id>/modificar/",views.modificar_usuario,name="modificar_usuario"),
    path("usuarios/<int:id>/eliminar/",views.eliminar_usuario,name="eliminar_usuario"),
    
    ## copio tu formato de hacer las rutas para lo mio asi queda mas unificado
    path("naves/crear/", views.crear_nave, name="crear_nave"),
    path("misiones/asignar/", views.asignar_mision, name="asignar_mision"),
    path("misiones/<int:id>/finalizar/", views.finalizar_mision, name="finalizar_mision"),
    path("misiones/<int:id>/tripulacion/", views.tripulacion_mision, name="tripulacion_mision"),
    path("capitanes/<int:id>/exoplanetas/", views.planetas_capitan, name="planetas_capitan"),
]