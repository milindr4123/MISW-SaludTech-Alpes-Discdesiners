from pydispatch import dispatcher

from .handlers import HandlerSemillaIntegracion

from hsm.modulos.semilla.dominio.eventos import SemillaCreada

dispatcher.connect(HandlerSemillaIntegracion.handle_semilla_creada, signal=f'{SemillaCreada.__name__}Integracion')
