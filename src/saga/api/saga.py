from flask import request, jsonify, current_app

from saga.seedwork.presentacion import api
from saga.modulos.saga.aplicacion.handlers import SagaHandler

bp = api.crear_blueprint('saga', '/saga')

@bp.route('/procesar_imagen', methods=('POST',))
async def procesar_imagen():
    datos = request.json
    handler = SagaHandler(current_app)
    try:
        await handler.iniciar_saga(datos)
        return jsonify({"mensaje": "Saga iniciada"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500