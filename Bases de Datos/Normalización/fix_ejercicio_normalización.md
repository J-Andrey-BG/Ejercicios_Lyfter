# Ejercicios de normalización de bases de datos

Vamos a normalizar las tablas **Orders** y **Cars** hasta llegar a la **Tercera Forma Normal (3FN)**. La idea es ir paso a paso: primero se identifican los problemas de cada tabla, después se hacen los cambios necesarios y se muestra cómo va quedando la información en cada forma normal.

**Antes de empezar:** se utiliza **PK** para clave primaria y **FK** para clave foránea. Los códigos de pedido se dejan como texto para no perder los ceros iniciales, y los precios se muestran como números decimales. Cuando sea necesario crear identificadores nuevos, se indicará. También se aclararán las suposiciones realizadas, porque unas cuantas filas no siempre bastan para conocer todas las reglas del sistema.

---

## Ejercicio 1: Orders (Pedidos)

### 0. Tabla original

| Order ID | Customer Name | Customer Phone | Address | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
|---|---|---|---|---|---|---|---:|---|---|
| 001 | Alice | 123-456-7890 | 123 Main St | 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | Alice | 123-456-7890 | 123 Main St | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | Bob | 987-654-3210 | 4th Avenue | 102 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | Claire | 555-123-4567 | 789 Oak St | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | Claire | 555-123-4567 | 464 Georgia St | 106 | Water | $1 | 1 | None | 5:00 PM |

**¿Qué se observa aquí?** Hay bastantes datos repetidos. Por ejemplo, Alice aparece dos veces porque pidió dos productos, y las papas tienen el mismo nombre y precio en diferentes pedidos. Si un dato cambia, habría que corregirlo en varias filas, y es fácil que alguna quede desactualizada.

**¿Y qué pasa con las dos direcciones de la orden `002`?** Para este ejercicio se permite que un mismo pedido tenga varias direcciones de entrega. Así, Bob puede pagar **una sola vez por toda la orden**, aunque la pizza vaya a `456 Elm St` y las papas a `4th Avenue`. De esta manera no es necesario borrar ni cambiar ninguno de los datos originales.

Esto quiere decir que **`OrderID` por sí solo no determina cuál es la dirección** (`OrderID ↛ Address`). Para saber a dónde va cada producto, se debe revisar la línea del pedido: (`OrderID`, `ItemID`). El pago, en cambio, pertenece al pedido completo. Como no se proporcionan datos sobre montos pagados, métodos de pago o transacciones, no se agregan datos inventados ni se crea una tabla `Payments`.

### 1. Primera Forma Normal (1FN)

En la **1FN**, lo primero es revisar que cada columna guarde un solo valor y que cada fila pueda identificarse de manera única. Aquí los datos ya son atómicos, así que no hace falta dividir ninguna columna. Se utiliza (`OrderID`, `ItemID`) como **clave primaria compuesta**. Esto funciona bajo la suposición de que un producto aparece una sola vez dentro de cada pedido.

**Orders_1FN** — **PK:** (`OrderID`, `ItemID`)

| OrderID **PK** | ItemID **PK** | CustomerName | CustomerPhone | Address | ItemName | Price | Quantity | SpecialRequest | DeliveryTime |
|---|---|---|---|---|---|---:|---:|---|---|
| 001 | 101 | Alice | 123-456-7890 | 123 Main St | Cheeseburger | 8.00 | 2 | No onions | 6:00 PM |
| 001 | 102 | Alice | 123-456-7890 | 123 Main St | Fries | 3.00 | 1 | Extra ketchup | 6:00 PM |
| 002 | 103 | Bob | 987-654-3210 | 456 Elm St | Pizza | 12.00 | 1 | Extra cheese | 7:30 PM |
| 002 | 102 | Bob | 987-654-3210 | 4th Avenue | Fries | 3.00 | 2 | None | 7:30 PM |
| 003 | 105 | Claire | 555-123-4567 | 789 Oak St | Salad | 6.00 | 1 | No croutons | 12:00 PM |
| 004 | 106 | Claire | 555-123-4567 | 464 Georgia St | Water | 1.00 | 1 | None | 5:00 PM |

**Ahora revisemos de qué depende cada dato:**

- `OrderID → CustomerName, CustomerPhone, DeliveryTime`: el pedido determina quién lo realiza y su hora de entrega.
- `ItemID → ItemName, Price`: se considera que el precio es el precio registrado del producto en el catálogo.
- `(OrderID, ItemID) → Quantity, SpecialRequest, Address`: los datos corresponden a una línea concreta del pedido, que puede tener su propio destino.
- Aunque los nombres de los clientes no se repiten entre personas en la muestra, `CustomerName` no es un identificador fiable; más adelante se incorpora `CustomerID`.

**¿Ya está lista?** Todavía no. Aunque la tabla cumple 1FN, tiene dependencias parciales: `ItemName` depende únicamente de `ItemID`, y `DeliveryTime` depende únicamente de `OrderID`. Por eso se continúa con 2FN.

### 2. Segunda Forma Normal (2FN)

En la **2FN** se busca eliminar las dependencias parciales. Dicho de forma sencilla: si un dato depende solo de una parte de la clave compuesta, no debería seguir en esta tabla. Por eso se separa la información del pedido, la del producto y la que corresponde a cada producto dentro del pedido.

**Orders_2FN** — **PK:** `OrderID`

| OrderID **PK** | CustomerName | CustomerPhone | DeliveryTime |
|---|---|---|---|
| 001 | Alice | 123-456-7890 | 6:00 PM |
| 002 | Bob | 987-654-3210 | 7:30 PM |
| 003 | Claire | 555-123-4567 | 12:00 PM |
| 004 | Claire | 555-123-4567 | 5:00 PM |

**Items_2FN** — **PK:** `ItemID`

| ItemID **PK** | ItemName | Price |
|---|---|---:|
| 101 | Cheeseburger | 8.00 |
| 102 | Fries | 3.00 |
| 103 | Pizza | 12.00 |
| 105 | Salad | 6.00 |
| 106 | Water | 1.00 |

**OrderItems_2FN** — **PK:** (`OrderID`, `ItemID`); **FK:** `OrderID → Orders_2FN`, `ItemID → Items_2FN`

| OrderID **PK, FK** | ItemID **PK, FK** | Quantity | SpecialRequest | Address |
|---|---|---:|---|---|
| 001 | 101 | 2 | No onions | 123 Main St |
| 001 | 102 | 1 | Extra ketchup | 123 Main St |
| 002 | 103 | 1 | Extra cheese | 456 Elm St |
| 002 | 102 | 2 | None | 4th Avenue |
| 003 | 105 | 1 | No croutons | 789 Oak St |
| 004 | 106 | 1 | None | 464 Georgia St |

**¿Qué se consigue con esto?** Ahora los datos generales del pedido están en `Orders_2FN`, los productos están en `Items_2FN` y las cantidades, solicitudes y direcciones quedan en `OrderItems_2FN`. En esta última tabla, los datos dependen de la clave completa (`OrderID`, `ItemID`). Todavía aparecen algunos datos repetidos, como la información de Claire y ciertas direcciones, así que falta un paso más.

### 3. Tercera Forma Normal (3FN)

En la **3FN** se revisa si hay información que depende de otro dato en lugar de depender directamente de la clave de su tabla. Por ejemplo, los datos del cliente no necesitan estar repetidos en cada pedido. También conviene guardar las direcciones por separado. Así cada tabla tendrá una responsabilidad más clara.

**Vamos a hacer estos cambios:**

1. Se crean `CustomerID` para identificar a los clientes, porque el nombre no sirve como identificador único confiable.
2. Se crea `AddressID` para identificar cada dirección y `CustomerID` como clave foránea para registrar a qué cliente pertenece.
3. `Orders` conserva **una fila por pedido**, con un único cliente y una hora de entrega indicada en los datos originales.
4. `OrderItems` utiliza `AddressID` para indicar el destino de cada producto; así, dos productos de una misma orden pueden enviarse a direcciones diferentes.
5. El pago se considera **único por orden**, incluso cuando existen varios destinos. No se almacena un pago por línea ni por dirección.

Los códigos `C001`, `C002`, `C003` y los números del `1` al `5` para las direcciones los agregamos nosotros. No estaban en la tabla original, pero nos sirven para relacionar las tablas sin depender de nombres o direcciones escritas como texto.

**Customers (Clientes)** — **PK:** `CustomerID`

| CustomerID **PK** | CustomerName | CustomerPhone |
|---|---|---|
| C001 | Alice | 123-456-7890 |
| C002 | Bob | 987-654-3210 |
| C003 | Claire | 555-123-4567 |

**Addresses (Direcciones)** — **PK:** `AddressID`; **FK:** `CustomerID → Customers`

| AddressID **PK** | CustomerID **FK** | Address |
|---|---|---|
| 1 | C001 | 123 Main St |
| 2 | C002 | 456 Elm St |
| 3 | C002 | 4th Avenue |
| 4 | C003 | 789 Oak St |
| 5 | C003 | 464 Georgia St |

**Orders (Pedidos)** — **PK:** `OrderID`; **FK:** `CustomerID → Customers`

| OrderID **PK** | CustomerID **FK** | DeliveryTime |
|---|---|---|
| 001 | C001 | 6:00 PM |
| 002 | C002 | 7:30 PM |
| 003 | C003 | 12:00 PM |
| 004 | C003 | 5:00 PM |

**Items (Productos)** — **PK:** `ItemID`

| ItemID **PK** | ItemName | Price |
|---|---|---:|
| 101 | Cheeseburger | 8.00 |
| 102 | Fries | 3.00 |
| 103 | Pizza | 12.00 |
| 105 | Salad | 6.00 |
| 106 | Water | 1.00 |

**OrderItems (Detalles del pedido)** — **PK:** (`OrderID`, `ItemID`); **FK:** `OrderID → Orders`, `ItemID → Items`, `AddressID → Addresses`

| OrderID **PK, FK** | ItemID **PK, FK** | Quantity | SpecialRequest | AddressID **FK** |
|---|---|---:|---|---|
| 001 | 101 | 2 | No onions | 1 |
| 001 | 102 | 1 | Extra ketchup | 1 |
| 002 | 103 | 1 | Extra cheese | 2 |
| 002 | 102 | 2 | None | 3 |
| 003 | 105 | 1 | No croutons | 4 |
| 004 | 106 | 1 | None | 5 |

**¿Por qué esta separación funciona?**

- `Customers` almacena los atributos de cada cliente una sola vez: `CustomerID → CustomerName, CustomerPhone`.
- `Addresses` registra cada dirección con su identificador: `AddressID → CustomerID, Address`. Un cliente puede registrar varias direcciones (**relación 1:N**).
- `Orders` identifica un pedido y su cliente: `OrderID → CustomerID, DeliveryTime`. Un cliente puede tener varias órdenes (**relación 1:N**).
- `Items` contiene los atributos propios de cada producto: `ItemID → ItemName, Price`.
- `OrderItems` resuelve la relación **muchos a muchos (N:N)** entre pedidos y productos. `Quantity`, `SpecialRequest` y `AddressID` dependen de la línea identificada por (`OrderID`, `ItemID`). No se repiten los datos descriptivos de la dirección en cada línea.
- Bajo las dependencias asumidas, cada atributo no clave depende de su clave correspondiente, sin dependencias parciales o transitivas en las tablas finales.

**El pedido `002` permite comprobar cómo funciona:**

| OrderID | Cliente | Producto | Cantidad | Dirección de entrega |
|---|---|---|---:|---|
| 002 | Bob | Pizza | 1 | 456 Elm St |
| 002 | Bob | Fries | 2 | 4th Avenue |

Ambas filas tienen el **mismo `OrderID`**. Es un solo pedido y, por lo tanto, puede hacerse un solo pago, aunque tenga dos destinos distintos. Si más adelante fuera necesario registrar los pagos, se podría agregar una tabla `Payments` relacionada con `Orders` y establecer un pago por pedido. Por ahora no hace falta porque esos datos no aparecen en el ejercicio.

**Algunos detalles que conviene tener presentes:**

- Para impedir que una línea de un pedido utilice por error la dirección de otro cliente, el sistema debe verificar que `Orders.CustomerID` coincida con `Addresses.CustomerID`. Las claves foráneas descritas por sí solas no garantizan esa coincidencia; se puede reforzar mediante una restricción compuesta o validación en la aplicación.
- La hora `DeliveryTime` se mantiene en `Orders` porque las líneas de cada pedido comparten la misma hora en los datos proporcionados. Si cada destino pudiera tener horarios diferentes, se necesitaría registrar el horario por entrega o línea.
- Se asume que cada producto aparece como máximo una vez por pedido. Si pudiera aparecer dos veces como líneas distintas (por ejemplo, el mismo producto con dos direcciones), se necesitaría `OrderItemID` o un número de línea como identificador, en vez de (`OrderID`, `ItemID`).
- Se toma `Price` como precio del catálogo. En una aplicación real normalmente también se conserva el precio efectivamente cobrado en el detalle, pero el enunciado no proporciona esa distinción.
- Un pago único no implica necesariamente un único envío físico ni un único costo de entrega: esas operaciones podrían modelarse por separado si existieran más requisitos.

---

## Ejercicio 2: Cars (Automóviles)

### 0. Tabla original

| VIN | Make | Model | Year | Color | Owner ID | Owner Name | Owner Phone | Insurance Company | Insurance Policy |
|---|---|---|---:|---|---|---|---|---|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 101 | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 102 | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue | 103 | Claire | 555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red | 104 | Dave | 111-222-3333 | GHI Insurance | Basic Legal |

**¿Qué problemas aparecen?** El mismo VIN se repite cuando hay más de un propietario, también se repiten las características del vehículo y los datos de cada persona. Además, los seguros están mezclados con los propietarios, aunque se desea que las pólizas se relacionen con **el vehículo**, no con una persona.

Hay un caso que merece atención: el VIN `1HGCM82633A` aparece con **dos propietarios y dos coberturas distintas**. Los datos no indican fechas ni cuál es el seguro vigente. En esta solución se registran las dos coberturas como asociaciones del automóvil. Así no se descarta ninguna, pero tampoco se inventa una fecha o se afirma que una reemplazó a la otra.

También se considera que `Year` es el **año de la versión del modelo**. Por ejemplo, el Accord 2003 se trata como una versión del modelo y no como una característica que deba escribirse nuevamente para cada VIN. En un sistema real también podría distinguirse entre año del modelo y año de fabricación, pero el ejercicio solo incluye un campo `Year`.

### 1. Primera Forma Normal (1FN)

En la **1FN**, cada celda debe contener un solo valor y las filas tienen que poder identificarse de forma única. Los datos originales ya son atómicos. Para esta primera etapa se utiliza la combinación (`VIN`, `OwnerID`) como clave primaria, porque identifica las cuatro filas proporcionadas.

**Cars_1FN** — **PK:** (`VIN`, `OwnerID`)

| VIN **PK** | OwnerID **PK** | Make | Model | Year | Color | OwnerName | OwnerPhone | InsuranceCompany | InsurancePolicy |
|---|---|---|---|---:|---|---|---|---|---|
| 1HGCM82633A | 101 | Honda | Accord | 2003 | Silver | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | 102 | Honda | Accord | 2003 | Silver | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | 103 | Honda | CR-V | 2014 | Blue | Claire | 555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU | 104 | Chevrolet | Volt | 2015 | Red | Dave | 111-222-3333 | GHI Insurance | Basic Legal |

**¿Qué dependencias se pueden identificar?**

- `VIN → Make, Model, Year, Color`: las características del automóvil se identifican por su VIN en la tabla original.
- `OwnerID → OwnerName, OwnerPhone`: los datos personales dependen del identificador del propietario.
- Los nombres de aseguradoras y coberturas están incluidos en filas de propietarios, pero **no se asumirá que dependen del propietario**. La asociación correcta para este ejercicio es la del seguro con el vehículo.

La clave está formada por dos columnas y varios atributos dependen solamente de una de ellas. Por eso todavía no se cumple la 2FN.

### 2. Segunda Forma Normal (2FN)

La **2FN** busca eliminar las dependencias parciales. Por eso se separan los automóviles y los propietarios. Después se crea una tabla intermedia para relacionarlos, ya que un automóvil puede tener varios propietarios y una persona puede tener varios automóviles.

Los seguros también se separan desde esta etapa. En lugar de vincularlos a `CarOwners`, se guardan en una tabla de seguros asociados al **VIN**. Se agrega un identificador para distinguir cada registro de seguro, porque un mismo vehículo puede tener más de uno.

**Cars_2FN** — **PK:** `VIN`

| VIN **PK** | Make | Model | Year | Color |
|---|---|---|---:|---|
| 1HGCM82633A | Honda | Accord | 2003 | Silver |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red |

**Owners_2FN** — **PK:** `OwnerID`

| OwnerID **PK** | OwnerName | OwnerPhone |
|---|---|---|
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |

**CarOwners_2FN** — **PK:** (`VIN`, `OwnerID`); **FK:** `VIN → Cars_2FN`, `OwnerID → Owners_2FN`

| VIN **PK, FK** | OwnerID **PK, FK** |
|---|---|
| 1HGCM82633A | 101 |
| 1HGCM82633A | 102 |
| 5J6RM4H79EL | 103 |
| 1G1RA6EH1FU | 104 |

**CarInsurances_2FN** — **PK:** `CarInsuranceID`; **FK:** `VIN → Cars_2FN`. `CarInsuranceID` es nuevo.

| CarInsuranceID **PK** | VIN **FK** | InsuranceCompany | InsurancePolicy |
|---|---|---|---|
| 1 | 1HGCM82633A | ABC Insurance | Fire & Theft |
| 2 | 1HGCM82633A | XYZ Insurance | Full Cover |
| 3 | 5J6RM4H79EL | DEF Insurance | Collision |
| 4 | 1G1RA6EH1FU | GHI Insurance | Basic Legal |

**¿Qué mejoró?** Las características de los vehículos aparecen una sola vez por VIN y los datos personales aparecen una sola vez por propietario. `CarOwners_2FN` ya no almacena seguros: únicamente representa quién está asociado con cada automóvil. Además, `CarInsurances_2FN` permite que un VIN tenga varios registros de cobertura sin asignárselos a una persona específica.

Todavía se escriben las marcas, los modelos y los nombres de los seguros directamente como texto. En la 3FN se separa esa información para evitar repeticiones y facilitar las actualizaciones.

### 3. Tercera Forma Normal (3FN)

En la **3FN**, la idea es que los atributos descriptivos estén en la tabla de la entidad a la que realmente pertenecen. Si se puede obtener un dato a través de otro atributo que no es la clave, es necesario revisar si conviene separarlo.

En este caso se realizan tres ajustes principales:

1. **Separar fabricantes, modelos y vehículos.** El nombre del fabricante pertenece a `Makes`; el nombre y el año de la versión del modelo pertenecen a `Models`. `Cars` conserva el VIN, una referencia al modelo y el color individual del vehículo.
2. **Separar aseguradoras y pólizas.** Las compañías se identifican mediante `InsuranceCompanyID`. Cada tipo de cobertura ofrecido por una compañía se registra una sola vez en `InsurancePolicies`, evitando repetir el texto completo por cada automóvil asegurado.
3. **Asociar las pólizas directamente a los vehículos.** `CarOwners` solo relaciona personas y autos. La tabla `CarInsurances` relaciona cada VIN con las pólizas que aparecen en los datos.

Para este ejercicio, `InsurancePolicy` se interpreta como el **nombre de un tipo de cobertura** (por ejemplo, `Full Cover`), no como un número de contrato individual. Se supone que una compañía puede ofrecer varios tipos de cobertura. Por eso no se utiliza la dependencia `InsuranceCompany → InsurancePolicy`: saber la compañía no necesariamente determina una única póliza.

#### Tabla 1. Makes (Fabricantes)

**PK:** `MakeID` (identificador nuevo)

| MakeID **PK** | MakeName |
|---|---|
| 1 | Honda |
| 2 | Chevrolet |

#### Tabla 2. Models (Modelos)

**PK:** `ModelID`; **FK:** `MakeID → Makes`. Cada fila representa una versión identificada por fabricante, nombre y año.

| ModelID **PK** | MakeID **FK** | ModelName | Year |
|---|---|---|---:|
| 1 | 1 | Accord | 2003 |
| 2 | 1 | CR-V | 2014 |
| 3 | 2 | Volt | 2015 |

De esta manera, si existieran varios vehículos Honda Accord del año 2003, todos podrían apuntar al mismo `ModelID` sin repetir esos datos.

#### Tabla 3. Cars (Automóviles)

**PK:** `VIN`; **FK:** `ModelID → Models`

| VIN **PK** | ModelID **FK** | Color |
|---|---|---|
| 1HGCM82633A | 1 | Silver |
| 5J6RM4H79EL | 2 | Blue |
| 1G1RA6EH1FU | 3 | Red |

Ahora `Cars` contiene únicamente el identificador del vehículo, la referencia a su versión de modelo y un atributo propio del automóvil: su color.

#### Tabla 4. Owners (Propietarios)

**PK:** `OwnerID`

| OwnerID **PK** | OwnerName | OwnerPhone |
|---|---|---|
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |

#### Tabla 5. CarOwners (Automóviles y propietarios)

**PK:** (`VIN`, `OwnerID`); **FK:** `VIN → Cars`, `OwnerID → Owners`

| VIN **PK, FK** | OwnerID **PK, FK** |
|---|---|
| 1HGCM82633A | 101 |
| 1HGCM82633A | 102 |
| 5J6RM4H79EL | 103 |
| 1G1RA6EH1FU | 104 |

La relación es **muchos a muchos (N:N)** y ya no hay información sobre seguros en esta tabla.

#### Tabla 6. InsuranceCompanies (Aseguradoras)

**PK:** `InsuranceCompanyID` (identificador nuevo)

| InsuranceCompanyID **PK** | CompanyName |
|---|---|
| 1 | ABC Insurance |
| 2 | XYZ Insurance |
| 3 | DEF Insurance |
| 4 | GHI Insurance |

Si una misma compañía asegura 500 automóviles, su nombre sigue apareciendo solamente una vez en `InsuranceCompanies`.

#### Tabla 7. InsurancePolicies (Tipos de póliza)

**PK:** `PolicyID`; **FK:** `InsuranceCompanyID → InsuranceCompanies`. Cada registro representa una cobertura ofrecida por una compañía específica.

| PolicyID **PK** | InsuranceCompanyID **FK** | PolicyName |
|---|---|---|
| 1 | 1 | Fire & Theft |
| 2 | 2 | Full Cover |
| 3 | 3 | Collision |
| 4 | 4 | Basic Legal |

Por ejemplo, la cobertura `Full Cover` de `XYZ Insurance` se registra una sola vez, aunque se utilice para muchos vehículos. Si otra compañía también ofrece una cobertura llamada `Full Cover`, puede tener otro `PolicyID`, porque son productos de aseguradoras diferentes.

#### Tabla 8. CarInsurances (Seguros de vehículos)

**PK:** (`VIN`, `PolicyID`); **FK:** `VIN → Cars`, `PolicyID → InsurancePolicies`

| VIN **PK, FK** | PolicyID **PK, FK** |
|---|---|
| 1HGCM82633A | 1 |
| 1HGCM82633A | 2 |
| 5J6RM4H79EL | 3 |
| 1G1RA6EH1FU | 4 |

Esta tabla resuelve la relación **muchos a muchos (N:N)** entre vehículos y tipos de póliza. Un vehículo puede aparecer con varias coberturas y una misma cobertura puede estar asociada a muchos vehículos sin duplicar el nombre del seguro.

### 4. Comprobación del resultado

**¿Por qué estas tablas cumplen con la 3FN bajo el modelo elegido?**

- `Makes` guarda el nombre de cada fabricante asociado a `MakeID`.
- `Models` guarda la versión del modelo, su año y la referencia al fabricante. Esos atributos corresponden a `ModelID`.
- `Cars` contiene datos determinados por el VIN, sin repetir los nombres del fabricante ni del modelo.
- `Owners` conserva los atributos de cada propietario en una sola fila.
- `CarOwners` contiene únicamente las claves que forman la relación entre propietarios y automóviles.
- `InsuranceCompanies` registra cada compañía por separado, de modo que los cambios de nombre no requieren modificar cientos de vehículos.
- `InsurancePolicies` identifica cada tipo de cobertura ofrecido por una aseguradora.
- `CarInsurances` enlaza vehículos con pólizas mediante sus identificadores, sin repetir los textos de compañía y cobertura.

**Un detalle sobre los datos originales:** inicialmente, la primera fila asocia a Alice con `ABC Insurance` y la segunda asocia a Bob con `XYZ Insurance`. En el diseño solicitado, esos seguros se relacionan **solo con el vehículo**. Por lo tanto, se conservan los propietarios y las dos coberturas, pero **ya no se puede reconstruir qué propietario estaba junto a qué seguro en cada fila original**. Esta pérdida de asociación es consecuencia de la nueva regla del negocio y no se debe ocultar. Para conservar ese historial haría falta información adicional, como fechas o registros históricos de contratación; no se inventa porque el enunciado no la proporciona.

Tampoco se puede saber con los datos disponibles si las dos coberturas del mismo VIN estaban vigentes al mismo tiempo. Aquí se guardan las dos asociaciones, sin afirmar cuál está vigente.

---

## Resumen de resultados

| Ejercicio | Tablas en 1FN | Tablas en 2FN | Tablas finales en 3FN |
|---|---|---|---|
| Orders | `Orders_1FN` | `Orders_2FN`, `Items_2FN`, `OrderItems_2FN` | `Customers`, `Addresses`, `Orders`, `Items`, `OrderItems` |
| Cars | `Cars_1FN` | `Cars_2FN`, `Owners_2FN`, `CarOwners_2FN`, `CarInsurances_2FN` | `Makes`, `Models`, `Cars`, `Owners`, `CarOwners`, `InsuranceCompanies`, `InsurancePolicies`, `CarInsurances` |

**Para terminar:** con estos cambios, ambas tablas llegan a 3FN según las reglas y suposiciones explicadas, y se muestran las tablas intermedias. En `Orders` se permiten varias direcciones dentro de un solo pedido y un pago único. En `Cars`, los propietarios y las coberturas se relacionan por separado con cada vehículo. Los valores originales se conservan, aunque la asociación original entre una persona y un seguro concreto ya no puede reconstruirse sin datos adicionales.
