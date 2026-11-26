from django.http import JsonResponse
import json
from json import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt

from .models import Usuario


def listar_usuarios(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    usuarios = Usuario.objects.all().values()
    return JsonResponse(list(usuarios), safe=False)

@csrf_exempt
def crear_usuario(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El JSON no está bien formado"},
            status=400
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "El JSON debe contener un objeto"},
            status=400
        )

    nombre = datos.get("nombre")
    apellidos = datos.get("apellidos")

    if not isinstance(nombre, str) or not nombre.strip():
        return JsonResponse({"error": "El nombre es obligatorio"}, status=400)

    if not isinstance(apellidos, str) or not apellidos.strip():
        return JsonResponse({"error": "Los apellidos son obligatorios"}, status=400)

    if len(nombre.strip()) > 100 or len(apellidos.strip()) > 150:
        return JsonResponse({"error": "Nombre o apellidos demasiado largos"}, status=400)

    caracteristicas = [
        "misiones_largas",
        "explorador_cortas_distancias",
        "conflictivo",
        "cocinero",
        "mantenimiento",
    ]

    for campo in caracteristicas:
        if campo in datos and not isinstance(datos[campo], bool):
            return JsonResponse(
                {"error": f"{campo} debe ser true o false"},
                status=400
            )

    usuario = Usuario.objects.create(
        nombre=nombre.strip(),
        apellidos=apellidos.strip(),
        misiones_largas=datos.get("misiones_largas", False),
        explorador_cortas_distancias=datos.get("explorador_cortas_distancias", False),
        conflictivo=datos.get("conflictivo", False),
        cocinero=datos.get("cocinero", False),
        mantenimiento=datos.get("mantenimiento", False),
    )

    return JsonResponse(
        {"mensaje": "Usuario creado correctamente", "id": usuario.id},
        status=201
    )

def consultar_usuario(request, id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    usuario = Usuario.objects.filter(id=id).values().first()

    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    return JsonResponse(usuario)

@csrf_exempt
def modificar_usuario(request, id):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    usuario = Usuario.objects.filter(id=id).first()

    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "El JSON no está bien formado"},
            status=400
        )

    if not isinstance(datos, dict) or not datos:
        return JsonResponse(
            {"error": "Debes enviar un objeto JSON con datos"},
            status=400
        )

    campos_texto = {"nombre": 100, "apellidos": 150}
    caracteristicas = [
        "misiones_largas",
        "explorador_cortas_distancias",
        "conflictivo",
        "cocinero",
        "mantenimiento",
    ]

    campos_permitidos = set(campos_texto) | set(caracteristicas)

    for campo, valor in datos.items():
        if campo not in campos_permitidos:
            return JsonResponse(
                {"error": f"Campo no permitido: {campo}"},
                status=400
            )

        if campo in campos_texto:
            if not isinstance(valor, str) or not valor.strip():
                return JsonResponse(
                    {"error": f"{campo} no puede estar vacío"},
                    status=400
                )
            if len(valor.strip()) > campos_texto[campo]:
                return JsonResponse(
                    {"error": f"{campo} es demasiado largo"},
                    status=400
                )
            valor = valor.strip()

        if campo in caracteristicas and not isinstance(valor, bool):
            return JsonResponse(
                {"error": f"{campo} debe ser true o false"},
                status=400
            )

        setattr(usuario, campo, valor)

    usuario.save()

    return JsonResponse({"mensaje": "Usuario modificado correctamente"})

@csrf_exempt
def eliminar_usuario(request, id):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    usuario = Usuario.objects.filter(id=id).first()

    if usuario is None:
        return JsonResponse(
            {"error": "Usuario no encontrado"},
            status=404
        )

    usuario.delete()

    return JsonResponse({"mensaje": "Usuario eliminado correctamente"})