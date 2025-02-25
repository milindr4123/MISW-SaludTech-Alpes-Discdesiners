from hsm.config.db import db
from hsm.seedwork.infraestructura.uow import UnidadTrabajo, Batch

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return list[db.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        try:  # FIX: Se agregó manejo de excepciones para evitar fallos en mitad del commit
            for batch in self.batches:
                lock = batch.lock
                batch.operacion(*batch.args, **batch.kwargs)

            db.session.commit()
            super().commit()
        except Exception as e:  # FIX: Captura errores y revierte la transacción si algo falla
            db.session.rollback()
            raise e

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        db.session.begin_nested()