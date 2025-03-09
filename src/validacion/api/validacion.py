import validacion.seedwork.presentacion.api as api
import json
# from validacion.modulos.validacion.aplicacion.servicios import ServicioToken
from validacion.modulos.validacion.aplicacion.dto import ValidacionDTO
from validacion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacionDTOJson
from validacion.modulos.validacion.aplicacion.comandos.crear_validacion import CrearValidacion
from validacion.modulos.validacion.aplicacion.queries.obtener_validacion import ObtenerValidacion
from validacion.seedwork.aplicacion.comandos import ejecutar_commando
from validacion.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('validacion', '/validacion')

@bp.route('/validacion', methods=('POST',))
def crear_token():
    try:
        token_dict = request.json

        map_token = MapeadorValidacionDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearValidacion(token_dto.id_solicitud, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion, 'CREADO')

        ejecutar_commando(comando)

         # Respuesta más significativa con los datos
        response_data = {
            "status": "success",
            "message": "validación realizada correctamente",
            "data": {
                "id_solicitud": token_dto.id_solicitud,
                "id_paciente": token_dto.id_paciente,
                "token_anonimo": token_dto.token_anonimo,
                "fecha_creacion": token_dto.fecha_creacion
            }
        }
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
