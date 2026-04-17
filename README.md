# Sistema Cliente-Servidor en Python con SQLite

Este proyecto implementa un sistema **cliente-servidor TCP en Python**.  
El servidor acepta múltiples clientes de forma concurrente (multihilo), recibe mensajes de texto, los almacena en una base de datos SQLite junto con la fecha y la IP del cliente, y responde con una confirmación.

El cliente se conecta al servidor, envía mensajes y finaliza su ejecución cuando el usuario lo decide.

---

## Estructura del proyecto

```
.
├── servidor.py     # Servidor TCP multihilo con almacenamiento en SQLite
├── cliente.py      # Cliente TCP que envía mensajes al servidor
└── mensajes.db     # Base de datos SQLite (se crea automáticamente)
```

---

## Requisitos

- Python 3.8 o superior  
- No se requieren librerías externas (solo módulos estándar de Python)

---

## Ejecución del proyecto

### 1) Iniciar el servidor

```bash
python servidor.py
```

El servidor:

- Escucha conexiones en `127.0.0.1:5000`
- Inicializa automáticamente la base de datos `mensajes.db`
- Crea la tabla `mensajes` si no existe
- Acepta múltiples clientes simultáneamente mediante hilos

---

### 2) Ejecutar el cliente

```bash
python cliente.py
```

El cliente:

- Se conecta al servidor en `localhost:5000`
- Permite enviar múltiples mensajes
- Finaliza cuando el usuario escribe "éxito"

---

## Funcionamiento del servidor (`servidor.py`)

### Conectividad

- Usa sockets TCP/IP  
- Dirección: `127.0.0.1`  
- Puerto: `5000`

---

### Concurrencia

- Cada cliente se maneja en un hilo independiente  
- Se utiliza `threading.Lock` para proteger el acceso concurrente a la base de datos  

---

### Base de datos SQLite

- Archivo: `mensajes.db`  
- Tabla creada automáticamente:

```sql
CREATE TABLE mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    fecha_envio TEXT NOT NULL,
    ip_cliente TEXT NOT NULL
);
```

Cada mensaje guarda:

- Contenido del mensaje  
- Fecha y hora en formato ISO (UTC)  
- Dirección IP del cliente  

---

### Fechas

Se utiliza:

```python
datetime.now(datetime.timezone.utc)
```

Esto garantiza timestamps confiables y evita advertencias deprecadas.

---

### Respuesta del servidor

Por cada mensaje válido recibido, el servidor responde:

```
Mensaje recibido
```

Además, el servidor imprime en consola:

- Conexión del cliente  
- Mensajes recibidos  
- Cierre de conexiones  
- Errores (si ocurren)  

---

## Funcionamiento del cliente (`cliente.py`)

- Se conecta al servidor TCP especificado  
- Maneja errores de conexión (`ConnectionRefusedError`)  
- Finaliza correctamente si el servidor no está disponible  
- Permite enviar múltiples mensajes en una misma conexión  
- Finaliza cuando el usuario escribe "éxito"  

---

## Manejo de errores

### Servidor

- Control de excepciones en:
  - Inicialización de la base de datos  
  - Inserción de mensajes  
  - Manejo de clientes  
- Mensajes de error claros en consola  
- Notificación al cliente si falla la operación en la base de datos  

---

### Cliente

- Detecta servidor inactivo  
- Muestra mensajes de error sin bloquear la ejecución  

---

## Características principales

- Arquitectura cliente-servidor  
- Comunicación TCP/IP  
- Soporte multicliente (multihilo)  
- Persistencia con SQLite  
- Manejo de concurrencia seguro  
- Uso exclusivo de librerías estándar  

---

<<<<<<< HEAD
=======
## Capturas de pruebas
## Terminal cliente.py
<img width="886" height="305" alt="image" src="https://github.com/user-attachments/assets/dc2bf877-3e6f-402e-90cb-9f70608bc2f1" />

## Terminal servidor.py
<img width="886" height="272" alt="image" src="https://github.com/user-attachments/assets/bc76aa29-e73c-4ecd-a81b-85c8e42721ca" />

---

## Información académica

**Instituto de Formación Técnica Superior N° 29**  
Tecnicatura Superior en Desarrollo de Software
Daniel Cordoba - 3°A 
**Año 2026**
