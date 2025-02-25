""" Excepciones reusables parte del seedwork del proyecto

En este archivo usted encontrará los Excepciones reusables parte del seedwork del proyecto

"""

from .reglas import ReglaNegocio

class ExcepcionDominio(Exception):
    ...

class IdDebeSerInmutableExcepcion(ExcepcionDominio):
    def __init__(self, mensaje='El identificador debe ser inmutable'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)
        
class IdDebeSerMayor32Excepcion(ExcepcionDominio):
    def __init__(self, mensaje='El tamaño debe ser mayor a 32'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)

class ReglaNegocioExcepcion(ExcepcionDominio):
    def __init__(self, regla: ReglaNegocio):
        self.regla = regla

    def __str__(self):
        return str(self.regla)

class ExcepcionFabrica(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)