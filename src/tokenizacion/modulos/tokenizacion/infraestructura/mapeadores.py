""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from tokenizacion.seedwork.dominio.repositorios import Mapeador
from tokenizacion.modulos.tokenizacion.dominio.entidades import Token, DetalleToken
from .dto import Token as TokenDTO, DetalleToken as DetalleTokenDTO

class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Token) -> TokenDTO:
        token_dto = TokenDTO()
        token_dto.id = str(entidad.id)
        token_dto.id_paciente = entidad.id_paciente
        token_dto.token_anonimo = entidad.token_anonimo
        token_dto.fecha_creacion = entidad.fecha_creacion 
        return token_dto

    def dto_a_entidad(self, dto: TokenDTO) -> Token:
        token = Token(
            id=dto.id,
            id_paciente=dto.id_paciente,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return token

    

    def obtener_tipo(self) -> type:
        return Token.__class__
    
class MapeadorDetalle(Mapeador):
    def entidad_a_dto(self, entidad: DetalleToken) -> DetalleTokenDTO:
        detalle_dto = DetalleTokenDTO()
        detalle_dto.id = entidad.id
        detalle_dto.tipo = entidad.tipo
        detalle_dto.estado = entidad.estado
        detalle_dto.id_paciente = entidad.id_paciente
        detalle_dto.token_anonimo = entidad.token_anonimo
        detalle_dto.fecha_revocacion = entidad.fecha_revocacion
        detalle_dto.fecha_creacion = entidad.fecha_creacion
        return detalle_dto

    def dto_a_entidad(self, dto: DetalleTokenDTO) -> DetalleToken:
        detalle = DetalleToken(
            id=dto.id,
            tipo=dto.tipo,
            estado=dto.estado,
            id_paciente=dto.id_paciente,
            token_anonimo=dto.token_anonimo,
            fecha_revocacion=dto.fecha_revocacion,
            fecha_creacion=dto.fecha_creacion
        )
        return detalle

    

    def obtener_tipo(self) -> type:
        return DetalleToken.__class__   