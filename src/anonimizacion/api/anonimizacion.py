import anonimizacion.seedwork.presentacion.api as api
import json
from anonimizacion.modulos.anonimizacion.aplicacion.servicios import ServicioToken
from anonimizacion.modulos.anonimizacion.aplicacion.dto import TokenDTO
from anonimizacion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorTokenDTOJson
from anonimizacion.modulos.anonimizacion.aplicacion.comandos.crear_token import CrearToken
from anonimizacion.modulos.anonimizacion.aplicacion.queries.obtener_token import ObtenerToken
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimizacion.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('anonimizacion', '/anonimizacion')

@bp.route('/token', methods=('POST',))
def crear_token():
    try:
        token_dict = request.json

        map_token = MapeadorTokenDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        sr = ServicioToken()
        dto_final = sr.crear_token(token_dto)

        return map_token.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/token-comando', methods=('POST',))
def crear_token_asincrona():
    try:
        token_dict = request.json

        map_token = MapeadorTokenDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearToken(token_dto.id, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion)
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/token', methods=('GET',))
@bp.route('/token/<id>', methods=('GET',))
def obtener_token(id=None):
    if id:
        sr = ServicioToken()
        map_token = MapeadorTokenDTOJson()
        
        return map_token.dto_a_externo(sr.obtener_token_por_id(id))
    else:
        return [{'message': 'GET!'}]

@bp.route('/token-query', methods=('GET',))
@bp.route('/token-query/<id>', methods=('GET',))
def obtener_token_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerToken(id))
        map_token = MapeadorTokenDTOJson()
        
        return map_token.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]



@bp.route('/token_documento', methods=('POST',))
def crear_token_documento():
    try:
        token_dict = request.json

        map_token = MapeadorTokenDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        sr = ServicioToken()
        dto_final = sr.crear_token(token_dto)

        return map_token.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/token_comando_documento', methods=('POST',))
def crear_token_documento_asincrona():
    try:
        token_dict = request.json

        map_token = MapeadorTokenDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearToken(token_dto.id, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion)
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')