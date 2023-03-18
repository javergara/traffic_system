from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import models, schemas
from utils import crud
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/people/", response_model= schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.get_person_by_email(db, person_email= person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Person already created")
    return crud.create_person(db=db, person=person)

@app.get("/people/", response_model=list[schemas.Person])
def read_people(skip: int= 0, limit: int= 100, db: Session= Depends(get_db)):
    people = crud.get_persons(db, skip=skip, limit=limit)
    return people

@app.post("/people/{person_id}/vehicles/", response_model= schemas.Vehicle)
def create_vehicle_for_person(
    person_id: int, 
    vehicle: schemas.VehicleCreate, 
    db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle_by_plate(db, plate=vehicle.plate)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle already registered")
    return crud.create_vehicle(db=db, vehicle=vehicle, person_id=person_id)

@app.get("/vehicles/", response_model= list[schemas.Vehicle])
def read_vehicles(skip: int= 0, limit: int= 100, db: Session = Depends(get_db)):
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@app.post("/vehicles/{vehicle_plate}/tickets/", response_model= schemas.Ticket)
def load_ticket(vehicle_plate: str, ticket: schemas.TicketCreate, db: Session= Depends(get_db)):
    return crud.create_ticket(db= db, ticket=ticket, plate=vehicle_plate)

@app.get("/tickets/", response_model=list[schemas.Ticket])
def read_tickets(skip: int= 0, limit: int= 100, db: Session = Depends(get_db)):
    tickets=crud.get_tickets(db, skip=skip, limit=limit)
    return tickets

@app.post("/agents/", response_model= schemas.Agent)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    db_vehicle = crud.get_agent_by_identifier(db, agent_identifier=agent.agent_identifier)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Agent already created")
    return crud.create_agent(db= db, agent=agent)

@app.get("/agents/", response_model= list[schemas.Agent])
def read_agents(skip: int= 0, limit: int =100, db: Session = Depends(get_db)):
    agents = crud.get_agents(db= db, skip=skip, limit=limit)
    return agents

