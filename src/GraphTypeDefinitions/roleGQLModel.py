import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated
from uoishelpers.resolvers import createInputs

from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphPermissions import (
    RoleBasedPermission, 
    OnlyForAuthentized,
    RBACPermission
)
import src.GraphTypeDefinitions
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,

    encapsulateInsert,
    encapsulateUpdate
)

from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a role of a user in a group (like user A in group B is Dean)""",
)
class RoleGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).roles

    id = resolve_id
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    @strawberry.field(
        description="""If an user has still this role""",
        permission_classes=[OnlyForAuthentized])
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(
        description="""When an user has got this role""",
        permission_classes=[OnlyForAuthentized])
    def startdate(self) -> Union[str, None]:
        return self.startdate

    @strawberry.field(
        description="""When an user has been removed from this role""",
        permission_classes=[OnlyForAuthentized])
    def enddate(self) -> Union[str, None]:
        return self.enddate

    @strawberry.field(
        description="""Role type (like Dean)""",
        permission_classes=[OnlyForAuthentized])
    async def roletype(self, info: strawberry.types.Info) -> Optional[RoleTypeGQLModel]:
        # result = await resolveRoleTypeById(session,  self.roletype_id)
        result = await src.GraphTypeDefinitions.RoleTypeGQLModel.resolve_reference(info, self.roletype_id)
        return result

    @strawberry.field(
        description="""User having this role. Must be member of group?""",
        permission_classes=[OnlyForAuthentized])
    async def user(self, info: strawberry.types.Info) -> Optional[UserGQLModel]:
        # result = await resolveUserById(session,  self.user_id)
        result = await src.GraphTypeDefinitions.UserGQLModel.resolve_reference(info, self.user_id)
        return result

    @strawberry.field(
        description="""Group where user has a role name""",
        permission_classes=[OnlyForAuthentized])
    async def group(self, info: strawberry.types.Info) -> Optional[GroupGQLModel]:
        # result = await resolveGroupById(session,  self.group_id)
        result = await src.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, self.group_id)
        return result
    
    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    @strawberry.field(
        description="""""",
        permission_classes=[OnlyForAuthentized])
    async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .RBACObjectGQLModel import RBACObjectGQLModel
        result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.createdby)
        return result    
        
#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
GroupInputWhereFilter = Annotated["GroupInputWhereFilter", strawberry.lazy(".groupGQLModel")]
UserInputWhereFilter = Annotated["UserInputWhereFilter", strawberry.lazy(".userGQLModel")]
RoleTypeInputWhereFilter = Annotated["RoleTypeInputWhereFilter", strawberry.lazy(".roleTypeGQLModel")]
@createInputs
@dataclass
class RoleInputWhereFilter:
    name: str
    valid: bool
    startdate: datetime.datetime
    enddate: datetime.datetime
    # from .groupGQLModel import GroupInputWhereFilter
    # from .userGQLModel import UserInputWhereFilter
    # from .roleTypeGQLModel import RoleTypeInputWhereFilter
    group: GroupInputWhereFilter
    user: UserInputWhereFilter
    roletype: RoleTypeInputWhereFilter

@strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized])
async def role_by_user(self, info: strawberry.types.Info, user_id: IDType) -> List["RoleGQLModel"]:
    loader = getLoader(info).roles
    rows = await loader.filter_by(user_id=user_id)
    return rows


from ._GraphResolvers import asPage
@strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized])
@asPage
async def role_page(self, info: strawberry.types.Info, where: Optional[RoleInputWhereFilter] = None) -> List["RoleGQLModel"]:
    loader = getLoader(info).roles
    return loader

from src.DBDefinitions import (
    UserModel, MembershipModel, GroupModel, RoleModel
)
from sqlalchemy import select

async def resolve_roles_on_user(self, info: strawberry.types.Info, user_id: IDType) -> List["RoleGQLModel"]:
    # ve vsech skupinach, kde je user clenem najdi vsechny role a ty vrat
    loaderm = getLoader(info).memberships
    rows = await loaderm.filter_by(user_id = user_id)
    groupids = [row.group_id for row in rows]
    # print("groupids", groupids)
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    loader = getLoader(info).roles
    rows = await loader.execute_select(stmt)
    return rows


async def resolve_roles_on_group(self, info: strawberry.types.Info, group_id: IDType) -> List["RoleGQLModel"]:
    # najdi vsechny role pro skupinu a nadrizene skupiny
    grouploader = getLoader(info).groups
    groupids = []
    cid = group_id
    while cid is not None:
        row = await grouploader.load(cid)
        if row is None:
            break
        groupids.append(row.id)
        cid = row.mastergroup_id
    # print("groupids", groupids)
    stmt = (
        select(RoleModel).
        where(RoleModel.group_id.in_(groupids))
    )
    roleloader = RoleGQLModel.getLoader(info)
    rows = await roleloader.execute_select(stmt)
    return rows

roles_on_user_decsription = """
## Description

Returns all roles applicable on an user (defined by userId).
If there is a dean, role with type named "dean" will be enlisted.
"""
@strawberry.field(
    description=roles_on_user_decsription,
    permission_classes=[OnlyForAuthentized])
async def roles_on_user(self, info: strawberry.types.Info, user_id: IDType) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_user(self, info, user_id=user_id)
    return rows

roles_on_group_decsription = """
## Description

Returns all roles applicable on a group (defined by groupId).
If the group is deparment which is subgroup of faculty, role with type named "dean" will be enlisted.
"""
@strawberry.field(
    description=roles_on_group_decsription,
    permission_classes=[OnlyForAuthentized])
async def roles_on_group(self, info: strawberry.types.Info, group_id: IDType) -> List["RoleGQLModel"]:
    rows = await resolve_roles_on_group(self, info=info, group_id=group_id)
    return rows

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class RoleUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class RoleInsertGQLModel:
    user_id: IDType
    group_id: IDType
    roletype_id: IDType
    id: Optional[IDType] = strawberry.field(description="primary key", default_factory=uuid.uuid1)
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = strawberry.field(description="start datetime of role", default_factory=datetime.datetime.now)
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.type(description="")
class RoleResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def role(self, info: strawberry.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result
    
class UpdateRolePermission(RBACPermission):
    message = "User is not allowed to update the role"
    async def has_permission(self, source, info: strawberry.types.Info, role: RoleUpdateGQLModel) -> bool:
        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        _role = await self.resolveUserRole(info, 
            rbacobject=role.id, 
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not _role: return False
        return True

@strawberry.mutation(
    description="""Updates a role""",
    permission_classes=[
        OnlyForAuthentized,
        UpdateRolePermission
    ])
async def role_update(self, 
    info: strawberry.types.Info, 
    role: RoleUpdateGQLModel
) -> RoleResultGQLModel:
    return await encapsulateUpdate(info, RoleGQLModel.getLoader(info), role, RoleResultGQLModel(msg="ok", id=None))

class InsertRolePermission(RBACPermission):
    message = "User is not allowed create new membership"
    async def has_permission(self, source, info: strawberry.types.Info, role: RoleInsertGQLModel) -> bool:
        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        _role = await self.resolveUserRole(info, 
            rbacobject=role.id, 
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not _role: return False
        return True

@strawberry.mutation(
    description="""Inserts a role""",
    permission_classes=[
        OnlyForAuthentized,
        InsertRolePermission
    ])
async def role_insert(self, 
    info: strawberry.types.Info, 
    role: RoleInsertGQLModel
) -> RoleResultGQLModel:
    role.rbacobject = role.group_id
    return await encapsulateInsert(info, RoleGQLModel.getLoader(info), role, RoleResultGQLModel(msg="ok", id=None))
    