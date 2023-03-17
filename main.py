from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .db import models, schemas
from .utils import crud
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@app.post("/persons/", response )



""" 
@app.on_event("startup")
async def startup():
    database = Database("sqlite:///./mydatabase.db")
    await database.connect()
    app.state.database = database

@app.on_event("shutdown")
async def shutdown():
    await app.state.database.disconnect()

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(50)),
)

@app.post("/users/")
async def create_user(name: str, email: str):
    query = users.insert().values(name=name, email=email)
    last_record_id = await app.state.database.execute(query)
    return {"id": last_record_id, "name": name, "email": email}
"""