from pydispatch import dispatcher

from .handlers import HandlerValidacionIntegracion

from validacion.modulos.validacion.dominio.eventos import ValidacionCreada, ValidacionAprobada, ValidacionFallida, ValidacionCompensada
dispatcher.connect(HandlerValidacionIntegracion.handle_validacion_creado, signal=f'{ValidacionCreada.__name__}Integracion')
dispatcher.connect(HandlerValidacionIntegracion.handle_validacion_aprobado, signal=f'{ValidacionAprobada.__name__}Integracion')
dispatcher.connect(HandlerValidacionIntegracion.handle_validacion_fallido, signal=f'{ValidacionFallida.__name__}Integracion')
dispatcher.connect(HandlerValidacionIntegracion.handle_validacion_compensada, signal=f'{ValidacionCompensada.__name__}Integracion')




