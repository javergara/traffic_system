from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from db import models, schemas
from utils import crud
from db.database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

ALGORITHM= "HS256"
ACESS_TOKEN_TIME = 20
SECRET= "N5TEST"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:5500"
]

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

def token_verification(token: str= Depends(oauth2), db: Session = Depends(get_db)):
    try:
        agent_id = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Not authorized cow",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    if not crud.get_agent_by_identifier(db=db, agent_identifier= agent_id):
        raise HTTPException(status_code=400, detail="Agent not found")
    return True

@app.post("/login/")
def login(form: OAuth2PasswordRequestForm= Depends(), db: Session= Depends(get_db)):
    db_agent = crud.get_agent_by_identifier(db= db, agent_identifier=form.username)

    if not db_agent:
        raise HTTPException(status_code=400, detail="Not agent found")
    if not crypt.verify(form.password, db_agent.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    acces_token = {"sub": str(db_agent.agent_identifier), 
                   "exp": datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_TIME)}
    return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM),
            "token_type":"bearer"}

@app.post("/people/", response_model= schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    if person.name == "" or person.email == "":
        raise HTTPException(status_code=400, detail="Empty values")
    db_person = crud.get_person_by_email(db, person_email= person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Person already created")
    return crud.create_person(db=db, person=person)

@app.get("/people/", response_model=list[schemas.Person])
def read_people(skip: int= 0, limit: int= 100, db: Session= Depends(get_db)):
    people = crud.get_persons(db, skip=skip, limit=limit)
    return people

@app.delete("/people/{person_id}")
def delete_person(person_id:int , db: Session = Depends(get_db)):
    if not crud.get_person(db, person_id=person_id):
        raise HTTPException(status_code=400, detail= "Person not in database")
    crud.delete_person(db=db, person_id=person_id)
    return {"person_id": person_id, "status": "deleted"}

@app.patch("/people/{person_id}")
def update_person(person_id: int, name: str, db: Session = Depends(get_db)):
    if not crud.get_person(db, person_id=person_id):
        raise HTTPException(status_code=400, detail= "Person not in database")
    crud.update_person(db= db, person_id= person_id, name=name)
    return {"name": name, "person_id": person_id, "status": "updated"}

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

@app.delete("/vehicles/{vehicle_plate}")
def delete_vehicle(vehicle_plate: str, db: Session = Depends(get_db)):
    if not crud.get_vehicle_by_plate(db= db, plate=vehicle_plate):
        raise HTTPException(status_code=400, detail= "Vehicle not in database")
    crud.delete_vehicle(db=db, plate=vehicle_plate)
    return {"vehicle_plate": vehicle_plate, "status": "deleted"}

@app.patch("/vehicles/{vehicle_plate}")
def update_vehicle(vehicle_plate: str, brand:str, db: Session = Depends(get_db)):
    if not crud.get_vehicle_by_plate(db= db, plate=vehicle_plate):
        raise HTTPException(status_code=400, detail= "Vehicle not in database")
    crud.update_vehicle(db=db, plate=vehicle_plate, brand=brand)
    return {"brand": brand, "plate": vehicle_plate, "status": "updated"}

@app.post("/vehicles/{vehicle_plate}/tickets/", response_model= schemas.Ticket)
def load_ticket(vehicle_plate: str, 
                ticket: schemas.TicketCreate,
                token_validation: bool = Depends(token_verification),
                db: Session= Depends(get_db)):
    if not token_validation:
        raise HTTPException(status_code=401, detail="Not authorized", headers={"WWW-Authenticate": "Bearer"})
    
    db_vehicle = crud.get_vehicle_by_plate(db, plate=vehicle_plate)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Plate not found")
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

@app.delete("/agents/{agent_identifier}")
def delete_agent(agent_identifier: int, db: Session = Depends(get_db)):
    if not crud.get_agent_by_identifier(db= db, agent_identifier=agent_identifier):
        raise HTTPException(status_code=400, detail= "Agent not in database")
    crud.delete_agent(db=db, agent_identifier=agent_identifier)
    return {"agent_id": agent_identifier, "status": "deleted"}

@app.patch("/agents/{agent_identifier}")
def update_agent(agent_identifier: int, name:str, db: Session = Depends(get_db)):
    if not crud.update_agent(db= db, agent_identifier=agent_identifier, name=name):
        raise HTTPException(status_code=400, detail= "Agent not in database")
    crud.update_agent(db=db, agent_identifier=agent_identifier, name=name)
    return {"name": name, "agent_id": agent_identifier, "status": "updated"}

@app.get("/report/{email}/")
def generate_report(email: str, db: Session= Depends(get_db)):
    db_person = crud.get_person_by_email(db= db, person_email=email)
    traffic_ticket_by_plate = {"name": db_person.name, "email": db_person.email}
    for vehicles in db_person.vehicles:
        traffic_ticket_by_plate[vehicles.plate]= vehicles.tickets
    return traffic_ticket_by_plate