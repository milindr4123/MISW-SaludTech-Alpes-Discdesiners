from hsm.seedwork.infraestructura.vistas import Vista
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.config.db import db
from .dto import Semilla as SemillaDTO

class VistaSemilla(Vista):
    def obtener_por(seed=None, estado=None,  **kwargs) -> [Semilla]:
        params = dict()

        if seed:
            params['seed'] = str(seed)
        
      
            
        # TODO Convierta ReservaDTO a Reserva y valide que la consulta es correcta
        return db.session.query(SemillaDTO).filter_by(**params)
