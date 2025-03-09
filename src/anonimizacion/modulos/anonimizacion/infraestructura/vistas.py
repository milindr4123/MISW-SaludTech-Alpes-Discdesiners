from anonimizacion.seedwork.infraestructura.vistas import Vista
from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from anonimizacion.config.db import db
from .dto import Anonimizacion as AnonimizacionDTO

class VistaAnonimizacion(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [Anonimizacion]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta TokenDTO a Token y valide que la consulta es correcta
        return db.session.query(AnonimizacionDTO).filter_by(**params)
