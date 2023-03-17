from typing import List, Union

from pydantic import BaseModel

class VehicleBase(BaseModel):
    vehicle_plate: str
    car_brand: str
    color: str
    
class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    owner_id : int

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
    agent_name: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int