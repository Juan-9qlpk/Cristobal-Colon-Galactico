# Cristóbal Colón Galáctico

> En 1492 Colón cruzó el Atlántico con tres carabelas. Ahora toca cruzar la galaxia.

**Cristóbal Colón Galáctico** es una API REST hecha con Django para organizar expediciones espaciales en busca de nuevos exoplanetas. Desde aquí se recluta a la tripulación, se preparan las naves, se lanzan las misiones y se registra cada mundo descubierto.

No todas las expediciones vuelven con éxito, y no cualquiera puede subirse a una nave: cada misión tiene que cumplir las reglas de la flota antes de despegar.

### Qué permite hacer

- **Reclutar tripulantes:** alta, consulta, modificación y baja de usuarios con sus cinco características (misiones largas, explorador de cortas distancias, conflictivo, cocinero y mantenimiento).
- **Preparar la flota:** naves pequeñas, medianas y grandes, cada una con su capacidad y su número de capitanes.
- **Lanzar misiones:** se asigna una nave y su tripulación, comprobando que nadie esté ya en otra misión en curso y que la nave vaya con las personas y los capitanes que le corresponden.
- **Volver a casa:** se finaliza la misión con éxito o con fracaso y, si sale bien, se registran los exoplanetas descubiertos.
- **Consultar el cuaderno de bitácora:** quién viajó en cada misión y qué planetas ha descubierto cada capitán.

## Instalación y ejecución

Requisitos previos: [Python](https://www.python.org/downloads/) 3.12 o superior (Django 6.1 no funciona con versiones anteriores) y [Git](https://git-scm.com/downloads).

1. Clonar el repositorio y entrar en la carpeta:

   ```powershell
   git clone https://github.com/Juan-9qlpk/Cristobal-Colon-Galactico.git
   cd Cristobal-Colon-Galactico
   ```

2. Crear un entorno virtual:

   ```powershell
   python -m venv .venv
   ```

3. Activarlo en PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Si Windows muestra un error porque la ejecución de scripts está deshabilitada, hay que ejecutar una vez este comando y volver a activar el entorno:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

4. Instalar las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Aplicar las migraciones:

   ```powershell
   python manage.py migrate
   ```

6. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

La API estará disponible en `http://127.0.0.1:8000/api/`. Por ejemplo, `http://127.0.0.1:8000/api/usuarios/` devuelve la lista de usuarios.

## Datos de prueba

La factoría usa la librería Faker para generar nombres aleatorios. Se ejecuta con:

```powershell
python manage.py factoria
```

El comando añade 20 usuarios con características aleatorias, tres naves (una de cada tamaño), tres misiones y dos exoplanetas.

Las misiones incluyen:

- Una misión pequeña finalizada con éxito y dos exoplanetas descubiertos.
- Una misión mediana finalizada sin éxito.
- Una misión grande en curso.

Cada ejecución añade nuevos datos a la base de datos. Para empezar de cero, se borra `db.sqlite3` y se vuelve a ejecutar `python manage.py migrate`.

## API de usuarios

La URL base durante el desarrollo es:

```text
http://127.0.0.1:8000/api/
```

Las peticiones con cuerpo usan JSON (`Content-Type: application/json`) y todas las URL terminan en `/`. Si algo falla, la respuesta tiene la forma `{"error": "mensaje"}`.

### Listar usuarios

- Método: `GET`
- URL: `/api/usuarios/`

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "nombre": "Dani",
    "apellidos": "Prueba",
    "misiones_largas": false,
    "explorador_cortas_distancias": false,
    "conflictivo": false,
    "cocinero": true,
    "mantenimiento": false
  }
]
```

### Consultar un usuario

- Método: `GET`
- URL: `/api/usuarios/<id>/`
- Parámetro: `id` del usuario que se quiere consultar.

Ejemplo de respuesta:

```json
{
  "id": 1,
  "nombre": "Dani",
  "apellidos": "Prueba",
  "misiones_largas": false,
  "explorador_cortas_distancias": false,
  "conflictivo": false,
  "cocinero": true,
  "mantenimiento": false
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| El usuario no existe | `404` | `Usuario no encontrado` |

### Crear un usuario

- Método: `POST`
- URL: `/api/usuarios/crear/`
- El cuerpo de la petición debe estar en formato JSON.
- `nombre` y `apellidos` son obligatorios. Las características son
  opcionales y toman el valor `false` si no se indican.

Ejemplo de petición:

```json
{
  "nombre": "Dani",
  "apellidos": "Prueba",
  "cocinero": true,
  "mantenimiento": false
}
```

Ejemplo de respuesta:

```json
{
  "mensaje": "Usuario creado correctamente",
  "id": 1
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| Falta el nombre o está vacío | `400` | `El nombre es obligatorio` |
| Faltan los apellidos o están vacíos | `400` | `Los apellidos son obligatorios` |
| Nombre de más de 100 caracteres o apellidos de más de 150 | `400` | `Nombre o apellidos demasiado largos` |
| Una característica no es `true` ni `false` | `400` | `cocinero debe ser true o false` (con el nombre del campo) |
| JSON mal escrito | `400` | `El JSON no está bien formado` |
| El cuerpo no es un objeto (por ejemplo `[]`) | `400` | `El JSON debe contener un objeto` |
| Método distinto de `POST` | `405` | `Método no permitido` |

### Modificar un usuario

- Método: `PATCH`
- URL: `/api/usuarios/<id>/modificar/`
- Parámetro: `id` del usuario que se quiere modificar.
- El cuerpo contiene únicamente los campos que se quieren cambiar.

Ejemplo de petición:

```json
{
  "cocinero": false,
  "mantenimiento": true
}
```

Ejemplo de respuesta:

```json
{
  "mensaje": "Usuario modificado correctamente"
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| El usuario no existe | `404` | `Usuario no encontrado` |
| Cuerpo vacío (`{}`) o que no es un objeto | `400` | `Debes enviar un objeto JSON con datos` |
| Campo que no existe en el usuario | `400` | `Campo no permitido: edad` (con el nombre del campo) |
| Nombre o apellidos vacíos | `400` | `nombre no puede estar vacío` (con el nombre del campo) |
| Nombre o apellidos demasiado largos | `400` | `nombre es demasiado largo` (con el nombre del campo) |
| Una característica no es `true` ni `false` | `400` | `cocinero debe ser true o false` (con el nombre del campo) |
| JSON mal escrito | `400` | `El JSON no está bien formado` |
| Método distinto de `PATCH` | `405` | `Método no permitido` |

### Eliminar un usuario

- Método: `DELETE`
- URL: `/api/usuarios/<id>/eliminar/`
- Parámetro: `id` del usuario que se quiere eliminar.

Ejemplo de respuesta:

```json
{
  "mensaje": "Usuario eliminado correctamente"
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| El usuario no existe | `404` | `Usuario no encontrado` |
| Método distinto de `DELETE` | `405` | `Método no permitido` |

## API de naves y misiones

Todas las respuestas de estos endpoints tienen el mismo formato:

- Si todo va bien: `"ok": true`, un `"mensaje"` y los `"datos"`.
- Si algo falla: `"ok": false` y un `"error"` que explica el motivo.

Las peticiones con cuerpo usan JSON (`Content-Type: application/json`) y todas las URL terminan en `/`.

### Códigos de estado

| Código | Significado |
|---|---|
| `200` | Consulta o acción correcta |
| `201` | Nave o misión creada |
| `400` | JSON inválido, datos incorrectos o regla de negocio incumplida |
| `404` | La misión o el usuario de la URL no existen |
| `405` | Método HTTP no permitido (`"Operacion no permitida"`) |

### Reglas de negocio

| Tipo de nave | Personas a bordo | Capitanes |
|---|---|---|
| Pequeña | 4 | 1 |
| Mediana | Entre 8 y 10 | 1 |
| Grande | Entre 11 y 30 | 2 |

- Los capitanes cuentan dentro de la tripulación: una nave pequeña lleva 1 capitán y 3 tripulantes.
- La capacidad de cada nave se obtiene de su tamaño.
- Una misión debe tener una nave asignada.
- Una nave no puede estar en dos misiones en curso a la vez.
- Un usuario no puede estar en dos misiones en curso a la vez, ni como capitán ni como tripulante.
- Una misión finalizada no se puede volver a finalizar.
- Solo se registran exoplanetas cuando la misión termina con éxito. Una misión con éxito puede tener varios exoplanetas o ninguno.
- Una nave con misiones no se puede borrar (`on_delete=PROTECT`).

### Crear una nave

- Método: `POST`
- URL: `/api/naves/crear/`
- `nombre` es obligatorio.
- `tamano` debe ser `PEQUENA`, `MEDIANA` o `GRANDE`.

Ejemplo de petición:

```json
{
  "nombre": "La Niña",
  "tamano": "PEQUENA"
}
```

Ejemplo de respuesta (`201`):

```json
{
  "ok": true,
  "mensaje": "Nave creada correctamente",
  "datos": {
    "nombre": "La Niña",
    "tamano": "PEQUENA"
  }
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| Sin nombre | `400` | `El nombre de la nave es obligatorio` |
| Tamaño no válido | `400` | `El tamano debe ser PEQUENA, MEDIANA o GRANDE` |
| JSON mal escrito | `400` | `JSON invalido` |
| El cuerpo no es un objeto (por ejemplo `[]`) | `400` | `Se esperaba un objeto JSON` |
| Método distinto de `POST` | `405` | `Operacion no permitida` |

### Asignar una misión

- Método: `POST`
- URL: `/api/misiones/asignar/`
- `nombre`: nombre de la misión (obligatorio).
- `nave`: ID de la nave (obligatorio).
- `capitanes`: lista con los ID de los capitanes.
- `tripulantes`: lista con los ID de los tripulantes.

Ejemplo para una nave pequeña:

```json
{
  "nombre": "Primera expedición",
  "nave": 1,
  "capitanes": [1],
  "tripulantes": [2, 3, 4]
}
```

Ejemplo para una nave grande (2 capitanes y 9 tripulantes):

```json
{
  "nombre": "Gran expedición",
  "nave": 3,
  "capitanes": [1, 2],
  "tripulantes": [3, 4, 5, 6, 7, 8, 9, 10, 11]
}
```

Ejemplo de respuesta (`201`):

```json
{
  "ok": true,
  "mensaje": "mision asignada correctamente",
  "datos": {
    "id": 1
  }
}
```

Errores (todos con código `400`):

| Caso | `error` |
|---|---|
| Sin nombre | `El nombre de la mision es obligatorio` |
| Sin nave | `La mision necesita una nave` |
| Nave inexistente | `La nave no existe` |
| `capitanes` o `tripulantes` no son listas | `capitanes y tripulantes deben ser listas` |
| Un ID aparece dos veces | `Hay tripulantes repetidos` |
| Usuario inexistente | `El tripulante 99 no existe` |
| Número de capitanes incorrecto | `Una nave pequena necesita 1 capitan` |
| Demasiadas o muy pocas personas | `Una nave pequena debe llevar 4 personas` |
| Nave en una misión en curso | `La nave ya esta en una mision en curso` |
| Usuario en otra misión en curso | `El usuario 2 ya esta en otra mision en curso` |

Los mensajes de capacidad y capitanes cambian según el tamaño de la nave, por ejemplo `Una nave grande necesita 2 capitanes` o `Una nave mediana debe llevar entre 8 y 10 personas`.

### Finalizar una misión

- Método: `POST`
- URL: `/api/misiones/<id>/finalizar/`
- `id` es el identificador de la misión.
- `exito`: `true` o `false` (obligatorio).
- `exoplanetas`: lista con los nombres de los planetas descubiertos (opcional). Solo se pueden registrar si la misión ha tenido éxito.

Ejemplo de petición:

```json
{
  "exito": true,
  "exoplanetas": ["Nueva Tierra", "Estrella Azul"]
}
```

Ejemplo de respuesta (`200`):

```json
{
  "ok": true,
  "mensaje": "Mision finalizada correctamente",
  "datos": {
    "mision": "Primera expedición",
    "exito": true,
    "exoplanetas": [
      {"nombre": "Nueva Tierra"},
      {"nombre": "Estrella Azul"}
    ]
  }
}
```

Para una misión fallida, se puede enviar:

```json
{
  "exito": false,
  "exoplanetas": []
}
```

Respuesta (`200`):

```json
{
  "ok": true,
  "mensaje": "Mision finalizada correctamente",
  "datos": {
    "mision": "Segunda expedición",
    "exito": false,
    "exoplanetas": []
  }
}
```

Errores:

| Caso | Código | `error` |
|---|---|---|
| Misión inexistente | `404` | `Mision no encontrada` |
| Misión ya finalizada | `400` | `La mision ya esta finalizada` |
| Falta `exito` o no es `true`/`false` | `400` | `exito debe ser true o false` |
| `exoplanetas` no es una lista | `400` | `exoplanetas debe ser una lista` |
| Exoplanetas en una misión sin éxito | `400` | `Solo se registran exoplanetas si la mision tiene exito` |

### Consultar la tripulación de una misión

- Método: `GET`
- URL: `/api/misiones/<id>/tripulacion/`
- `id` es el identificador de la misión.

Ejemplo de respuesta (`200`):

```json
{
  "ok": true,
  "mensaje": "tripulacion de la mision",
  "datos": {
    "mision": "Primera expedición",
    "tripulacion": [
      {"id": 1, "nombre": "Dani", "apellidos": "Prueba", "rol": "capitan"},
      {"id": 2, "nombre": "Juanma", "apellidos": "Prueba", "rol": "tripulante"},
      {"id": 3, "nombre": "Ana", "apellidos": "Prueba", "rol": "tripulante"},
      {"id": 4, "nombre": "Luis", "apellidos": "Prueba", "rol": "tripulante"}
    ]
  }
}
```

Error: misión inexistente → `404` `Mision no encontrada`.

### Consultar planetas descubiertos por un capitán

- Método: `GET`
- URL: `/api/capitanes/<id>/exoplanetas/`
- `id` es el identificador del usuario.
- Solo salen los planetas de las misiones en las que el usuario fue **capitán**. No cuentan las misiones en las que fue tripulante.

Ejemplo de respuesta (`200`):

```json
{
  "ok": true,
  "mensaje": "Planetas descubiertos por el capitan",
  "datos": {
    "capitan": "Dani Prueba",
    "planetas": [
      {"id": 1, "nombre": "Nueva Tierra", "mision_id": 1},
      {"id": 2, "nombre": "Estrella Azul", "mision_id": 1}
    ]
  }
}
```

Si fue capitán pero sus misiones no descubrieron planetas, `planetas` es una lista vacía.

Errores:

| Caso | Código | `error` |
|---|---|---|
| Usuario inexistente | `404` | `Tripulante no encontrado` |
| El usuario nunca ha sido capitán | `404` | `Este tripulante no ha sido capitan` |

## Pruebas

Las pruebas están en `america/tests.py` y usan `TestCase` de Django. Cada test se ejecuta con una base de datos de pruebas vacía, que se crea al empezar y se borra al terminar, así que no tocan `db.sqlite3`.

Para ejecutar las pruebas automáticas:

```powershell
python manage.py test
```

Para ejecutar solo una clase o un test:

```powershell
python manage.py test america.tests.MisionTest
python manage.py test america.tests.MisionTest.test_asignar_mision
```

### UsuarioAPITest: CRUD de usuarios

| Test | Qué comprueba |
|---|---|
| `test_listar_usuarios` | Listar usuarios devuelve `200` y el usuario creado |
| `test_consultar_usuario` | Consultar un usuario existente devuelve sus datos |
| `test_consultar_usuario_inexistente` | Consultar un ID que no existe devuelve `404` |
| `test_crear_usuario` | Crear un usuario devuelve `201` y se guarda en la base de datos |
| `test_crear_usuario_sin_nombre` | Crear un usuario sin nombre devuelve `400` |
| `test_modificar_usuario` | Modificar las características de un usuario las guarda |
| `test_eliminar_usuario` | Eliminar un usuario lo borra de la base de datos |

### FactoriaTest: datos de prueba

| Test | Qué comprueba |
|---|---|
| `test_factoria_crea_usuarios_y_naves` | La factoría crea 20 usuarios y una nave de cada tamaño |
| `test_factoria_crea_misiones_y_exoplanetas` | Crea una misión en curso, una con éxito y otra sin éxito; los 2 exoplanetas son de la misión con éxito; cada misión cumple la capacidad y los capitanes de su nave, y ningún usuario está en dos misiones en curso |

### MisionTest: misiones, tripulación y exoplanetas

Antes de cada test, `setUp()` crea dos naves pequeñas (`Islote` e `Isla`) y cinco usuarios: un capitán, tres tripulantes y uno extra.

| Test | Qué comprueba |
|---|---|
| `test_crear_mision` | Una misión nueva empieza sin finalizar y sin resultado |
| `test_no_se_puede_borrar_nave_con_misiones` | `PROTECT` impide borrar una nave que tiene misiones |
| `test_asignar_mision` | Asignar 1 capitán y 3 tripulantes a una nave pequeña devuelve `201` y crea 4 tripulantes |
| `test_navent` | Una misión sin nave devuelve `400` y no se crea |
| `test_muchas_personas` | 5 personas en una nave pequeña devuelve `400` |
| `test_meter_capitanes` | 2 capitanes en una nave pequeña devuelve `400` |
| `test_mision_usuario` | Los mismos usuarios no pueden ir a una segunda misión mientras la primera sigue en curso |
| `test_finalizar_y_guardar` | Finalizar con éxito guarda el resultado y los 2 exoplanetas |
| `test_guardar_planetoides` | Enviar exoplanetas en una misión sin éxito devuelve `400` y la misión sigue sin finalizar |
| `test_no_finalizar_dos_veces` | Una misión ya finalizada no se puede volver a finalizar ni cambiar su resultado |
| `test_preguntar_tripulacion` | La tripulación de una misión devuelve sus 2 miembros y el capitán con rol `capitan` |
| `test_planetas_capi` | Un capitán solo ve los planetas de las misiones en las que fue capitán, no los de aquellas en las que fue tripulante |
| `test_nave_mediana` | Una nave mediana con 1 capitán y 7 tripulantes (8 personas) devuelve `201` |
| `test_nave_grande` | Una nave grande con 2 capitanes y 9 tripulantes (11 personas) devuelve `201` |

### Pruebas manuales con Postman

En la raíz del repositorio está la colección `cristobal_colocolo.postman_collection.json`. Se importa en Postman con **Import** y contiene peticiones para el CRUD de usuarios, la creación de naves, la gestión de misiones y pruebas sobre los datos de la factoría. Conviene empezar con la base de datos vacía para que los ID coincidan:

```powershell
del db.sqlite3
python manage.py migrate
python manage.py runserver
```

## Trabajo realizado

### Dani

- Modelos iniciales de usuarios y naves.
- CRUD de usuarios y pruebas automáticas.
- Factoría para generar usuarios, naves, misiones, tripulaciones
  y exoplanetas de prueba.
- Documentación de instalación, pruebas y API de usuarios.

### Juanma

- Modelos de misiones, tripulación (capitán o tripulante) y exoplanetas.
- Endpoints para asignar y finalizar misiones, consultar la tripulación
  y consultar los exoplanetas descubiertos por un capitán.
- Reglas de capacidad, capitanes, disponibilidad de usuarios, nave obligatoria,
  misiones finalizadas y exoplanetas solo en misiones con éxito.
- Pruebas de misiones, tripulación y exoplanetas.
- Documentación de la API de naves y misiones.
