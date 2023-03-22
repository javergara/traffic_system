# N5

## Python dev challenge

Se le encarga crear un sistema de registro de infracciones de tránsito en Python.

## Como correr el proyecto

### Local

1. Clone el repositorio desde 
    
    [https://github.com/javergara/traffic_system.git](https://github.com/javergara/traffic_system.git)
    
2. Instale python 3.11
3. Instale nodejs en versiones mayores o iguales a la 16.x
4. Cree un ambiente virtual de python con el comando:
    
    `python -m venv env`
    
5. Active el ambiente `env`
6. Instale los requerimientos con `pip install -r requirements.txt`
7. Corra el servidor ejecutando `uvicorn main:app --host 0.0.0.0 --port 8000`
8. Corra el cliente ejecutando `node client/server.js`
9. El servidor web estará corriendo en [http://localhost:3000/](http://localhost:3000/) y el backend en [http://localhost:8000](http://localhost:8000/)
10. Si quiere acceder a la documentación de la API la puede encontrar en [http://localhost:8000](http://localhost:8000/)/docs

### Docker

Para correr la aplicación usando docker los pasos son:

1. Descargue la imagen de Docker con:
    
    ```python
    docker pull javergara/traffic_system_fastapi:v1
    ```
    
2.  ejecute el comando docker 
    
    ```python
    sudo docker run -p 8000:8000 -p 3000:3000 javergara/traffic_system_fastapi:v1
    ```
    
3. El servidor web estará corriendo en [http://localhost:3000/](http://localhost:3000/) y el backend en [http://localhost:8000](http://localhost:8000/)
4. Si quiere acceder a la documentación de la API la puede encontrar en [http://localhost:8000](http://localhost:8000/)/docs

> **Tener en cuenta:** La base de datos es una base de datos SQLite
> 

### Interactuar con la app

Al abrir el cliente en el navegador a través de [http://localhost:3000/](http://localhost:3000/) se abre una interfaz administrativa donde por medio de formularios puede crear, ver, modificar y borrar registros de los tres elementos de la base de datos que son : 

- Persona :  ID, Nombre, Correo electrónico
- Vehículo: Placa, marca, color, ID (de la persona a la que le pertenece el vehículo)
- Oficiales: Nombre, Id del agente, password
    
    > **Supuesto**: No se creo un sistema de roles donde hayan roles de administrador, cualquier persona puede modificar los elementos
    > 
    
    > **Nota**: Al hacer una modificación por favor recargue la pagina para que se visualice el cambio
    > 

### Cargar infracción:

Para cargar una infracción el agente debe estar creado en la base de datos, para cargar la infracción debe llamar la ruta login a través del método POST y autenticarse con su ID de agente (debe ser un numero entero) y su password, para hacerlo puede usar el comando: 

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=1234&password=1234&scope=&client_id=&client_secret='
```

> **Nota**: asegúrese de cambiar en la ultima linea, el username={id_agente} y password={password}
> 

Esto le devolverá un access token el cual debe usar como token para llamar al método de cargar infracción

Response body:

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0IiwiZXhwIjoxNjc5NDk2MDU1fQ.cMLT-_QCI_U4dUa2yuOTSNlTtWUJ6VTjCoslauPXXHo",
  "token_type": "bearer"
}
```

---

Una vez se tenga el access_token, se procede a hacer la peticion a la API usando la placa del vehículo a consultar como path parameter en la ruta :  http://127.0.0.1:8000/vehicles/{PLACA_VEHICULO}/tickets/ y el access token como bearer token, además de los comentarios que se deban hacer para la infracción que se esta creando, un ejemplo usando el access_token anterior seria:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/vehicles/gsx123/tickets/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0IiwiZXhwIjoxNjc5NDk2MzgzfQ.q00ExvOCd8nbPAH153IABEnTn5fU56LB36cA1VDVmcE' \
  -H 'Content-Type: application/json' \
  -d '{
  "comments": "Max speed"
}'
```

> **Nota**: este ejemplo esta con la placa gsx123, recuerde cambiarlo a la placa que desea junto a los comentarios que en este caso se encuentran como  `"comments": "Max speed"`
> 

> **Supuesto:** La infracción se carga con un timestamp que se registra en la base de datos en el momento que se accede a ella, por lo que no es necesario que lo cargue el agente
> 

> **Supuesto:** No se tiene un campo de on update timestamp ya que no se deberia cambiar la fecha en la que se crea la infraccion
> 

### Generar informe

Para generar el informe se debe acceder a **`'http://127.0.0.1:8000/report/{email}/'`** con el email de la persona a consultar, se puede ver un ejemplo con:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/report/javergara91%40gmail.com/' \
  -H 'accept: application/json'
```

> **Nota**: Recordar cambiar el Path parameter del email
> 

al generar el inform se incluyen los siguientes campos para poder acceder a la lista de tickets por placa 

![Untitled](N5%20e30b44f6e17c4088a72625095837bfee/Untitled.png)

### Deuda técnica(backlog):

- Implementar sistema de roles para que haya un rol administrativo que sea el único que pueda modificar la base de datos, IDEA: Al estar ya la autenticación de los agentes, se podría usar esta para que solo los agentes puedan acceder a las modificaciones de la API
- Implementar las pruebas unitarias
- Implementar arquitectura de routers para la API

##