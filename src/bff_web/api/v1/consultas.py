
import strawberry
from .esquemas import *
##Anonimizacion
@strawberry.type
class Query:
    anonimizacion: typing.List[Anonimizacion] = strawberry.field(resolver=obtener_anonimizaciones)
##Tokenizacion
@strawberry.type
class Query:
    tokenizacion: typing.List[Tokenizacion] = strawberry.field(resolver=obtener_tokenizacion)
##Validacion
@strawberry.type
class Query:
    validacion: typing.List[Tokenizacion] = strawberry.field(resolver=obtener_validacion)
##HSM
@strawberry.type
class Query:
    hsm: typing.List[HSM] = strawberry.field(resolver=obtener_hsm)