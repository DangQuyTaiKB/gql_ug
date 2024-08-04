# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import declarative_base

# BaseModel = declarative_base()

from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4
import sqlalchemy
from sqlalchemy import (
    Column,
    DateTime,
    Uuid
)
def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

class BaseModel(DeclarativeBase):
    id = Column(Uuid, primary_key=True, index=True, comment="primary key", default=uuid4)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")

    createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    
    rbacobject = UUIDFKey(nullable=True, comment="holds object for role resolution")#Column(ForeignKey("users.id"), index=True, nullable=True)        

    pass