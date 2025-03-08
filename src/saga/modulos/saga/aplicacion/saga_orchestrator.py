import asyncio
from datetime import datetime
from uuid import uuid4
from saga.modulos.saga.aplicacion.manejador.anonimizador import ManejarAnominizacionEvento
from saga.modulos.saga.aplicacion.saga_state_repository import SagaStateRepository
from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
from saga.modulos.saga.infraestructura.schema.v1.comandos import ComandoCrearTokenizacion, CrearTokenizacionPayload
from saga.seedwork.infraestructura.utils import unix_time_millis

# from saga.producers import publish_event


class SagaOrchestrator:
    def __init__(self):
        self.repo = SagaStateRepository()
        self.despachador = DespachadorComandos()

    # async def start_saga(self, request_id: str, data: dict):
        
    #     class EventoEjemplo:
    #         def __init__(self, id_solicitud, id_paciente, fecha_creacion, fecha_actualizacion, token_anonimo):
    #             self.id_solicitud = id_solicitud
    #             self.id_paciente = id_paciente
    #             self.fecha_creacion = fecha_creacion
    #             self.fecha_actualizacion = fecha_actualizacion
    #             self.estado = "CREADO"
    #             self.token_anonimo = token_anonimo
                
                
    #     # 1. Guardar estado inicial en la BD
    #     self.repo.save_saga_state(request_id, step="ANONYMIZATION_REQUESTED")

    #     # 2. Enviar comando al Anonimizado

    #     # Datos de ejemplo para el evento
    #     evento = EventoEjemplo(
    #         id_solicitud="12345",
    #         id_paciente="6789011",
    #         fecha_creacion=datetime.now(),
    #         fecha_actualizacion=datetime.now(),
    #         token_anonimo="abcde12345",
    #     )
    
    
    #     await ManejarAnominizacionEvento.enviar_mensaje_anonimizacion( "AnonimizacionCreada", evento)

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

    # Y así para cada paso (tokenización, hsm, validación, etc.)
    # handle_tokenization_succeeded(...)
    # handle_hsm_succeeded(...)
    # handle_validation_succeeded(...)
    # handle_*_failed(...)

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