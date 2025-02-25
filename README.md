# MISW-SaludTech-Alpes-Discdesiners

Este proyecto implementa un sistema de **tokenización segura**, utilizando un **HSM (Hardware Security Module)** y **Apache Pulsar** para la comunicación asíncrona. La arquitectura sigue el modelo **hexagonal (puertos y adaptadores)**, lo que permite escalabilidad, disponibilidad y seguridad en el procesamiento de tokens.

## 📂 Estructura del Proyecto

El código está organizado siguiendo una **arquitectura hexagonal**, dividiendo la lógica en capas bien definidas:

- **`api/`**: Punto de entrada del microservicio, donde se exponen los endpoints mediante **API REST**.
- **`modulos/`**: Contiene los subdominios que representan la lógica del microservicio. Se organiza en:
  - **`aplicacion/`**: Implementa el patrón **CQRS**, dividiéndose en:
    - **`comando/`**: Manejo de operaciones de escritura.
    - **`queries/`**: Manejo de operaciones de lectura.
  - **`dominio/`**: Representa la lógica de negocio principal, incluyendo:
    - **Entidades**: Modelos centrales del dominio.
    - **Objetos de valor** (*Value Objects*): Elementos inmutables que encapsulan lógica.
    - **Fábricas**: Métodos para la creación de objetos de dominio.
    - **Repositorios**: Abstracción de acceso a datos.
    - **Servicios de dominio**: Contienen lógica de negocio compleja.
  - **`infraestructura/`**: Implementaciones técnicas como persistencia y comunicación con otros servicios. 
- **`seedwork/`**: Contiene clases base y componentes compartidos entre módulos.

## 🚀 Funcionamiento del Sistema

1. **Generación de Semilla**  
   - El **microservicio HSM** recibe una solicitud de semilla a través de un **endpoint REST**.  
   - La semilla se almacena de forma segura y se publica en **Pulsar**.  

2. **Recepción y Uso de la Semilla**  
   - El **microservicio Token** actúa como suscriptor de **Pulsar**, recibe la semilla y la usa para **generar y cifrar tokens**.  
   - Los tokens se almacenan en la base de datos y se usan para autenticación segura.  

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**  
- **Flask** (para la API REST)  
- **Apache Pulsar** (para eventos asíncronos)  
- **Docker & Docker Compose** (para contenedores)  
- **Arquitectura Hexagonal** (para modularidad y escalabilidad)  

## 📦 Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```sh
git clone https://github.com/tu-repo/misw-saludtech.git
cd misw-saludtech


## 📦 Video
Link: https://www.youtube.com/watch?v=-JxjhmCcgAQ

Repositorio:
Link: https://github.com/milindr4123/MISW-SaludTech-Alpes-Discdesiners


📌 Escenarios de Calidad Implementados

1️⃣ Disponibilidad - Recuperación ante fallo del servidor

Balanceador de carga con failover automático: Se implementa un balanceador de carga que redirige las solicitudes en caso de falla de un servidor.

Replicación de base de datos: Para asegurar la disponibilidad inmediata de los datos.

Medición: Tiempo de conmutación menor a 5 segundos con un 99.9% de disponibilidad.

2️⃣ Disponibilidad - Mantenimiento sin afectar el servicio

Despliegue en Azul/Verde: Se utiliza este enfoque para garantizar continuidad.

Base de datos en modo lectura/escritura con failover automático: Permite que el sistema siga funcionando durante la actualización.

Medición: Disponibilidad del 99.95% durante el mantenimiento.

3️⃣ Disponibilidad - Aumento de carga repentina

Escalado automático horizontal: Implementado en servidores de aplicación.

Cache en capa de datos (Redis/Memcached): Para reducir la carga en la base de datos.

Medición: Tiempo de respuesta menor a 2 segundos en el 99% de las solicitudes.

4️⃣ Escalabilidad - Ingesta de datos médicos

Procesamiento distribuido de datos: Permite manejar grandes volúmenes de información.

Balanceo de carga en ingesta y procesamiento: Se optimiza el flujo de datos.

Medición: Latencia menor a 5 minutos por lote de 500 GB.

5️⃣ Escalabilidad - Distribución de datos a clientes

Bases de datos distribuidas con caching (Redis, DynamoDB): Mejora los tiempos de respuesta.

Uso de API Gateway con balanceo de carga: Optimiza la entrega de datos concurrentes.

Medición: Tiempo de respuesta menor a 2 segundos por solicitud.