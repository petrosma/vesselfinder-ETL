from sqlalchemy.orm import Session
import models
from db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def insert_vessel(vessel_data: dict, db: Session = SessionLocal()):
    delete_vessels(vessel_data)
    db_vessel = models.Vessels(**vessel_data)
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)
    db.close()

def delete_vessels(vessel_data:dict, db: Session = SessionLocal()):
    db.query(models.Vessels).filter(models.Vessels.vessel_mmsi == vessel_data['vessel_mmsi']).delete(synchronize_session=False)
    db.commit()



