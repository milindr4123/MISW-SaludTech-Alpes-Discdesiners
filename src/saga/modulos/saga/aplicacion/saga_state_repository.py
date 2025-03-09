from saga.config.db import db

from saga.modulos.saga.infraestructura.dto import SagaState

# Base.metadata.create_all(bind=engine)

class SagaStateRepository:
    def __init__(self, app=None):
        self.app = app


    def save_saga_state(self, request_id: str, step: str):
        with self.app.app_context():
            nueva_saga = SagaState(request_id=request_id, step=step)
            db.session.add(nueva_saga)
            db.session.commit()
