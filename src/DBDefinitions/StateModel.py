import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .UUID import uuid, UUIDFKey, UUIDColumn
from .Base import BaseModel

class StateModel(BaseModel):
    __tablename__ = "states"

    name = Column(String, comment="name of type")
    name_en = Column(String, comment="english name of type")
    order = Column(Integer, comment="determines order of states", server_default="0")

    statemachine = relationship("StateMachineModel", back_populates="states")
    statemachine_id = Column(ForeignKey("statemachines.id"), index=True, nullable=False)
    readerslist_id = UUIDFKey(comment="who can read item in this state", default=uuid)
    writerslist_id = UUIDFKey(comment="who can update item in this state", default=uuid)
