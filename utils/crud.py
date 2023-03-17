from sqlalchemy.orm import Session

from ..db import models, schemas

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(name= person.name, email=person.email )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id==vehicle_id).first()

def get_vehicle_by_plate(db: Session, plate: str):
    return db.query(models.Vehicle).filter(models.Vehicle.plate==plate).first()

def create_vehicle(db: Session, vehicle: schemas.Vehicle, person_id: int):
    db_vehicle = models.Vehicle(**vehicle.dict(), owner_id = person_id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_agent(db: Session, agent_id: int):
    return db.query(models.Agent).filter(models.Agent.id==agent_id).first()

