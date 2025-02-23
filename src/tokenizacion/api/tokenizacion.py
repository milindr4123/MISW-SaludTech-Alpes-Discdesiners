import tokenizacion.seedwork.presentacion.api as api
import json
from tokenizacion.modulos.tokenizacion.aplicacion.servicios import ServicioToken
from tokenizacion.modulos.tokenizacion.aplicacion.dto import TokenDTO
from tokenizacion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenDTOJson
from tokenizacion.modulos.tokenizacion.aplicacion.comandos.crear_token import CrearToken
from tokenizacion.modulos.tokenizacion.aplicacion.queries.obtener_token import ObtenerToken
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando
from tokenizacion.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('tokenizacion', '/tokenizacion')

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

        comando = CrearToken(token_dto.fecha_creacion, token_dto.fecha_actualizacion, token_dto.id, token_dto.detalle)
        
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