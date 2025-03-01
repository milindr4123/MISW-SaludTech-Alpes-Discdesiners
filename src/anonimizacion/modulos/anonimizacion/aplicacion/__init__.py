from pydispatch import dispatcher

from .handlers import HandlerTokenIntegracion

from anonimizacion.modulos.anonimizacion.dominio.eventos import TokenCreado
dispatcher.connect(HandlerTokenIntegracion.handle_token_creado, signal=f'{TokenCreado.__name__}Integracion')




