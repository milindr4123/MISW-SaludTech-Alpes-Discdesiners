from tokenizacion.modulos.tokenizacion.infraestructura.schema.v1.comandos import CrearTokenizacionPayload
from tokenizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from tokenizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from .dto import TokenizacionDTO

from datetime import datetime

class MapeadorTokenizacionDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> TokenizacionDTO:
        tokenizacion_dto = TokenizacionDTO(
            id = externo.get('id'), 
            id_solicitud= externo.get('id_solicitud'),
            id_paciente= externo.get('id_paciente'),
            token_anonimo = externo.get('token_anonimo'),
            fecha_creacion= externo.get('fecha_creacion')
        )

        # token_dto = TokenDTO()
        # token_dto.id_paciente = externo.get('id_paciente')
        # token_dto.token_anonimo = externo.get('token_anonimo')
        # token_dto.fecha_creacion = externo.get('fecha_creacion')
        # token_dto.id = externo.get('id')
        return tokenizacion_dto

    def dto_a_externo(self, dto: TokenizacionDTO) -> dict:
        return dto.__dict__

class MapeadorTokenizacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Tokenizacion.__class__

    def entidad_a_dto(self, entidad: Tokenizacion) -> TokenizacionDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        token_anonimo = str(entidad.token_anonimo)
        id_paciente = str(entidad.id_paciente)
        id_solicitud = str(entidad.id_solicitud)

        
        return TokenizacionDTO(_id, id_solicitud, id_paciente, token_anonimo, fecha_creacion)

    def dto_a_entidad(self, dto: TokenizacionDTO) -> Tokenizacion:
        try:
            tokenizacion = Tokenizacion(
                id_solicitud=dto.id_solicitud,
                id_paciente=dto.id_paciente,
                token_anonimo=dto.token_anonimo,
                estado=dto.estado,
                fecha_creacion=dto.fecha_creacion,
                fecha_actualizacion=datetime.utcnow()
            )
            return tokenizacion
        except Exception as e:
           
            print(f"Ocurrió un error: {e}")
        
    def payload_a_dto(self, CrearTokenizacionPayload:CrearTokenizacionPayload) -> TokenizacionDTO:
        return TokenizacionDTO(
            id_solicitud= CrearTokenizacionPayload.id_solicitud,
            id_paciente = CrearTokenizacionPayload.id_paciente,
            token_anonimo = "",
            estado = CrearTokenizacionPayload.estado,
            fecha_creacion= datetime.now()
        )