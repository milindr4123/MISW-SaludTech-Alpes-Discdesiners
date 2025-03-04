from pydispatch import dispatcher

from .handlers import HandlerTokenIntegracion

from validacion.modulos.validacion.dominio.eventos import TokenCreado
dispatcher.connect(HandlerTokenIntegracion.handle_token_creado, signal=f'{TokenCreado.__name__}Integracion')




