from sqlalchemy.orm import Session

from db import models, schemas

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_person_by_email(db: Session, person_email: str):
    return db.query(models.Person).filter(models.Person.email == person_email).first()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(name= person.name, email=person.email )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit=limit).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id==vehicle_id).first()

def get_vehicle_by_plate(db: Session, plate: str):
    return db.query(models.Vehicle).filter(models.Vehicle.plate==plate).first()

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit=limit).all()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate, person_id: int):
    db_vehicle = models.Vehicle(**vehicle.dict(), owner_id = person_id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_agent(db: Session, agent_id: int):
    return db.query(models.Agent).filter(models.Agent.id==agent_id).first()

def get_agent_by_identifier(db: Session, agent_identifier: int):
    return db.query(models.Agent).filter(models.Agent.agent_identifier==agent_identifier).first()

def get_agents(db: Session, skip: int= 0, limit: int= 100):
    return db.query(models.Agent).offset(skip).limit(limit=limit).all()

def create_agent(db: Session, agent: schemas.AgentCreate):
    db_agent = models.Agent(name=agent.name, agent_identifier=agent.agent_identifier)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_ticket_by_plate(db: Session, plate: str):
    return db.query(models.Ticket).filter(models.Ticket.plate==plate).first()

def get_tickets(db: Session, skip: int= 0, limit: int= 100):
    return db.query(models.Ticket).offset(skip).limit(limit=limit).all()

def create_ticket(db: Session, ticket: schemas.TicketCreate, plate: str):
    db_ticket = models.Ticket(comments= ticket.comments, plate= plate)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
