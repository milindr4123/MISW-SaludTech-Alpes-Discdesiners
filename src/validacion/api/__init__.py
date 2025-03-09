import asyncio
import os
import threading

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import validacion.modulos.validacion.aplicacion

def importar_modelos_alchemy():
    import validacion.modulos.validacion.infraestructura.dto

def comenzar_consumidor(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import validacion.modulos.validacion.infraestructura.consumidores as anonimizador_consumidores

    # Suscripción a eventos
    # threading.Thread(target=anonimizador_consumidores.suscribirse_a_eventos, args=[app]).start()

    # Suscripción a comandos
    threading.Thread(target=anonimizador_consumidores.suscribirse_a_comandos, args=[app]).start()


def comenzar_consumidor_asyncio(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional, puede ser un poco peligroso tener 
    threads corriendo por sí solos. Mi sugerencia es, en estos casos, usar un verdadero manejador
    de procesos y threads como Celery.
    
    Aquí hemos reemplazado threading por asyncio para manejar tareas asíncronas de forma más segura.
    """

    import validacion.modulos.validacion.infraestructura.consumidores as anonimizador_consumidores
    # Suscripción a eventos (si también es asíncrona, puedes hacer lo mismo)
    # asyncio.create_task(anonimizador_consumidores.suscribirse_a_eventos(app))
    def run_async_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Suscripción a comandos
        loop.create_task(anonimizador_consumidores.suscribirse_a_comandos(app))

        # Mantener el bucle corriendo
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
    threading.Thread(target=run_async_loop, daemon=True).start()
        
def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from validacion.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from validacion.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor_asyncio(app)

    # Importa Blueprints
    from . import validacion

    # Registro de Blueprints
    app.register_blueprint(validacion.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app