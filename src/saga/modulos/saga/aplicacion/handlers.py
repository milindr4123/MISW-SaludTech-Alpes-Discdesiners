from datetime import datetime
from uuid import uuid4
from saga.modulos.saga.aplicacion.saga_state_repository import SagaStateRepository
from saga.modulos.saga.infraestructura.schema.v1.comandos import CrearAnonimizacionPayload, ComandoCrearAnonimizacion
from saga.modulos.saga.dominio.eventos import (
    AnonimizationSucceeded,
    TokenizationFailed
)
from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
from saga.seedwork.infraestructura.utils import unix_time_millis

class SagaHandler:
    def __init__(self, app=None):
        self.despachador = DespachadorComandos()
        self.repo = SagaStateRepository(app)

    def crear_comando_payload(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearAnonimizacionPayload(
            id_solicitud=str(datos["id_solicitud"]), 
            id_paciente=str(datos["id_paciente"]), 
            token_anonimo=str(datos["token_anonimo"]),
            estado='CREADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearAnonimizacion(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload(evento)
        )
    
    async def iniciar_saga(self, datos):
        try:
            # Paso 1: Anonimizar EventoAnonimizacionCreado publicar_mensaje(self, mensaje, topico, schema):
            self.repo.save_saga_state(str(datos["id_solicitud"]), step="ANONYMIZATION_REQUESTED")
            topico = "AnonimizacionCreada"
            
            
            evento_integracion = self.crear_comando(datos)
            self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearAnonimizacion)
            # self.despachador.enviar_comando("anonimizacion", "AnonymizeImageCommand", datos)
            # ... lógica para escuchar eventos de respuesta ...
        except Exception as e:
            print(e)
            self.compensar_saga(datos)

    def compensar_saga(self, datos):
        # Ejecutar compensaciones en orden inverso
        self.despachador.enviar_comando("validacion", "CompensateValidation", datos)
        self.despachador.enviar_comando("hsm", "CompensateHSMSeed", datos)
        # ... otros pasos de compensación ...