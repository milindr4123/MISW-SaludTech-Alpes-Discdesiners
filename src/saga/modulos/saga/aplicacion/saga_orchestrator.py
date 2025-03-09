import asyncio
from datetime import datetime
from uuid import uuid4
from saga.modulos.saga.aplicacion.manejador.anonimizador import ManejarAnominizacionEvento
from saga.modulos.saga.aplicacion.saga_state_repository import SagaStateRepository
from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
from saga.modulos.saga.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, ComandoCrearHsm, ComandoCrearTokenizacion, ComandoCrearValidacion, CrearAnonimizacionPayload, CrearHsmPayload, CrearTokenizacionPayload, CrearValidacionPayload
from saga.seedwork.infraestructura.utils import unix_time_millis

# from saga.producers import publish_event


class SagaOrchestrator:
    def __init__(self):
        self.repo = SagaStateRepository()
        self.despachador = DespachadorComandos()

    async def manejador_anonimizacion_aprobada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="TOKENIZATION_REQUESTED")
        topico = "TokenizacionCreada"
        evento_integracion = self.crear_comando_tokenizacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearTokenizacion)

    async def manejador_anonimizacion_rechazada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="ANONYMIZATION_FAILED")
        
    async def manejador_tokenizacion_aprobada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="HSM_REQUESTED")
        topico = "HsmCreada" 
        evento_integracion = self.crear_comando_hsm(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearHsm)
        
    async def manejador_tokenizacion_rechazada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="TOKENIZATION_FAILED")
        topico = "AnonimizacionCompensada"
        evento_integracion = self.crear_comando_anonimizacion_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearAnonimizacion)
        self.repo.save_saga_state(datos.id_solicitud, step="ANONYMIZATION_COMPENSATED")

    async def manejador_hsm_aprobada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="VALIDATION_REQUESTED")
        topico = "ValidacionCreada" 
        evento_integracion = self.crear_comando_validacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearValidacion)
        
    async def manejador_hsm_rechazada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="HSM_FAILED")
        topico = "TokenizacionCompensada"
        evento_integracion = self.crear_comando_tokenizacion_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearTokenizacion)
        self.repo.save_saga_state(datos.id_solicitud, step="TOKENIZATION_COMPENSATED")
        topico = "AnonimizacionCompensada"
        evento_integracion = self.crear_comando_anonimizacion_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearAnonimizacion)
        self.repo.save_saga_state(datos.id_solicitud, step="ANONYMIZATION_COMPENSATED")
        
    async def manejador_validacion_aprobada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="VALIDATION_REQUESTED_OK")
        
        
    async def manejador_validacion_rechazada(self, datos: object):
        self.repo.save_saga_state(datos.id_solicitud, step="VALIDATION_FAILED")
        topico = "HsmCompensada"
        evento_integracion = self.crear_comando_hsm_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearHsm)
        self.repo.save_saga_state(datos.id_solicitud, step="HSM_COMPENSATED")
        topico = "TokenizacionCompensada"
        evento_integracion = self.crear_comando_tokenizacion_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearTokenizacion)
        self.repo.save_saga_state(datos.id_solicitud, step="TOKENIZATION_COMPENSATED")
        topico = "AnonimizacionCompensada"
        evento_integracion = self.crear_comando_anonimizacion_compensacion(datos)
        self.despachador.publicar_mensaje_async(evento_integracion, topico, ComandoCrearAnonimizacion)
        self.repo.save_saga_state(datos.id_solicitud, step="ANONYMIZATION_COMPENSATED")
        
    
  






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
        
    def crear_comando_payload_validacion(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearValidacionPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='CREADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_validacion(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearValidacion(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_validacion(evento)
        )
        
    def crear_comando_payload_anonimacion_compensacion(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearAnonimizacionPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='COMPENSADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_anonimizacion_compensacion(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearAnonimizacion(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_anonimacion_compensacion(evento)
        )
        
        
        
    def crear_comando_payload_tokenizacion_compensacion(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearTokenizacionPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='COMPENSADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_tokenizacion_compensacion(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearTokenizacion(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_tokenizacion_compensacion(evento)
        )
        
        
        
        
    def crear_comando_payload_hsm_compensacion(self, datos):
        """
        Crea un payload en formato compatible con Avro basado en los datos del evento.
        """
        return CrearHsmPayload(
            id_solicitud=str(datos.id_solicitud), 
            id_paciente=str(datos.id_paciente), 
            token_anonimo=str(datos.token_anonimo),
            estado='COMPENSADO', 
            fecha_creacion=int(unix_time_millis(datetime.now())),
            fecha_actualizacion=int(unix_time_millis(datetime.now()))
        )
        
    def crear_comando_hsm_compensacion(self, evento):
        """
        Crea un comando con metadatos adicionales.
        """
        dat = datetime.now()
        unix = unix_time_millis(dat)
        
        return ComandoCrearHsm(
            correlation_id=str(uuid4()),
            timestamp=unix,
            data=self.crear_comando_payload_hsm_compensacion(evento)
        )