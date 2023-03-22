from typing import List, Union
from datetime import datetime

from pydantic import BaseModel

class TicketBase(BaseModel):
    comments: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    plate: str
    created: datetime


    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    plate: str
    car_brand: str
    color: str
    
class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    owner_id : int
    tickets: list[Ticket]

    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    name: str
    email: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    vehicles: list[Vehicle]

    class Config:
        orm_mode = True


class AgentBase(BaseModel):
    name: str
    agent_identifier: int

class AgentCreate(AgentBase):
    password: str

class Agent(AgentBase):
    id: int

    class Config:
        orm_mode = True
