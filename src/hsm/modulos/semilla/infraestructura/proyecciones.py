from hsm.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from hsm.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from hsm.modulos.semilla.infraestructura.fabricas import FabricaRepositorio
from hsm.modulos.semilla.infraestructura.repositorios import RepositorioSemilla
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.modulos.semilla.infraestructura.dto import Semilla as SemillaDTO

from hsm.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import SemillaAnalitica

class ProyeccionSemilla(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionSemillasTotales(ProyeccionSemilla):
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
        record = db.session.query(SemillaAnalitica).filter_by(fecha_creacion=self.fecha_creacion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(SemillaAnalitica(fecha_creacion=self.fecha_creacion.date(), total=1))
        
        db.session.commit()

class ProyeccionSemillaLista(ProyeccionSemilla):
    def __init__(self, seed, estado, fecha_creacion, fecha_actualizacion):
        self.seed = seed
        self.estado = estado
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioSemilla)
        
        # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
        repositorio.agregar(
            Semilla(
               
                seed=str(self.seed), 
                estado=str(self.estado), 
                fecha_creacion=self.fecha_creacion, 
                fecha_actualizacion=self.fecha_actualizacion))
        
        # TODO ¿Y si la reserva ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionSemillaHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionSemilla):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from hsm.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionSemillaLista)
@proyeccion.register(ProyeccionSemillasTotales)
def ejecutar_proyeccion_semilla(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionSemillaHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    