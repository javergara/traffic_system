import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email  = Column(String, unique=True, index=True)

    vehicles = relationship("Vehicle", back_populates= "owner")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True)
    car_brand = Column(String)
    color = Column(String)
    owner_id = Column(Integer, ForeignKey("people.id"))

    owner = relationship("Person", back_populates= "vehicles")
    tickets = relationship("Ticket", back_populates= "ticketed_vehicle")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    comments = Column(String)
    plate = Column(String, ForeignKey("vehicles.plate"))

    ticketed_vehicle = relationship("Vehicle", back_populates= "tickets")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    agent_identifier = Column(Integer, unique= True)

