from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import CrearAnonimizacionPayload
from anonimizacion.seedwork.aplicacion.dto import Mapeador as AppMap
from anonimizacion.seedwork.dominio.repositorios import Mapeador as RepMap
from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from .dto import AnonimizacionDTO

from datetime import datetime

class MapeadorAnonimizacionDTOJson(AppMap):
    
    
    def externo_a_dto(self, externo: dict) -> AnonimizacionDTO:
        anonimizacion_dto = AnonimizacionDTO(
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
        return anonimizacion_dto

    def dto_a_externo(self, dto: AnonimizacionDTO) -> dict:
        return dto.__dict__

class MapeadorAnonimizacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Anonimizacion.__class__

    def entidad_a_dto(self, entidad: Anonimizacion) -> AnonimizacionDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        token_anonimo = str(entidad.token_anonimo)
        id_paciente = str(entidad.id_paciente)
        id_solicitud = str(entidad.id_solicitud)

        
        return AnonimizacionDTO(_id, id_solicitud, id_paciente, token_anonimo, fecha_creacion)

    def dto_a_entidad(self, dto: AnonimizacionDTO) -> Anonimizacion:
        try:
            anonimizacion = Anonimizacion(
                id_solicitud=dto.id_solicitud,
                id_paciente=dto.id_paciente,
                token_anonimo=dto.token_anonimo,
                estado=dto.estado,
                fecha_creacion=dto.fecha_creacion,
                fecha_actualizacion=datetime.utcnow()
            )
            return anonimizacion
        except Exception as e:
           
            print(f"Ocurrió un error: {e}")
        
    def payload_a_dto(self, CrearAnonimizacionPayload:CrearAnonimizacionPayload) -> AnonimizacionDTO:
        return AnonimizacionDTO(
            id_solicitud= CrearAnonimizacionPayload.id_solicitud,
            id_paciente = CrearAnonimizacionPayload.id_paciente,
            token_anonimo = "",
            estado = CrearAnonimizacionPayload.estado,
            fecha_creacion= datetime.now()
        )