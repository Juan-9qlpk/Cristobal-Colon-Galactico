# Cristóbal Colón Galáctico

Proyecto desarrollado con Django para gestionar expediciones espaciales.
La aplicación permitirá administrar usuarios, naves, misiones y exoplanetas
a través de una API.

## Instalación y ejecución

1. Crear un entorno virtual:

   ```powershell
   python -m venv .venv
   ```

2. Activarlo en PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instalar las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Aplicar las migraciones:

   ```powershell
   python manage.py migrate
   ```

5. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Datos de prueba

El comando añade 20 usuarios, tres naves, tres misiones y dos exoplanetas.

Las misiones incluyen:

- Una misión pequeña finalizada con éxito y dos exoplanetas descubiertos.
- Una misión mediana finalizada sin éxito.
- Una misión grande en curso.

Cada ejecución añade nuevos datos a la base de datos.

```powershell
python manage.py factoria
```

El comando añade 20 usuarios y tres naves, una de cada tamaño.
Cada ejecución añade nuevos datos a la base de datos.

## Pruebas

Para ejecutar las pruebas automáticas:

```powershell
python manage.py test
```

## API de usuarios

La URL base durante el desarrollo es:

```text
http://127.0.0.1:8000/api/
```

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

## Trabajo realizado

### Dani

- Modelos iniciales de usuarios y naves.
- CRUD de usuarios y pruebas automáticas.
- Factoría para generar usuarios, naves, misiones, tripulaciones
  y exoplanetas de prueba.
- Documentación de instalación, pruebas y API de usuarios.

### Juanma

- Desarrollo de misiones, tripulaciones y exoplanetas.