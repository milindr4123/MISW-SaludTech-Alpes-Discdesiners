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
