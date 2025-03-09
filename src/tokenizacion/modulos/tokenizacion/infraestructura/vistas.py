from tokenizacion.seedwork.infraestructura.vistas import Vista
from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from tokenizacion.config.db import db
from .dto import Tokenizacion as TokenizacionDTO

class VistaTokenizacion(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> [Tokenizacion]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta TokenDTO a Token y valide que la consulta es correcta
        return db.session.query(TokenizacionDTO).filter_by(**params)
