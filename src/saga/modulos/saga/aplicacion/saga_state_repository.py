import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SagaState(Base):
    __tablename__ = "saga_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String)
    step = Column(String)
    event_time = Column(DateTime, default=func.now())
    
    
basedir=os.path.abspath(os.path.dirname(__file__))
engine = create_engine(f'sqlite:///{os.path.join(basedir, "database.db")}')
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

class SagaStateRepository:
    def save_saga_state(self, request_id: str, step: str):
        db = SessionLocal()
        saga_state = SagaState(request_id=request_id, step=step)
        db.add(saga_state)
        db.commit()
        db.close()

    def update_saga_step(self, request_id: str, step: str):
        db = SessionLocal()
        saga_state = db.query(SagaState).filter_by(request_id=request_id).first()
        if saga_state:
            saga_state.step = step
            db.commit()
        db.close()
