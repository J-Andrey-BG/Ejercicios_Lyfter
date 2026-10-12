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

**¿Cuál es el problema?** El mismo automóvil aparece varias veces cuando tiene más de un propietario. Por ejemplo, el VIN `1HGCM82633A` está asociado tanto con Alice como con Bob. Entonces, **usar solamente el VIN como clave primaria no funcionaría** para identificar todas las filas de esta tabla.

**¿Y qué pasa con los seguros?** Aunque Alice y Bob están asociados con el mismo carro, aparecen con seguros diferentes. Por eso se considera que el seguro corresponde a la relación entre el automóvil y cada propietario. No se sabe si ambos son propietarios al mismo tiempo o en momentos diferentes, así que no se asume ninguna de esas dos situaciones.

### 1. Primera Forma Normal (1FN)

Para cumplir la **1FN**, se comprueba que las columnas tengan valores individuales y que cada fila cuente con una clave única. Los valores ya son atómicos. En este caso se utiliza la clave compuesta (`VIN`, `OwnerID`), bajo la suposición de que cada combinación de carro y propietario aparece una sola vez.

**Cars_1FN** — **PK:** (`VIN`, `OwnerID`)

| VIN **PK** | OwnerID **PK** | Make | Model | Year | Color | OwnerName | OwnerPhone | InsuranceCompany | InsurancePolicy |
|---|---|---|---|---:|---|---|---|---|---|
| 1HGCM82633A | 101 | Honda | Accord | 2003 | Silver | Alice | 123-456-7890 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | 102 | Honda | Accord | 2003 | Silver | Bob | 987-654-3210 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | 103 | Honda | CR-V | 2014 | Blue | Claire | 555-123-4567 | DEF Insurance | Collision |
| 1G1RA6EH1FU | 104 | Chevrolet | Volt | 2015 | Red | Dave | 111-222-3333 | GHI Insurance | Basic Legal |

**Ahora revisemos de qué depende cada dato:**

- `VIN → Make, Model, Year, Color`: características del vehículo.
- `OwnerID → OwnerName, OwnerPhone`: información del propietario.
- `(VIN, OwnerID) → InsuranceCompany, InsurancePolicy`: datos del seguro de esa asociación vehículo–propietario.

**¿Qué falta?** Aunque la tabla ya cumple 1FN, todavía presenta dependencias parciales. Las características del carro dependen de `VIN`, mientras que el nombre y teléfono del propietario dependen de `OwnerID`. No se necesitan ambas partes de la clave para conocer esos datos.

### 2. Segunda Forma Normal (2FN)

En **2FN** se separan esos datos. Se crea una tabla para los automóviles y otra para los propietarios. Como un carro puede tener varios propietarios y un propietario podría tener varios carros, se necesita una tercera tabla que los relacione. Esta es una relación **muchos a muchos (N:N)**.

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

| VIN **PK, FK** | OwnerID **PK, FK** | InsuranceCompany | InsurancePolicy |
|---|---|---|---|
| 1HGCM82633A | 101 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | 102 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | 103 | DEF Insurance | Collision |
| 1G1RA6EH1FU | 104 | GHI Insurance | Basic Legal |

**¿Qué mejora con esto?** Ya no se repiten las características del vehículo ni los datos personales del propietario cada vez que aparece una relación. En `CarOwners_2FN` se mantienen la compañía y la cobertura del seguro, porque en este ejercicio dependen de la combinación entre carro y propietario.

### 3. Tercera Forma Normal (3FN)

Para llegar a **3FN**, se revisa si todavía hay información que se pueda separar. Cada automóvil tiene un modelo y cada modelo pertenece a un fabricante. En lugar de repetir esos nombres en todos los carros, se pueden guardar fabricantes y modelos en sus propias tablas.

**Estas son las dependencias que se utilizan:**

- `VIN → ModelID, Year, Color`.
- `ModelID → MakeID, ModelName`.
- `MakeID → MakeName`.

Vamos a considerar que cada modelo pertenece a un fabricante. Como dos marcas podrían usar nombres de modelo iguales, es mejor identificar cada modelo con su propio código.

**Makes (Fabricantes)** — **PK:** `MakeID`; identificadores nuevos

| MakeID **PK** | MakeName |
|---|---|
| 1 | Honda |
| 2 | Chevrolet |

**Models (Modelos)** — **PK:** `ModelID`; **FK:** `MakeID → Makes`; identificadores nuevos

| ModelID **PK** | MakeID **FK** | ModelName |
|---|---|---|
| 1 | 1 | Accord |
| 2 | 1 | CR-V |
| 3 | 2 | Volt |

**Cars (Automóviles)** — **PK:** `VIN`; **FK:** `ModelID → Models`

| VIN **PK** | ModelID **FK** | Year | Color |
|---|---|---:|---|
| 1HGCM82633A | 1 | 2003 | Silver |
| 5J6RM4H79EL | 2 | 2014 | Blue |
| 1G1RA6EH1FU | 3 | 2015 | Red |

**Owners (Propietarios)** — **PK:** `OwnerID`

| OwnerID **PK** | OwnerName | OwnerPhone |
|---|---|---|
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |

**CarOwners (Relación entre automóviles y propietarios)** — **PK:** (`VIN`, `OwnerID`); **FK:** `VIN → Cars`, `OwnerID → Owners`

| VIN **PK, FK** | OwnerID **PK, FK** | InsuranceCompany | InsurancePolicy |
|---|---|---|---|
| 1HGCM82633A | 101 | ABC Insurance | Fire & Theft |
| 1HGCM82633A | 102 | XYZ Insurance | Full Cover |
| 5J6RM4H79EL | 103 | DEF Insurance | Collision |
| 1G1RA6EH1FU | 104 | GHI Insurance | Basic Legal |

**¿Por qué el resultado cumple 3FN?**

- `Makes` almacena cada fabricante una sola vez.
- `Models` relaciona cada modelo con su fabricante sin repetir el nombre de este último.
- `Cars` guarda el modelo mediante `ModelID` y solo los atributos que corresponden al vehículo individual.
- `Owners` conserva los datos de cada propietario bajo su identificador.
- `CarOwners` representa la relación **N:N** y mantiene los datos del seguro correspondientes a cada asociación.
- Bajo los supuestos establecidos, se eliminan las dependencias parciales y transitivas de las tablas finales.

**¿Por qué no se separan también los seguros?** Aquí `InsurancePolicy` muestra nombres de coberturas, no números únicos de póliza. Tampoco hay información suficiente para afirmar que cada compañía ofrece una sola cobertura o que cada cobertura pertenece a una única compañía. Por eso esos dos datos se mantienen en `CarOwners`. En un sistema más grande se podrían crear otras tablas, pero para este ejercicio no es necesario.

**Sobre los propietarios:** como la relación es N:N, la tabla `CarOwners` nos permite representar varios dueños por carro y varios carros por dueño. No agregamos fechas de propiedad porque no aparecen en los datos originales.

**¿Se perdió información?** No. Al relacionar `CarOwners`, `Cars`, `Owners`, `Models` y `Makes`, se pueden recuperar las cuatro filas originales, incluyendo los dos propietarios del VIN `1HGCM82633A` y sus seguros.

---

## Resumen de resultados

| Ejercicio | Tablas en 1FN | Tablas en 2FN | Tablas finales en 3FN |
|---|---|---|---|
| Orders | `Orders_1FN` | `Orders_2FN`, `Items_2FN`, `OrderItems_2FN` | `Customers`, `Addresses`, `Orders`, `Items`, `OrderItems` |
| Cars | `Cars_1FN` | `Cars_2FN`, `Owners_2FN`, `CarOwners_2FN` | `Makes`, `Models`, `Cars`, `Owners`, `CarOwners` |

**Para terminar:** con estos cambios, ambas tablas llegan a 3FN según las reglas y suposiciones explicadas. Se muestran todas las tablas intermedias sin perder los datos originales. En `Orders` se permiten varias direcciones dentro de un solo pedido y un pago único; en `Cars` se conserva la relación entre carros, propietarios y sus respectivos seguros.
