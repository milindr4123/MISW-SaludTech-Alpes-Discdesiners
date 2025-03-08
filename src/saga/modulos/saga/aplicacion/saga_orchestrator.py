import asyncio
import datetime
from saga.modulos.saga.aplicacion.manejador.anonimizador import ManejarAnominizacionEvento
from saga.modulos.saga.aplicacion.saga_state_repository import SagaStateRepository

# from saga.producers import publish_event


class SagaOrchestrator:
    def __init__(self):
        self.repo = SagaStateRepository()

    async def start_saga(self, request_id: str, data: dict):
        # 1. Guardar estado inicial en la BD
        self.repo.save_saga_state(request_id, step="ANONYMIZATION_REQUESTED")

        # 2. Enviar comando al Anonimizador
        cmd = {
            "request_id": request_id,
            "payload": data
        }
        
        class EventoEjemplo:
            def __init__(self, id_solicitud, id_paciente, fecha_creacion, fecha_actualizacion, token_anonimo):
                self.id_solicitud = id_solicitud
                self.id_paciente = id_paciente
                self.fecha_creacion = fecha_creacion
                self.fecha_actualizacion = fecha_actualizacion
                self.estado = "CREADO"
                self.token_anonimo = token_anonimo

        # Datos de ejemplo para el evento
        evento = EventoEjemplo(
            id_solicitud="12345",
            id_paciente="6789011",
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            token_anonimo="abcde12345",
        )
    
    
        await ManejarAnominizacionEvento.enviar_mensaje_anonimizacion( "AnonimizacionCreada", evento)

    async def handle_anonymization_succeeded(self, request_id: str):
        # Avanzar la saga
        self.repo.update_saga_step(request_id, step="TOKENIZATION_REQUESTED")
        # Enviar comando al servicio de tokenización
        cmd = {"request_id": request_id, "payload": {}}
        # await publish_command("tokenizacion-comandos", "TokenizationRequested", cmd)

    async def handle_anonymization_failed(self, request_id: str):
        # Iniciar compensación, o marcar saga como fallida
        self.repo.update_saga_step(request_id, step="ANONYMIZATION_FAILED")
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
