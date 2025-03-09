""" Excepciones del dominio de vuelos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de tokenizacoion

"""

from hsm.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioHsmExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de Hsm'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)