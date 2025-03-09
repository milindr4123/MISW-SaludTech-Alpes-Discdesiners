import anonimizacion.seedwork.presentacion.api as api
import json
# from anonimizacion.modulos.anonimizacion.aplicacion.servicios import ServicioToken
from anonimizacion.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from anonimizacion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from anonimizacion.modulos.anonimizacion.aplicacion.comandos.crear_anonimizacion import CrearAnonimizacion
from anonimizacion.modulos.anonimizacion.aplicacion.queries.obtener_anonimizacion import ObtenerAnonimizacion
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimizacion.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('anonimizacion', '/anonimizacion')

@bp.route('/anonimizar', methods=('POST',))
def crear_token_documento_asincrona():
    try:
        token_dict = request.json

        map_token = MapeadorAnonimizacionDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearAnonimizacion(token_dto.id_solicitud, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion, 'CREADO')
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')