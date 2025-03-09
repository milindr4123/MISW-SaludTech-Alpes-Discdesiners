from validacion.seedwork.infraestructura.vistas import Vista
from validacion.modulos.validacion.dominio.entidades import Validacion
from validacion.config.db import db
from .dto import Validacion as ValidacionDTO

class VistaValidacion(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [Validacion]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta TokenDTO a Token y valide que la consulta es correcta
        return db.session.query(ValidacionDTO).filter_by(**params)
