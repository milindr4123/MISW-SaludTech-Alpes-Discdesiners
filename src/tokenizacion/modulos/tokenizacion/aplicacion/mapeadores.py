from tokenizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from tokenizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from tokenizacion.modulos.tokenizacion.dominio.entidades import Token
from tokenizacion.modulos.tokenizacion.dominio.objetos_valor import DetalleToken
from .dto import TokenDTO, DetalleTokenDTO

from datetime import datetime

class MapeadorTokenDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> TokenDTO:
        token_dto = TokenDTO()
        token_dto.id_paciente = externo.get('id_paciente')
        token_dto.token_anonimo = externo.get('token_anonimo')
        token_dto.fecha_creacion = externo.get('fecha_creacion')
        token_dto.id = externo.get('id')
        return token_dto

    def dto_a_externo(self, dto: TokenDTO) -> dict:
        return dto.__dict__

class MapeadorToken(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_detalle(self, detalle_dto: DetalleTokenDTO) -> DetalleToken:
        return DetalleToken(
            nombre=detalle_dto.nombre,
            descripcion=detalle_dto.descripcion,
            valor=detalle_dto.valor
        )

    def obtener_tipo(self) -> type:
        return Token.__class__

    def entidad_a_dto(self, entidad: Token) -> TokenDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        detalle = self._procesar_detalle(entidad.detalle)
        
        return TokenDTO(fecha_creacion, fecha_actualizacion, _id, detalle)

    def dto_a_entidad(self, dto: TokenDTO) -> Token:
        token = Token()
        token.detalle = self._procesar_detalle(dto.detalle)
        token.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        token.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        token.id = dto.id
        
        return token