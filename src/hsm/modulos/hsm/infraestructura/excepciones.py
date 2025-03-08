""" Excepciones para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las Excepciones relacionadas
a la capa de infraestructura del dominio de tokenización

"""

from hsm.seedwork.dominio.excepciones import ExcepcionFabrica

class NoExisteImplementacionParaTipoFabricaExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una implementación para el repositorio con el tipo dado.'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)