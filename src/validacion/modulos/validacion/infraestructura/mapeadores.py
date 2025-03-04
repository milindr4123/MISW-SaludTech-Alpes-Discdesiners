""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from validacion.seedwork.dominio.repositorios import Mapeador
from validacion.modulos.validacion.dominio.entidades import Token
from .dto import Token as TokenDTO

class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Token) -> TokenDTO:
        token_dto = TokenDTO()
        token_dto.id_solicitud = str(entidad.id_solicitud)
        token_dto.id_paciente = entidad.id_paciente
        token_dto.token_anonimo = entidad.token_anonimo
        token_dto.fecha_creacion = entidad.fecha_creacion 
        return token_dto

    def dto_a_entidad(self, dto: TokenDTO) -> Token:
        token = Token(
            id=dto.id,
            id_solicitud=dto.id_solicitud,
            id_paciente=dto.id_paciente,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return token

    

    def obtener_tipo(self) -> type:
        return Token.__class__
    
