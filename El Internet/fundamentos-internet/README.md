# Fundamentos de Internet

## 1. Del Cliente al Servidor

Cuando una persona escribe `www.youtube.com` en el navegador y presiona Enter, ocurre una serie de pasos antes de que el video pueda mostrarse y reproducirse.

1. **El navegador interpreta la URL.**  
   El navegador identifica el dominio `www.youtube.com` y determina que debe comunicarse con un servidor por medio de Internet. Como YouTube utiliza HTTPS, la comunicación se realiza de forma cifrada.

2. **Se busca la dirección IP mediante DNS.**  
   Los equipos en Internet se comunican utilizando direcciones IP, pero para una persona es más sencillo recordar un nombre como `www.youtube.com`. Por eso se utiliza el sistema **DNS (Domain Name System)**. El navegador y el sistema operativo revisan primero si ya conocen la dirección IP correspondiente. Si no la tienen almacenada, realizan una consulta DNS.

3. **DNS traduce el dominio a una dirección IP.**  
   El servidor DNS responde indicando una dirección IP asociada con YouTube. Esa dirección permite saber hacia qué servidor o infraestructura de Google debe enviarse la comunicación. En servicios grandes como YouTube pueden existir muchas direcciones IP y servidores distribuidos geográficamente.

4. **El cliente establece una conexión.**  
   Una vez conocida la dirección IP, el navegador establece comunicación con el servidor. En HTTPS también se realiza un proceso de seguridad mediante TLS para verificar el certificado del sitio y establecer una conexión cifrada.

5. **El navegador envía una solicitud HTTP/HTTPS.**  
   El navegador funciona como **cliente** y envía un `request` al servidor. Por ejemplo, puede solicitar la página principal o la página correspondiente a un video. La solicitud incluye información como el método HTTP, la ruta solicitada y diferentes headers.

6. **El servidor recibe y procesa la solicitud.**  
   El servidor recibe el request y decide qué información debe devolver. En una plataforma como YouTube pueden intervenir diferentes servicios del backend para obtener datos del video, título, descripción, comentarios, recomendaciones y datos del usuario.

7. **El servidor devuelve una respuesta HTTP/HTTPS.**  
   El servidor envía un `response` que contiene un código de estado, headers y un cuerpo con información. Por ejemplo, un código `200 OK` indica que la solicitud fue procesada correctamente.

8. **El navegador construye la interfaz.**  
   El cliente recibe archivos e información necesarios para mostrar la página. Puede recibir HTML, CSS, JavaScript, imágenes y datos obtenidos mediante APIs.

9. **Se solicita el contenido del video.**  
   El video normalmente no se descarga como un único archivo completo. El navegador solicita fragmentos del contenido según la calidad seleccionada, la velocidad de la conexión y el punto de reproducción.

10. **El video aparece y comienza a reproducirse.**  
    Después de recibir suficiente información y algunos fragmentos iniciales del video, el navegador puede empezar la reproducción mientras continúa solicitando más datos al servidor.

### Flujo simplificado

```text
Usuario
  |
  v
Navegador / Cliente
  |
  | Consulta: ¿qué IP corresponde a www.youtube.com?
  v
DNS
  |
  | Responde con una dirección IP
  v
Navegador / Cliente
  |
  | HTTPS Request
  v
Servidor / CDN de YouTube
  |
  | HTTPS Response
  v
Navegador
  |
  v
Página y video en pantalla
```

En resumen, el **cliente** solicita información, el **DNS** permite encontrar la dirección IP del servidor, **HTTP/HTTPS** define cómo se intercambian las solicitudes y respuestas, y el **servidor** procesa la petición y devuelve la información necesaria.

---

## 2. Frontend y Backend en acción

Supongamos que se desarrolla una aplicación web para agendar citas médicas.

### Frontend

El **frontend** corresponde a todo lo que el usuario puede ver y utilizar directamente desde el navegador.

En esta aplicación incluiría, por ejemplo:

- Formulario para iniciar sesión.
- Lista de médicos y especialidades.
- Calendario con horarios disponibles.
- Formulario para reservar una cita.
- Pantalla para consultar o cancelar citas.
- Mensajes de confirmación o error.

Tres tecnologías que podrían utilizarse en el frontend son:

1. **HTML**: define la estructura de la página.
2. **CSS**: controla el diseño y la presentación visual.
3. **JavaScript**: permite agregar interacción y realizar solicitudes al backend.

También podrían utilizarse frameworks como React, Angular o Vue.

### Backend

El **backend** corresponde a la lógica que se ejecuta en el servidor y que normalmente no es visible directamente para el usuario.

Entre sus responsabilidades estarían:

- Consultar los médicos disponibles.
- Verificar si un horario sigue libre.
- Crear una nueva cita.
- Modificar o cancelar una cita.
- Validar datos enviados por el usuario.
- Consultar y modificar información en una base de datos.
- Aplicar reglas de negocio y permisos.

Tres tecnologías posibles para desarrollar el backend son:

1. **Node.js con Express**.
2. **Python con Django o Flask**.
3. **Java con Spring Boot**.

### Comunicación entre frontend y backend

El frontend puede comunicarse con el backend utilizando una **API**. La API publica endpoints que permiten realizar determinadas operaciones.

Por ejemplo, para consultar citas disponibles el frontend podría enviar:

```http
GET /api/citas/disponibles
```

Para crear una cita podría enviar:

```http
POST /api/citas
Content-Type: application/json
```

```json
{
  "pacienteId": 25,
  "medicoId": 8,
  "fecha": "2026-09-30",
  "hora": "10:30"
}
```

Este intercambio utiliza el protocolo **HTTP o HTTPS**. El frontend envía un **request** y el backend devuelve un **response**.

Ejemplo:

```text
Frontend
   |
   | HTTP Request
   v
API del Backend
   |
   | Procesa datos / consulta BD
   v
Base de datos
   |
   v
Backend
   |
   | HTTP Response
   v
Frontend
```

El response podría incluir un código de estado como `201 Created` y un objeto JSON con la información de la cita creada.

---

## 3. REST vs SOAP vs GraphQL

| Tipo de API | Formato de datos usado | Nivel de flexibilidad | Dificultad de implementación | Uso actual (Alta / Media / Baja) |
|---|---|---|---|---|
| REST | JSON / XML, principalmente JSON | Media | Baja / Media | Alta |
| SOAP | XML | Baja | Alta | Media |
| GraphQL | JSON | Alta | Media / Alta | Media / Alta |

### REST

REST trabaja normalmente con recursos identificados mediante URLs y utiliza métodos HTTP como `GET`, `POST`, `PUT`, `PATCH` y `DELETE`. Es sencillo de comprender y tiene una gran cantidad de herramientas y documentación disponibles.

### SOAP

SOAP utiliza mensajes XML y sigue reglas más estrictas. Puede utilizar contratos formales mediante WSDL y todavía se encuentra en sistemas empresariales donde se requieren integraciones muy estructuradas. Su configuración y mantenimiento suelen ser más complejos.

### GraphQL

GraphQL permite que el cliente indique exactamente qué campos necesita recibir. Esto ofrece una gran flexibilidad y puede reducir la cantidad de información innecesaria enviada por el servidor. Sin embargo, requiere más configuración y conocimiento que una API REST sencilla.

### ¿Cuál es más apropiada para una startup moderna? ¿Por qué?

Para una startup que desarrolla un sistema de reservas en línea elegiría inicialmente **REST**.

REST permite construir rápidamente endpoints claros para operaciones como consultar disponibilidad, crear reservas, modificarlas y cancelarlas. Además, funciona directamente con HTTP, normalmente utiliza JSON, cuenta con amplio soporte en frameworks y es fácil de probar con herramientas como Postman.

GraphQL también sería una buena opción si el sistema llegara a necesitar consultas muy flexibles o si existieran múltiples clientes con necesidades de datos diferentes. Sin embargo, para una primera versión del producto, REST suele ofrecer una implementación más sencilla y fácil de mantener.

---

## 4. Explorando APIs con Postman

### 4.1 Selección de la API

- **Nombre de la API:** JSONPlaceholder
- **URL base:** `https://jsonplaceholder.typicode.com`
- **Descripción:** JSONPlaceholder es una API REST pública y gratuita creada para realizar pruebas y prototipos. Ofrece recursos de ejemplo como posts, comentarios, usuarios, álbumes, fotografías y tareas. No requiere autenticación para utilizar sus endpoints.

Una característica importante es que las operaciones de escritura son **simuladas**. Las solicitudes `POST`, `PUT`, `PATCH` y `DELETE` responden como si el cambio se hubiera realizado, pero la información no queda modificada permanentemente en el servidor. Esto la hace apropiada para aprender a utilizar APIs sin alterar información real.

---

### 4.2 Configuración en Postman

- **Nombre de la colección:** `JSONPlaceholder`
- **Environment:** `JSONPlaceholder Environment`
- **Variable utilizada:** `base_url`
- **Valor de `base_url`:** `https://jsonplaceholder.typicode.com`

Las solicitudes utilizan la variable de esta manera:

```text
{{base_url}}/posts/1
```

#### Solicitudes agregadas

1. **GET - Obtener un post**
   - Método: `GET`
   - Endpoint: `{{base_url}}/posts/1`

2. **POST - Crear un post**
   - Método: `POST`
   - Endpoint: `{{base_url}}/posts`
   - Body:

```json
{
  "title": "Aprendiendo APIs con Postman",
  "body": "Esta publicación fue enviada desde una solicitud POST.",
  "userId": 1
}
```

3. **PUT - Actualizar un post**
   - Método: `PUT`
   - Endpoint: `{{base_url}}/posts/1`
   - Body:

```json
{
  "id": 1,
  "title": "Post actualizado desde Postman",
  "body": "El contenido del recurso fue reemplazado mediante PUT.",
  "userId": 1
}
```

4. **DELETE - Eliminar un post**
   - Método: `DELETE`
   - Endpoint: `{{base_url}}/posts/1`

No se requiere token de autenticación.

---

### 4.3 Ejecución y análisis

| Solicitud | Método | Endpoint | Código de estado esperado | Notas |
|---|---|---|---:|---|
| Obtener un post | GET | `/posts/1` | 200 | Devuelve el post con ID 1 en formato JSON. |
| Crear un post | POST | `/posts` | 201 | Simula la creación de un nuevo post y devuelve el recurso con un ID. |
| Actualizar un post | PUT | `/posts/1` | 200 | Simula el reemplazo del post con ID 1. |
| Eliminar un post | DELETE | `/posts/1` | 200 | Simula la eliminación y devuelve un objeto JSON vacío. |

Un header importante en las solicitudes que envían JSON es:

```http
Content-Type: application/json
```

En las respuestas también se puede observar un `Content-Type` relacionado con JSON.

Los códigos de estado permiten conocer rápidamente el resultado de una solicitud. Por ejemplo:

- `200 OK`: la solicitud se procesó correctamente.
- `201 Created`: un recurso fue creado correctamente.
- `404 Not Found`: el recurso solicitado no fue encontrado.
- `500 Internal Server Error`: ocurrió un error interno en el servidor.

Las respuestas de ejemplo se encuentran guardadas dentro de la colección exportada de Postman.

---

### 4.4 Explicación técnica

#### GET - Obtener un post

- **Método HTTP:** `GET`
- **Endpoint:** `{{base_url}}/posts/1`
- **Parámetros / body:** no requiere body.
- **Descripción de la respuesta:** devuelve el post cuyo identificador es `1`.

Ejemplo de respuesta:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

El método GET se utiliza cuando el cliente desea **consultar** información y no necesita modificar el recurso.

---

#### POST - Crear un post

- **Método HTTP:** `POST`
- **Endpoint:** `{{base_url}}/posts`
- **Parámetros / body:**

```json
{
  "title": "Aprendiendo APIs con Postman",
  "body": "Esta publicación fue enviada desde una solicitud POST.",
  "userId": 1
}
```

- **Descripción de la respuesta:** la API simula la creación del recurso y devuelve la información enviada junto con un nuevo identificador.

Ejemplo:

```json
{
  "title": "Aprendiendo APIs con Postman",
  "body": "Esta publicación fue enviada desde una solicitud POST.",
  "userId": 1,
  "id": 101
}
```

POST se utiliza principalmente para **crear nuevos recursos**.

---

#### PUT - Actualizar un post

- **Método HTTP:** `PUT`
- **Endpoint:** `{{base_url}}/posts/1`
- **Parámetros / body:**

```json
{
  "id": 1,
  "title": "Post actualizado desde Postman",
  "body": "El contenido del recurso fue reemplazado mediante PUT.",
  "userId": 1
}
```

- **Descripción de la respuesta:** devuelve una representación del recurso con los datos enviados en la actualización.

Ejemplo:

```json
{
  "id": 1,
  "title": "Post actualizado desde Postman",
  "body": "El contenido del recurso fue reemplazado mediante PUT.",
  "userId": 1
}
```

PUT se utiliza normalmente cuando se desea **reemplazar o actualizar completamente** un recurso existente.

---

#### DELETE - Eliminar un post

- **Método HTTP:** `DELETE`
- **Endpoint:** `{{base_url}}/posts/1`
- **Parámetros / body:** no requiere body.
- **Descripción de la respuesta:** JSONPlaceholder simula la eliminación del recurso y devuelve un objeto vacío.

Ejemplo:

```json
{}
```

DELETE representa la operación de **eliminar un recurso**.

### ¿Qué aprendí del proceso?

Con esta práctica aprendí que una API funciona como un punto de comunicación entre aplicaciones. Cada endpoint representa un recurso o una operación y los métodos HTTP indican qué acción desea realizar el cliente. También pude observar que una misma ruta puede comportarse de forma distinta dependiendo del método HTTP utilizado.

Además, comprendí mejor la importancia de elementos como los códigos de estado, los headers y el body. Postman permite ver cada una de estas partes por separado y hace más sencillo comprender exactamente qué información envía el cliente y qué devuelve el servidor.

---

### 4.5 Reflexión final

Esta actividad me permitió comprender que las APIs hacen posible que diferentes aplicaciones intercambien información utilizando reglas definidas. Una API REST puede exponer recursos mediante endpoints y utilizar métodos HTTP como GET, POST, PUT y DELETE para indicar la operación que se desea realizar. También entendí que el formato JSON es muy utilizado porque permite representar información de una manera estructurada y fácil de procesar tanto en frontend como en backend.

Postman me ayudó a visualizar de forma práctica la comunicación entre cliente y servidor. Al enviar cada request pude identificar el método HTTP, la URL, los headers y el body, y luego observar el código de estado y el contenido del response. Esto hace que conceptos que inicialmente pueden parecer teóricos, como request/response o códigos HTTP, sean más fáciles de comprender al verlos funcionando en una solicitud real.
