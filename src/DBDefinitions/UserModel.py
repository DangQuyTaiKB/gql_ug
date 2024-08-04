import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem"""

    __tablename__ = "users"

    name = Column(String, comment="name of the user")
    middlename = Column(String, comment="name of the user")
    surname = Column(String, comment="name of the user")

    @hybrid_property
    def fullname(self):
        return self.name + " " + self.surname

    email = Column(String)
    startdate = Column(DateTime, comment="first date of user in the system")
    enddate = Column(DateTime, comment="last date of user in the system")
    valid = Column(Boolean, default=True, comment="if the user is still active")

    memberships = relationship("MembershipModel", back_populates="user", foreign_keys="MembershipModel.user_id")
    roles = relationship("RoleModel", back_populates="user", foreign_keys="RoleModel.user_id")
    # groups = relationship("GroupModel", 
    #     secondary="join(MembershipModel, GroupModel, GroupModel.id==MembershipModel.group_id)",
    #     primaryjoin="UserModel.id==MembershipModel.user_id",
    #     secondaryjoin="GroupModel.id==MembershipModel.group_id",
    #     uselist=True,
    #     viewonly=True
    # )

