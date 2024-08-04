import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .UUID import uuid, UUIDFKey, UUIDColumn
from .Base import BaseModel

class StateTransitionModel(BaseModel):
    __tablename__ = "statetransitions"

    id = UUIDColumn()
    name = Column(String, comment="name of state transition")
    name_en = Column(String, comment="english name of state transition")

    source_id = Column(ForeignKey("states.id"), index=True, nullable=False)
    target_id = Column(ForeignKey("states.id"), index=True, nullable=False)
    statemachine_id = Column(ForeignKey("statemachines.id"), index=True, nullable=False)