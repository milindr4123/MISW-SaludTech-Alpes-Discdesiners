
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    anonimizacion: typing.List[Anonimizacion] = strawberry.field(resolver=obtener_anonimizaciones)