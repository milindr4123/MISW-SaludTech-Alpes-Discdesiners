from hsm.seedwork.infraestructura.vistas import Vista
from hsm.modulos.hsm.dominio.entidades import Hsm
from hsm.config.db import db
from .dto import Hsm as HsmDTO

class VistaHsm(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [Hsm]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta TokenDTO a Token y valide que la consulta es correcta
        return db.session.query(HsmDTO).filter_by(**params)
