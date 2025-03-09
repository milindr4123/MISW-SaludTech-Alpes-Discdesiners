from validacion.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from validacion.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from validacion.modulos.validacion.infraestructura.fabricas import FabricaRepositorio
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioValidacion
from validacion.modulos.validacion.dominio.entidades import Validacion
from validacion.modulos.validacion.infraestructura.dto import Validacion as ValidacionDTO

from validacion.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import ReservaValidacion

class ProyeccionValidacion(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionValidacionTotales(ProyeccionValidacion):
    ADD = 1
    DELETE = 2
    UPDATE = 3

    def __init__(self, fecha_creacion, operacion):
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.operacion = operacion

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        # NOTE esta no usa repositorios y de una vez aplica los cambios. Es decir, no todo siempre debe ser un repositorio
        record = db.session.query(ReservaValidacion).filter_by(fecha_creacion=self.fecha_creacion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(ReservaValidacion(fecha_creacion=self.fecha_creacion.date(), total=1))
        
        db.session.commit()

class ProyeccionValidacionLista(ProyeccionValidacion):
    def __init__(self, id_solciitud, id_paciente, fecha_actualizacion, estado):
        self.id_solciitud = id_solciitud
        self.id_paciente = id_paciente
        self.estado = estado
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioValidacion)
        
        # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
        obj = Validacion(
                id_solicitud=str(self.id_solciitud), 
                id_paciente=str(self.id_paciente), 
                token_anonimo='',
                estado=self.estado,
                fecha_creacion=self.fecha_actualizacion,
                fecha_actualizacion=self.fecha_actualizacion)
        repositorio.agregar( obj )
        
        # TODO ¿Y si la reserva ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionValidacionHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionValidacion):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from validacion.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionValidacionLista)
@proyeccion.register(ProyeccionValidacionTotales)
def ejecutar_proyeccion_validacion(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionValidacionHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    