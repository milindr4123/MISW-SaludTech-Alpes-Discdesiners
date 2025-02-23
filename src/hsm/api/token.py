import hsm.seedwork.presentacion.api as api
import json
from hsm.seedwork.dominio.excepciones import ExcepcionDominio
from hsm.modulos.semilla.infraestructura.despachadores import Despachador
from flask import redirect, render_template, request, session, url_for
from flask import Response
from hsm.modulos.semilla.aplicacion.mapeadores import MapeadorSemillaDTOJson
from hsm.modulos.semilla.aplicacion.comandos.crear_semilla import CrearSemilla
from hsm.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('hsm', '/hsm')
despachador = Despachador()

@bp.route('/hsm', methods=('POST',))
def generar_semilla_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'
        semilla_dict = request.json
        map_semilla = MapeadorSemillaDTOJson()
        semilla_dto = map_semilla.externo_a_dto(semilla_dict)

        comando = CrearSemilla(semilla_dto.formato, semilla_dto.length)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        despachador.publicar_comando(comando, "comandos-semilla")   

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
