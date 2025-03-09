from hsm.modulos.hsm.infraestructura.schema.v1.comandos import CrearHsmPayload
from hsm.seedwork.aplicacion.dto import Mapeador as AppMap
from hsm.seedwork.dominio.repositorios import Mapeador as RepMap
from hsm.modulos.hsm.dominio.entidades import Hsm
from .dto import HsmDTO

from datetime import datetime

class MapeadorHsmDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> HsmDTO:
        hsm_dto = HsmDTO(
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
        return hsm_dto

    def dto_a_externo(self, dto: HsmDTO) -> dict:
        return dto.__dict__

class MapeadorHsm(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Hsm.__class__

    def entidad_a_dto(self, entidad: Hsm) -> HsmDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        token_anonimo = str(entidad.token_anonimo)
        id_paciente = str(entidad.id_paciente)
        id_solicitud = str(entidad.id_solicitud)

        
        return HsmDTO(_id, id_solicitud, id_paciente, token_anonimo, fecha_creacion)

    def dto_a_entidad(self, dto: HsmDTO) -> Hsm:
        try:
            hsm = Hsm(
                id_solicitud=dto.id_solicitud,
                id_paciente=dto.id_paciente,
                token_anonimo=dto.token_anonimo,
                estado=dto.estado,
                fecha_creacion=dto.fecha_creacion,
                fecha_actualizacion=datetime.utcnow()
            )
            return hsm
        except Exception as e:
           
            print(f"Ocurrió un error: {e}")
        
    def payload_a_dto(self, CrearHsmPayload:CrearHsmPayload) -> HsmDTO:
        return HsmDTO(
            id_solicitud= CrearHsmPayload.id_solicitud,
            id_paciente = CrearHsmPayload.id_paciente,
            token_anonimo = "",
            estado = CrearHsmPayload.estado,
            fecha_creacion= datetime.now()
        )