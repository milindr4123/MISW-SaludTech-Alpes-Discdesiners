import hsm.seedwork.presentacion.api as api
import json
# from hsm.modulos.hsm.aplicacion.servicios import ServicioToken
from hsm.modulos.hsm.aplicacion.dto import HsmDTO
from hsm.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsmDTOJson
from hsm.modulos.hsm.aplicacion.comandos.crear_hsm import CrearHsm
from hsm.modulos.hsm.aplicacion.queries.obtener_hsm import ObtenerHsm
from hsm.seedwork.aplicacion.comandos import ejecutar_commando
from hsm.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('hsm', '/hsm')

@bp.route('/token', methods=('POST',))
def crear_token():
    try:
        token_dict = request.json

        map_token = MapeadorHsmDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        sr = None # ServicioToken()
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

        map_token = MapeadorHsmDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearHsm(token_dto.id, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion)
        
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
        sr = None # ServicioToken()
        map_token = MapeadorHsmDTOJson()
        
        return map_token.dto_a_externo(sr.obtener_token_por_id(id))
    else:
        return [{'message': 'GET!'}]

@bp.route('/token-query', methods=('GET',))
@bp.route('/token-query/<id>', methods=('GET',))
def obtener_token_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerHsm(id))
        map_token = MapeadorTokenDTOJson()
        
        return map_token.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]



@bp.route('/token_documento', methods=('POST',))
def crear_token_documento():
    try:
        token_dict = request.json

        map_token = MapeadorHsmDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        sr = None # ServicioToken()
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

        map_token = MapeadorHsmDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearHsm(token_dto.id, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion)
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')