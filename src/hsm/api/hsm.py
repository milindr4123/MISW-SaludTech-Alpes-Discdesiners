import hsm.seedwork.presentacion.api as api
import json
# from hsm.modulos.hsm.aplicacion.servicios import ServicioToken
from hsm.modulos.hsm.aplicacion.dto import HsmDTO
from hsm.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsmDTOJson
from hsm.modulos.hsm.aplicacion.comandos.crear_hsm import CrearHsm
from hsm.modulos.hsm.aplicacion.queries.obtener_hsm import ObtenerHsm
from hsm.seedwork.aplicacion.comandos import ejecutar_commando
from hsm.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('hsm', '/hsm')

@bp.route('/hsm', methods=('POST',))
def crear_token():
    try:
        token_dict = request.json

        map_token = MapeadorHsmDTOJson()
        token_dto = map_token.externo_a_dto(token_dict)

        comando = CrearHsm(token_dto.id_solicitud, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion, 'CREADO')

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
