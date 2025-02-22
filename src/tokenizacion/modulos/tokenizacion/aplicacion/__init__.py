from pydispatch import dispatcher

from .handlers import HandlerTokenIntegracion

from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenCreado, TokenRevocado
dispatcher.connect(HandlerTokenIntegracion.handle_token_creado, signal=f'{TokenCreado.__name__}Integracion')
dispatcher.connect(HandlerTokenIntegracion.handle_token_cancelado, signal=f'{TokenRevocado.__name__}Integracion')




