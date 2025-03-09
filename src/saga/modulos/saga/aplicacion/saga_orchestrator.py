import asyncio
from datetime import datetime
from uuid import uuid4
from saga.modulos.saga.aplicacion.manejador.anonimizador import ManejarAnominizacionEvento
from saga.modulos.saga.aplicacion.saga_state_repository import SagaStateRepository
from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
from saga.modulos.saga.infraestructura.schema.v1.comandos import ComandoCrearHsm, ComandoCrearTokenizacion, CrearHsmPayload, CrearTokenizacionPayload
from saga.seedwork.infraestructura.utils import unix_time_millis

# from saga.producers import publish_event


class SagaOrchestrator:
    def __init__(self):
        self.repo = SagaStateRepository()
        self.despachador = DespachadorComandos()

    async def manejador_anonimizacion_aprobada(self, datos: object):
        # Avanzar la saga
        self.repo.save_saga_state(datos.id_solicitud, step="TOKENIZATION_REQUESTED")
        # Enviar comando al servicio de tokenización
        topico = "TokenizacionCreada"
        evento_integracion = self.crear_comando_tokenizacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearTokenizacion)

    async def manejador_anonimizacion_rechazada(self, datos: object):
        # Iniciar compensación, o marcar saga como fallida
        self.repo.save_saga_state(datos.id_solicitud, step="ANONYMIZATION_FAILED")
        # No hay pasos previos en este ejemplo, pero si hubiera, haríamos "Compensate..."
        
    async def manejador_tokenizacion_aprobada(self, datos: object):
        # Avanzar la saga
        self.repo.save_saga_state(datos.id_solicitud, step="HSM_REQUESTED")
        # Enviar comando al servicio de tokenización
        topico = "HsmCreada" 
        evento_integracion = self.crear_comando_hsm(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearHsm)
        
    async def manejador_tokenizacion_rechazada(self, datos: object):
        # Iniciar compensación, o marcar saga como fallida
        self.repo.save_saga_state(datos.id_solicitud, step="HSM_FAILED")
        # No hay pasos previos en este ejemplo, pero si hubiera, haríamos "Compensate..."



    async def compensate(self, request_id: str):
        # Enviar comandos de compensación en orden inverso
        # ...
        pass


    def crear_comando_payload_tokenizacion(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearTokenizacionPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='CREADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_tokenizacion(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearTokenizacion(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_tokenizacion(evento)
        )
        
        
    def crear_comando_payload_hsm(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearHsmPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='CREADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_hsm(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearHsm(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_hsm(evento)
        )