import tokenizacion.seedwork.presentacion.api as api
import json
# from tokenizacion.modulos.tokenizacion.aplicacion.servicios import ServicioToken
from tokenizacion.modulos.tokenizacion.aplicacion.dto import TokenizacionDTO
from tokenizacion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacionDTOJson
from tokenizacion.modulos.tokenizacion.aplicacion.comandos.crear_tokenizacion import CrearTokenizacion
from tokenizacion.modulos.tokenizacion.aplicacion.queries.obtener_tokenizacion import ObtenerTokenizacion
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando
from tokenizacion.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('tokenizacion', '/tokenizacion')

@bp.route('/token', methods=('POST',))
def crear_token():
    try:
        token_dict = request.json

        map_token = MapeadorTokenizacionDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearTokenizacion(token_dto.id_solicitud, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion, 'CREADO')

        ejecutar_commando(comando)
       
       # Respuesta más significativa con los datos
        response_data = {
            "status": "success",
            "message": "Token creado correctamente",
            "data": {
                "id_solicitud": token_dto.id_solicitud,
                "id_paciente": token_dto.id_paciente,
                "token_anonimo": token_dto.token_anonimo,
                "fecha_creacion": token_dto.fecha_creacion
            }
        }
        return Response(json.dumps(response_data), status=202, mimetype='application/json')

    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
