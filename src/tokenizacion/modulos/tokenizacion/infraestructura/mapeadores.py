""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from tokenizacion.seedwork.dominio.repositorios import Mapeador
from tokenizacion.modulos.tokenizacion.dominio.entidades import Token, Usuario
from .dto import Token as TokenDTO
from .dto import Usuario as UsuarioDTO

class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Token) -> TokenDTO:
        token_dto = TokenDTO()
        token_dto.id = str(entidad.id)
        token_dto.estado = entidad.estado
        token_dto.fecha_creacion = entidad.fecha_creacion
        token_dto.usuarios = [self._usuario_entidad_a_dto(usuario) for usuario in entidad.usuarios]
        return token_dto

    def dto_a_entidad(self, dto: TokenDTO) -> Token:
        token = Token(
            id=dto.id,
            estado=dto.estado,
            fecha_creacion=dto.fecha_creacion,
            usuarios=[self._usuario_dto_a_entidad(usuario_dto) for usuario_dto in dto.usuarios]
        )
        return token

    def _usuario_entidad_a_dto(self, entidad: Usuario) -> UsuarioDTO:
        usuario_dto = UsuarioDTO()
        usuario_dto.id = str(entidad.id)
        usuario_dto.nombre = entidad.nombre
        usuario_dto.email = entidad.email
        usuario_dto.fecha_creacion = entidad.fecha_creacion
        return usuario_dto

    def _usuario_dto_a_entidad(self, dto: UsuarioDTO) -> Usuario:
        usuario = Usuario(
            id=dto.id,
            nombre=dto.nombre,
            email=dto.email,
            fecha_creacion=dto.fecha_creacion
        )
        return usuario

    def obtener_tipo(self) -> type:
        return Token.__class__