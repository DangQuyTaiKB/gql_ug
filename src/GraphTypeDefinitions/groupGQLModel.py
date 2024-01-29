import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated
from .BaseGQLModel import BaseGQLModel, IDType
from uoishelpers.resolvers import createInputs

from ._GraphPermissions import (
    RBACPermission,
    RoleBasedPermission, 
    OnlyForAuthentized,
    InsertRBACPermission,
    AlwaysFailPermission
    )
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

GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".groupTypeGQLModel")]
MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
RoleInputWhereFilter = Annotated["RoleInputWhereFilter", strawberry.lazy(".roleGQLModel")]

GroupGQLModel_description = """
## Description

Group is entity with members. 
It can have also mastergroup.
Mastergroup can be only one.
Groups are organized in tree structures.
There also can be defined roles on the group.
"""
@strawberry.federation.type(keys=["id"], description="""Entity representing a group""")
class GroupGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).groups

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    @strawberry.field(
        description="""Group's email""",
        permission_classes=[OnlyForAuthentized])
    def email(self) -> Optional[str]:
        result = None if not self.email else self.email
        return result


    @strawberry.field(
        description="""Group's validity (still exists?)""",
        permission_classes=[
            OnlyForAuthentized
        ])
    def valid(self) -> Optional[bool]:
        result = False if not self.valid else self.valid 
        return result

    @strawberry.field(
        description="""Group's type (like Department)""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def grouptype(
        self, info: strawberry.types.Info
    ) -> Optional["GroupTypeGQLModel"]:
        from .groupTypeGQLModel import GroupTypeGQLModel
        result = await GroupTypeGQLModel.resolve_reference(info, id=self.grouptype_id)
        return result

    @strawberry.field(
        description="""Directly commanded groups""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def subgroups(
        self, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoader(info).groups
        # print(self.id)
        result = await loader.filter_by(mastergroup_id=self.id)
        return result

    @strawberry.field(
        description="""Commanding group""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def mastergroup(
        self, info: strawberry.types.Info
    ) -> Optional["GroupGQLModel"]:
        result = await GroupGQLModel.resolve_reference(info, id=self.mastergroup_id)
        return result

    @strawberry.field(
        description="""List of users who are member of the group""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def memberships(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:
        from .membershipGQLModel import MembershipGQLModel
        # result = await resolveMembershipForGroup(session,  self.id, skip, limit)
        # async with withInfo(info) as session:
        #     result = await resolveMembershipForGroup(session, self.id, skip, limit)
        #     return result

        loader = MembershipGQLModel.getLoader(info)
        #print(self.id)
        result = await loader.filter_by(group_id=self.id)
        return result

    @strawberry.field(
        description="""List of roles in the group""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def roles(self, info: strawberry.types.Info, where: Optional[RoleInputWhereFilter] = None) -> List["RoleGQLModel"]:
        # result = await resolveRolesForGroup(session,  self.id)
        from .roleGQLModel import RoleGQLModel
        loader = RoleGQLModel.getLoader(info)
        result = await loader.filter_by(group_id=self.id)
        return result

    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    @strawberry.field(
        description="""rbacobject represents an user or a group which allows to derive needed roles for CRUD operations""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .RBACObjectGQLModel import RBACObjectGQLModel
        result = await RBACObjectGQLModel.resolve_reference(info, self.id)
        return result    

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
# MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]
@createInputs
@dataclass
class GroupInputWhereFilter:
    id: IDType
    name: str
    valid: bool
    from .membershipGQLModel import MembershipInputWhereFilter
    memberships: MembershipInputWhereFilter

@strawberry.field(
    description="""Returns a list of groups (paged)""",
    permission_classes=[
        OnlyForAuthentized
    ])
async def group_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[GroupInputWhereFilter] = None,
    orderby: Optional[str] = None,
    desc: Optional[bool] = None
) -> List[GroupGQLModel]:
    from strawberry.type import StrawberryList
    print(info._field.type.__class__ == StrawberryList)
    wheredict = None if where is None else strawberry.asdict(where)
    loader = getLoader(info).groups
    result = await loader.page(skip, limit, where=wheredict, orderby=orderby, desc=desc)
    return result

@strawberry.field(
    description="""Finds a group by its id""",
    permission_classes=[
        OnlyForAuthentized
    ])
async def group_by_id(
    self, info: strawberry.types.Info, id: IDType
) -> Union[GroupGQLModel, None]:
    result = await GroupGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds an user by letters in name and surname, letters should be atleast three""",
    deprecation_reason='replaced by `query($letters: String!){groupPage(where: {name: {_like: $letters}}) { id name }}`',
    permission_classes=[
        OnlyForAuthentized
    ]
)
async def group_by_letters(
    self,
    info: strawberry.types.Info,
    validity: Union[bool, None] = None,
    letters: str = "",
) -> List[GroupGQLModel]:
    # result = await resolveGroupsByThreeLetters(session,  validity, letters)
    loader = getLoader(info).groups

    if len(letters) < 3:
        return []
    stmt = loader.getSelectStatement()
    model = loader.getModel()
    stmt = stmt.where(model.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    result = await loader.execute_select(stmt)
    return result

# @strawberry.field(description="""Random university""")
# async def randomUniversity(
#     self, name: str, info: strawberry.types.Info
# ) -> GroupGQLModel:
#     async with withInfo(info) as session:
#         # newId = await randomDataStructure(session,  name)
#         newId = await randomDataStructure(session, name)
#         print("random university id", newId)
#         # result = await resolveGroupById(session,  newId)
#         result = await resolveGroupById(session, newId)
#         print("db response", result.name)
#         return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class GroupUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    grouptype_id: Optional[IDType] = None
    mastergroup_id: Optional[IDType] = None
    valid: Optional[bool] = None
    changedby: strawberry.Private[IDType] = None


@strawberry.input(description="")
class GroupInsertGQLModel:
    name: str
    grouptype_id: IDType
    id: Optional[IDType] = strawberry.field(description="primary key", default_factory=uuid.uuid1)
    name_en: Optional[str] = None
    mastergroup_id: Optional[IDType] = None
    valid: Optional[bool] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.type(description="represents the result of CUD op on GroupGQLModel")
class GroupResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of group operation""")
    async def group(self, info: strawberry.types.Info) -> Union[GroupGQLModel, None]:
        # print("GroupResultGQLModel", "group", self.id, flush=True)
        result = await GroupGQLModel.resolve_reference(info, self.id)
        # print("GroupResultGQLModel", result.id, result.name, flush=True)
        return result


class UpdateGroupPermission(RBACPermission):
    message = "User is not allowed to create a new group"
    async def has_permission(self, source, info: strawberry.types.Info, group: GroupInsertGQLModel) -> bool:
        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        role = await self.resolveUserRole(info, 
            rbacobject=group.id, 
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not role: return False
        roleTypeName = role["type"]["name"]
        if roleTypeName in allowedRoleNames:
            if group.mastergroup_id:
                raise self.error_class(f"{roleTypeName} cannot change mastergroup_id")
            if group.grouptype_id:
                raise self.error_class(f"{roleTypeName} cannot change grouptype_id")
        return True

@strawberry.mutation(
    description="""Allows a update of group, also it allows to change the mastergroup of the group""",
    permission_classes=[
        OnlyForAuthentized
    ])
async def group_update(self, info: strawberry.types.Info, group: GroupUpdateGQLModel) -> GroupResultGQLModel:
    user = getUserFromInfo(info)
    group.changedby = user["id"]
    loader = GroupGQLModel.getLoader(info)
    
    updatedrow = await loader.update(group)
    #print(updatedrow, updatedrow.id, updatedrow.name, flush=True)
    id = group.id
    msg = "fail" if updatedrow is None else "ok"
    return GroupResultGQLModel(id=id, msg=msg)   


class InsertGroupPermission(RBACPermission):
    message = "User is not allowed to create a new group"
    async def has_permission(self, source, info: strawberry.types.Info, group: GroupInsertGQLModel) -> bool:
        adminRoleNames = ["administrátor"]
        allowedRolesNames = ["garant"]
        result = await self.resolveUserRole(info, 
            rbacobject=group.mastergroup_id, 
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRolesNames)
        return result

@strawberry.mutation(
    description="""Allows to insert a group""",
    permission_classes=[
        OnlyForAuthentized,
        InsertGroupPermission
    ])
async def group_insert(self, info: strawberry.types.Info, group: GroupInsertGQLModel) -> Optional[GroupResultGQLModel]:
    group.rbacobject = group.id
    user = getUserFromInfo(info)
    group.createdby = user["id"]   
    loader = GroupGQLModel.getLoader(info)
    
    updatedrow = await loader.insert(group)
    # print("group_insert", updatedrow, updatedrow.id, updatedrow.name, flush=True)
    result = GroupResultGQLModel()
    result.id = updatedrow.id
    result.msg = "fail" if updatedrow is None else "ok"
        
    return result

# @strawberry.mutation(
#     description="""Allows to assign the group to8 specified master group""",
#     permission_classes=[OnlyForAuthentized])
# async def group_update_master(self, 
#     info: strawberry.types.Info, 
#     master_id: IDType,
#     group: GroupUpdateGQLModel) -> GroupResultGQLModel:

#     user = getUserFromInfo(info)
#     group.createdby = user["id"]
#     loader = getLoader(info).groups
    
#     result = GroupResultGQLModel()
#     result.id = group.id
#     result.msg = "ok"

#     #use asyncio.gather here
#     updatedrow = await loader.load(group.id)
#     if updatedrow is None:
#         result.msg = "fail"
#         return result

#     masterrow = await loader.load(master_id)
#     if masterrow is None:
#         result.msg = "fail"
#         return result

#     updatedrow.master_id = master_id
#     updatedrow = await loader.update(updatedrow)
    
#     if updatedrow is None:
#         result.msg = "fail"
    
#     return result