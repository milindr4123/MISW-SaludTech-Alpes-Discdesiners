import asyncio
import os
import threading

from flask import Flask, jsonify
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import saga.modulos.saga.aplicacion


def importar_modelos_alchemy():
    import saga.modulos.saga.infraestructura.dto

def comenzar_consumidor_asyncio(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional, puede ser un poco peligroso tener 
    threads corriendo por sí solos. Mi sugerencia es, en estos casos, usar un verdadero manejador
    de procesos y threads como Celery.
    
    Aquí hemos reemplazado threading por asyncio para manejar tareas asíncronas de forma más segura.
    """
    
    import saga.modulos.saga.infraestructura.consumidores as saga_consumidores

    def run_async_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Iniciar la tarea asíncrona
        loop.create_task(saga_consumidores.suscribirse_a_comandos(app))
        
        # Mantener el bucle corriendo
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    # Ejecutar el loop de asyncio en un hilo separado
    threading.Thread(target=run_async_loop, daemon=True).start()
        
        
        
def create_app(configuracion={}):
    # Init la aplicación de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from saga.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from saga.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()
    
    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor_asyncio(app)
            
    # Importa Blueprints
    from . import saga

    # Registro de Blueprints
    app.register_blueprint(saga.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Saga Orchestration API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"} 

    return app
