from datetime import datetime
from saga.modulos.saga.infraestructura.schema.v1.comandos import CrearAnonimizacionPayload, ComandoCrearAnonimizacion
from saga.modulos.saga.dominio.eventos import (
    AnonimizationSucceeded,
    TokenizationFailed
)
from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
from saga.seedwork.infraestructura.utils import unix_time_millis

class SagaHandler:
    def __init__(self):
        self.despachador = DespachadorComandos()

    async def iniciar_saga(self, datos):
        try:
            # Paso 1: Anonimizar EventoAnonimizacionCreado publicar_mensaje(self, mensaje, topico, schema):
            topico = "AnonimizacionCreada"
            
            payload = CrearAnonimizacionPayload(
                id_solicitud=str(datos["id_solicitud"]), 
                id_paciente=str(datos["id_paciente"]), 
                token_anonimo=str(datos["token_anonimo"]), 
                fecha_creacion=int(unix_time_millis(datetime.now())),
                fecha_actualizacion=int(unix_time_millis(datetime.now())),
                estado='CREADO'
            )
            evento_integracion = ComandoCrearAnonimizacion(data=payload)
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