import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class RoleTypeListModel(BaseModel):
    """Urcuje typ role (Vedouci katedry, dekan apod.)"""

    __tablename__ = "roletypelists"

    id = UUIDColumn()
    type_id = Column(ForeignKey("roletypes.id"), index=True, nullable=True)
    list_id = UUIDFKey(comment="list which item belongs to")#Column(ForeignKey("users.id"), index=True, nullable=True)

