import hsm.seedwork.presentacion.api as api
import json
from hsm.modulos.semilla.aplicacion.dto import SemillaDTO
from hsm.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from hsm.modulos.semilla.aplicacion.mapeadores import MapeadorSemillaDTOJson
from hsm.modulos.semilla.aplicacion.comandos.crear_semilla import CrearSemilla
from hsm.modulos.semilla.aplicacion.queries.obtener_reserva import ObtenerReserva
from hsm.seedwork.aplicacion.comandos import ejecutar_commando
from hsm.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('hsm', '/hsm')


@bp.route('/hsm', methods=('POST',))
def reservar_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        reserva_dict = request.json

        map_reserva = MapeadorReservaDTOJson()
        reserva_dto = map_reserva.externo_a_dto(reserva_dict)

        comando = CrearReserva(reserva_dto.fecha_creacion, reserva_dto.fecha_actualizacion, reserva_dto.id, reserva_dto.itinerarios)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
