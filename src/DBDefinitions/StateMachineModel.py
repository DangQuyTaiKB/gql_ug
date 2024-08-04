import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .UUID import uuid, UUIDFKey, UUIDColumn
from .Base import BaseModel

from .utils import createTypeAndCategory
StatemachineTypeModel, StatemachineCategoryModel = createTypeAndCategory(tableNamePrefix="statemachine")

class StateMachineModel(BaseModel):
    __tablename__ = "statemachines"

    id = UUIDColumn()
    name = Column(String, comment="name of type")
    name_en = Column(String, comment="english name of type")

    type_id = Column(ForeignKey("statemachinetypes.id"), index=True, nullable=True)
    states = relationship("StateModel", uselist=True, viewonly=True)