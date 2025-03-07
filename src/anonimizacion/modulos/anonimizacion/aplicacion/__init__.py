from pydispatch import dispatcher

from .handlers import HandlerAnonimizacionIntegracion

from anonimizacion.modulos.anonimizacion.dominio.eventos import AnonimizacionCreada, AnonimizacionAprobada, AnonimizacionFallida, AnonimizacionCompensada
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_creado, signal=f'{AnonimizacionCreada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_aprobado, signal=f'{AnonimizacionAprobada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_fallido, signal=f'{AnonimizacionFallida.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_compensada, signal=f'{AnonimizacionCompensada.__name__}Integracion')




