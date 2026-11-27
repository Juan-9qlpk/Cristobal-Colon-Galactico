from django.http import JsonResponse
import json
from json import JSONDecodeError

from django.views.decorators.csrf import csrf_exempt

from .models import Usuario, Nave, Mision, Tripulacion, Exoplaneta, Rol


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

def error(mensaje, codigo):
    return JsonResponse({"ok": False, "error": mensaje}, status=codigo)

def exito(mensaje, datos, codigo):
    return JsonResponse({"ok": True, "mensaje": mensaje, "datos": datos}, status=codigo)

def comprobar_operacion(request, metodo):
    if request.method != metodo:
        return error("Operacion no permitida", 405)
    return None

def leer_jasones(request):
    try:
        datos = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return error("JSON invalido", 400)

    if not isinstance(datos, dict):
        return error("Se esperaba un objeto JSON", 400)

    return datos

def comprobar_tamano(nave, tripulacion, capitanes):
    if nave.tamano == "PEQUENA":
        if capitanes != 1:
            return "Una nave pequena necesita 1 capitan"
        if tripulacion != 4:
            return "Una nave pequena debe llevar 4 personas"

    if nave.tamano == "MEDIANA":
        if capitanes != 1:
            return "Una nave mediana necesita 1 capitan"
        if tripulacion < 8 or tripulacion > 10:
            return "Una nave mediana debe llevar entre 8 y 10 personas"

    if nave.tamano == "GRANDE":
        if capitanes != 2:
            return "Una nave grande necesita 2 capitanes"
        if tripulacion < 11 or tripulacion > 30:
            return "Una nave grande debe llevar entre 11 y 30 personas"
    return None


def comprobar_nave(nave, num_capitanes, num_tripulantes):
    tripulacion = num_capitanes + num_tripulantes
    return comprobar_tamano(nave, tripulacion, num_capitanes)

@csrf_exempt
def crear_nave(request):
    fallo = comprobar_operacion(request, "POST")
    if fallo is not None:
        return fallo

    datos = leer_jasones(request)
    if not isinstance(datos, dict):
        return datos

    nombre = datos.get("nombre")
    tamano = datos.get("tamano")
    if not isinstance(nombre, str) or nombre == "":
        return error("El nombre de la nave es obligatorio", 400)

    if tamano not in Nave.Tamano.values:
        return error("El tamano debe ser PEQUENA, MEDIANA o GRANDE", 400)

    nave = Nave.objects.create(nombre=nombre, tamano=tamano)
    return exito("Nave creada correctamente", datos, 201)

@csrf_exempt
def asignar_mision(request):
    fallo = comprobar_operacion(request, "POST")
    if fallo is not None:
        return fallo

    datos = leer_jasones(request) ## intente modularizarlo mas pero no sabia como xd
    if not isinstance(datos, dict):
        return datos

    nombre = datos.get("nombre")
    nave = datos.get("nave")
    capitanes = datos.get("capitanes", [])
    tripulantes = datos.get("tripulantes", [])
    if not isinstance(nombre, str) or nombre == "":
        return error("El nombre de la mision es obligatorio", 400)

    if not nave:
        return error("La mision necesita una nave", 400)

    nave_encontrada = Nave.objects.filter(id=nave).first()
    if nave_encontrada is None:
        return error("La nave no existe", 400)

    if not isinstance(capitanes, list) or not isinstance(tripulantes, list):
        return error("capitanes y tripulantes deben ser listas", 400)

    todos = capitanes + tripulantes
    vistos = []
    for usuario_id in todos:
        if usuario_id in vistos:
            return error("Hay tripulantes repetidos", 400)
        vistos.append(usuario_id)

    for usuario_id in todos:
        if not Usuario.objects.filter(id=usuario_id).exists():
            return error("El tripulante " + str(usuario_id) + " no existe", 400)

    fallo_nave = comprobar_nave(nave_encontrada, len(capitanes), len(tripulantes))
    if fallo_nave:
        return error(fallo_nave, 400)

    if Mision.objects.filter(nave=nave_encontrada, finalizada=False).exists():
        return error("La nave ya esta en una mision en curso", 400)

    for usuario_id in todos:
        if Tripulacion.objects.filter(usuario_id=usuario_id, mision__finalizada=False).exists():
            return error("El usuario " + str(usuario_id) + " ya esta en otra mision en curso", 400)

    mision = Mision.objects.create(nombre=nombre, nave=nave_encontrada)
    for usuario_id in capitanes:
        Tripulacion.objects.create(mision=mision, usuario_id=usuario_id, rol=Rol.CAPITAN)

    for usuario_id in tripulantes:
        Tripulacion.objects.create(mision=mision, usuario_id=usuario_id, rol=Rol.TRIPULANTE)
    return exito("mision asignada correctamente", {"id": mision.id}, 201)


@csrf_exempt
def finalizar_mision(request, id):
    fallo = comprobar_operacion(request, "POST")
    if fallo is not None:
        return fallo

    mision_encontrada = Mision.objects.filter(id=id).first()
    if mision_encontrada is None:
        return error("Mision no encontrada", 404)

    if mision_encontrada.finalizada:
        return error("La mision ya esta finalizada", 400)

    datos = leer_jasones(request)
    if not isinstance(datos, dict):
        return datos

    resultado = datos.get("exito")
    exoplanetas = datos.get("exoplanetas", [])
    if not isinstance(resultado, bool):
        return error("exito debe ser true o false", 400)

    if not isinstance(exoplanetas, list):
        return error("exoplanetas debe ser una lista", 400)

    if resultado is False and len(exoplanetas) > 0:
        return error("Solo se registran exoplanetas si la mision tiene exito", 400)

    ## como tal deja claro en el este que se pueden registrar varios exoplanetas en una misione exitosa
    ## asi que lo voy a dejar asi...

    mision_encontrada.finalizada = True
    mision_encontrada.exito = resultado
    mision_encontrada.save()
    for nombre_planeta in exoplanetas:
        Exoplaneta.objects.create(nombre=nombre_planeta, mision=mision_encontrada)
    return exito("Mision finalizada correctamente", None, 200)


def tripulacion_mision(request, id):
    fallo = comprobar_operacion(request, "GET")
    if fallo is not None:
        return fallo

    mision_encontrada = Mision.objects.filter(id=id).first()
    if mision_encontrada is None:
        return error("Mision no encontrada", 404)

    tripulacion = []
    for miembro in Tripulacion.objects.filter(mision=mision_encontrada):
        tripulacion.append({"id": miembro.usuario.id, "nombre": miembro.usuario.nombre, "apellidos": miembro.usuario.apellidos, "rol": miembro.rol})

    datos = {"mision": mision_encontrada.nombre, "tripulacion": tripulacion,}
    return exito("tripulacion de la mision", datos, 200)

def planetas_capitan(request, id):
    fallo = comprobar_operacion(request, "GET")
    if fallo is not None:
        return fallo

    if not Usuario.objects.filter(id=id).exists():
        return error("Usuario no encontrado", 404)

    capitan = Usuario.objects.filter(id=id).first()
    if capitan is None:
        return error("Usuario no encontrado", 404)

    planetas = Exoplaneta.objects.filter(mision__tripulacion__usuario_id=id, mision__tripulacion__rol=Rol.CAPITAN).distinct().values("id", "nombre", "mision_id")
    datos = {"capitan": capitan.nombre + " " + capitan.apellidos, "planetas": list(planetas)}
    return exito("Planetas descubiertos por el capitan", datos, 200)