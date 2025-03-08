from pydispatch import dispatcher

from .handlers import HandlerHsmIntegracion

from hsm.modulos.hsm.dominio.eventos import HsmCreada, HsmAprobada, HsmFallida, HsmCompensada
dispatcher.connect(HandlerHsmIntegracion.handle_hsm_creado, signal=f'{HsmCreada.__name__}Integracion')
dispatcher.connect(HandlerHsmIntegracion.handle_hsm_aprobado, signal=f'{HsmAprobada.__name__}Integracion')
dispatcher.connect(HandlerHsmIntegracion.handle_hsm_fallido, signal=f'{HsmFallida.__name__}Integracion')
dispatcher.connect(HandlerHsmIntegracion.handle_hsm_compensada, signal=f'{HsmCompensada.__name__}Integracion')




