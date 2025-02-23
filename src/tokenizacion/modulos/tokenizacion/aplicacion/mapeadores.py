from tokenizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from tokenizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from tokenizacion.modulos.tokenizacion.dominio.entidades import Token
from .dto import TokenDTO

from datetime import datetime

class MapeadorTokenDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> TokenDTO:
        token_dto = TokenDTO(
            id = externo.get('id'), 
            id_paciente= externo.get('id_paciente'),
            token_anonimo = externo.get('token_anonimo'),
            fecha_creacion= externo.get('fecha_creacion')
        )

        # token_dto = TokenDTO()
        # token_dto.id_paciente = externo.get('id_paciente')
        # token_dto.token_anonimo = externo.get('token_anonimo')
        # token_dto.fecha_creacion = externo.get('fecha_creacion')
        # token_dto.id = externo.get('id')
        return token_dto

    def dto_a_externo(self, dto: TokenDTO) -> dict:
        return dto.__dict__

class MapeadorToken(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Token.__class__

    def entidad_a_dto(self, entidad: Token) -> TokenDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        token_anonimo = str(entidad.token_anonimo)
        id_paciente = str(entidad.id_paciente)

        
        return TokenDTO(_id, id_paciente, token_anonimo, fecha_creacion)

    def dto_a_entidad(self, dto: TokenDTO) -> Token:
        try:
            token = Token()
            token.id_paciente = dto.id_paciente
            token.token_anonimo = dto.token_anonimo
            return token
        except Exception as e:
           
            print(f"Ocurrió un error: {e}")
        
        
        