import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_anonimizacion(self, id_usuario: str, id_correlacion: str, info: Info) -> AnonimizacionRespuesta:
        anon_id_usuario, anon_id_correlacion = self._anonimizar_ids(id_usuario, id_correlacion)
        print(f"ID Usuario: {anon_id_usuario}, ID Correlación: {anon_id_correlacion}")
        payload = dict(
            id_usuario = anon_id_usuario,
            id_correlacion = anon_id_correlacion,
            fecha_creacion = utils.time_millis()
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoAnonimizacion",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-anonimizacion", "public/default/comando-crear-anonimizacion")
        
        return AnonimizacionRespuesta(mensaje="Procesando Mensaje", codigo=203)

    def _anonimizar_ids(self, id_usuario: str, id_correlacion: str) -> typing.Tuple[str, str]:
        anon_id_usuario = utils.anonymize(id_usuario)
        anon_id_correlacion = utils.anonymize(id_correlacion)
        return anon_id_usuario, anon_id_correlacion
    
    @strawberry.mutation
    async def crear_tokenizacion(self, id_paciente: str, info: Info) -> TokenizacionRespuesta:
        anon_id_paciente = utils.anonymize(id_paciente)
        print(f"ID Paciente: {anon_id_paciente}")
        payload = dict(
            id_paciente = anon_id_paciente,
            fecha_creacion = utils.time_millis()
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoTokenizacion",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-tokenizacion", "public/default/comando-crear-tokenizacion")
        
        return TokenizacionRespuesta(mensaje="Procesando Mensaje", codigo=203)
    @strawberry.mutation
    async def crear_validacion(self, id_paciente: str, info: Info) -> ValidacionRespuesta:
        anon_id_paciente = utils.anonymize(id_paciente)
        print(f"ID Paciente: {anon_id_paciente}")
        payload = dict(
            id_paciente = anon_id_paciente,
            fecha_creacion = utils.time_millis()
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoValidacion",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-validacion", "public/default/comando-crear-validacion")
        return ValidacionRespuesta(mensaje="Procesando Mensaje", codigo=203)
    @strawberry.mutation
    async  def crear_hsm(self, id: str, lenght: int, formato: str, info: Info) -> HsmRespuesta:
        payload = dict(
            id = id,
            lenght = lenght,
            formato = formato
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoHSM",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-hsm", "public/default/comando-crear-hsm")
        return HsmRespuesta(mensaje="Procesando Mensaje", codigo=203)