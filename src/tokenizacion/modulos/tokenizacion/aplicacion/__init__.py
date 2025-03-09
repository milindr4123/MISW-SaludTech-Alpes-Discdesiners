from pydispatch import dispatcher

from .handlers import HandlerTokenizacionIntegracion

from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenizacionCreada, TokenizacionAprobada, TokenizacionFallida, TokenizacionCompensada
dispatcher.connect(HandlerTokenizacionIntegracion.handle_tokenizacion_creado, signal=f'{TokenizacionCreada.__name__}Integracion')
dispatcher.connect(HandlerTokenizacionIntegracion.handle_tokenizacion_aprobado, signal=f'{TokenizacionAprobada.__name__}Integracion')
dispatcher.connect(HandlerTokenizacionIntegracion.handle_tokenizacion_fallido, signal=f'{TokenizacionFallida.__name__}Integracion')
dispatcher.connect(HandlerTokenizacionIntegracion.handle_tokenizacion_compensada, signal=f'{TokenizacionCompensada.__name__}Integracion')




