from validacion.modulos.validacion.infraestructura.schema.v1.comandos import CrearValidacionPayload
from validacion.seedwork.aplicacion.dto import Mapeador as AppMap
from validacion.seedwork.dominio.repositorios import Mapeador as RepMap
from validacion.modulos.validacion.dominio.entidades import Validacion
from .dto import ValidacionDTO

from datetime import datetime

class MapeadorValidacionDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> ValidacionDTO:
        validacion_dto = ValidacionDTO(
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
        return validacion_dto

    def dto_a_externo(self, dto: ValidacionDTO) -> dict:
        return dto.__dict__

class MapeadorValidacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Validacion.__class__

    def entidad_a_dto(self, entidad: Validacion) -> ValidacionDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        token_anonimo = str(entidad.token_anonimo)
        id_paciente = str(entidad.id_paciente)
        id_solicitud = str(entidad.id_solicitud)

        
        return ValidacionDTO(_id, id_solicitud, id_paciente, token_anonimo, fecha_creacion)

    def dto_a_entidad(self, dto: ValidacionDTO) -> Validacion:
        try:
            validacion = Validacion(
                id_solicitud=dto.id_solicitud,
                id_paciente=dto.id_paciente,
                token_anonimo=dto.token_anonimo,
                estado=dto.estado,
                fecha_creacion=dto.fecha_creacion,
                fecha_actualizacion=datetime.utcnow()
            )
            return validacion
        except Exception as e:
           
            print(f"Ocurrió un error: {e}")
        
    def payload_a_dto(self, CrearValidacionPayload:CrearValidacionPayload) -> ValidacionDTO:
        return ValidacionDTO(
            id_solicitud= CrearValidacionPayload.id_solicitud,
            id_paciente = CrearValidacionPayload.id_paciente,
            token_anonimo = "",
            estado = CrearValidacionPayload.estado,
            fecha_creacion= datetime.now()
        )