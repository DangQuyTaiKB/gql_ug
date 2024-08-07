import strawberry
import datetime
import typing
import uuid
import asyncio

from typing import Annotated
from enum import Enum    
from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getLoadersFromInfo,
    getUserFromInfo)
from .BaseGQLModel import BaseGQLModel

from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
    # createRootResolver_by_id,
    # createRootResolver_by_page

    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete
)

from src.DBResolvers import DBResolvers

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy('.roleTypeGQLModel')]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a state machine"""
)
class StateMachineGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).StateMachineModel
    
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""All states associated with this state machine""",
        permission_classes=[OnlyForAuthentized])
    async def states(self, info: strawberry.types.Info) -> typing.List["StateGQLModel"]:
        loader = StateGQLModel.getLoader(info)
        results = await loader.filter_by(statemachine_id=self.id)
        return results
           
    @strawberry.field(
        description="""All states associated with this state machine""",
        permission_classes=[OnlyForAuthentized])
    async def transitions(self, info: strawberry.types.Info) -> typing.List["StateTransitionGQLModel"]:
        loader = StateTransitionGQLModel.getLoader(info)
        results = await loader.filter_by(statemachine_id=self.id)
        return results
    

@strawberry.enum(description="")
class StateDataAccessType(Enum):
    READ = "read"
    WRITE = "write"

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a state of state machine"""
)
class StateGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).StateModel
    
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""Owing state machine""",
        permission_classes=[OnlyForAuthentized])
    async def statemachine(self, info: strawberry.types.Info) -> typing.Optional["StateMachineGQLModel"]:
        result = await StateMachineGQLModel.resolve_reference(info, id=self.statemachine_id)
        return result

    @strawberry.field(
        description="""position in list of states""",
        permission_classes=[OnlyForAuthentized])
    async def order(self, info: strawberry.types.Info) -> typing.Optional[int]:
        result = self.order 
        return result

    @strawberry.field(
        description="""Transitions linked into thist state""",
        permission_classes=[OnlyForAuthentized])
    async def sources(self, info: strawberry.types.Info) -> typing.List["StateTransitionGQLModel"]:
        loader = StateTransitionGQLModel.getLoader(info)
        results = await loader.filter_by(target_id=self.id)
        return results
    
    @strawberry.field(
        description="""Transitions going out of this state""",
        permission_classes=[OnlyForAuthentized])
    async def targets(self, info: strawberry.types.Info) -> typing.List["StateTransitionGQLModel"]:
        loader = StateTransitionGQLModel.getLoader(info)
        results = await loader.filter_by(source_id=self.id)
        return results

    # @strawberry.field(
    #     description="""All roletypes associated with this state, all roles will be enabled for read""",
    #     permission_classes=[OnlyForAuthentized])
    # async def readersroletypes(self, info: strawberry.types.Info) -> typing.List["RoleTypeGQLModel"]:
    #     from .roleListGQLModel import RoleTypeListGQLModel
    #     from .roleGQLModel import RoleGQLModel
    #     loader = RoleTypeListGQLModel.getLoader(info)
    #     results = await loader.filter_by(list_id=self.readerslist_id)
    #     awaitables = (RoleGQLModel.resolve_reference(info, id=r.roletype_id) for r in results)
    #     return await asyncio.gather(*awaitables)

    # @strawberry.field(
    #     description="""All roletypes associated with this state, all roles will be enabled for update""",
    #     permission_classes=[OnlyForAuthentized])
    # async def writersroletypes(self, info: strawberry.types.Info, access: typing.Optional[StateDataAccessType] = StateDataAccessType.READ) -> typing.List["RoleTypeGQLModel"]:

    #     from .roleListGQLModel import RoleTypeListGQLModel
    #     from .roleGQLModel import RoleGQLModel

    #     loader = RoleTypeListGQLModel.getLoader(info)
    #     if access == StateDataAccessType.READ:
    #         results = await loader.filter_by(list_id=self.readerslist_id)
    #     else:
    #         results = await loader.filter_by(list_id=self.writerslist_id)
    #     awaitables = (RoleGQLModel.resolve_reference(info, id=r.roletype_id) for r in results)
    #     return await asyncio.gather(*awaitables)

    @strawberry.field(
        description="""All roletypes associated with this state, all roles will be enabled for update""",
        permission_classes=[OnlyForAuthentized])
    async def roletypes(self, info: strawberry.types.Info, access: typing.Optional[StateDataAccessType] = StateDataAccessType.READ) -> typing.List["RoleTypeGQLModel"]:
        from .roleListGQLModel import RoleTypeListGQLModel
        from .roleTypeGQLModel import RoleTypeGQLModel
        loader = RoleTypeListGQLModel.getLoader(info)
        if access == StateDataAccessType.READ:
            results = await loader.filter_by(list_id=self.readerslist_id)
        else:
            results = await loader.filter_by(list_id=self.writerslist_id)
        awaitables = (RoleTypeGQLModel.resolve_reference(info, id=r.type_id) for r in results)
        return await asyncio.gather(*awaitables)

@strawberry.federation.type(
    keys=["id"], description="""Entity representing an entity type"""
)
class StateTransitionGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).StateTransitionModel
    
    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""Going from state""",
        permission_classes=[OnlyForAuthentized])
    async def source(self, info: strawberry.types.Info) -> typing.Optional["StateGQLModel"]:
        result = await StateGQLModel.resolve_reference(info, self.source_id)
        return result
    
    @strawberry.field(
        description="""Going to state""",
        permission_classes=[OnlyForAuthentized])
    async def target(self, info: strawberry.types.Info) -> typing.Optional["StateGQLModel"]:
        result = await StateGQLModel.resolve_reference(info, self.target_id)
        return result
    
    @strawberry.field(
        description="""Owing state machine""",
        permission_classes=[OnlyForAuthentized])
    async def statemachine(self, info: strawberry.types.Info) -> typing.Optional["StateMachineGQLModel"]:
        result = await StateMachineGQLModel.resolve_reference(info, self.statemachine_id)
        return result    
    
#############################################################
#
# Queries
#
#############################################################

from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

@createInputs
@dataclass
class StateMachineWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    created: datetime.datetime
    type_id: uuid.UUID

@createInputs
@dataclass
class StateWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    created: datetime.datetime
    statemachine_id: uuid.UUID

@createInputs
@dataclass
class StateTransitionWhereFilter:
    name: str
    name_en: str
    id: uuid.UUID
    created: datetime.datetime
    source_id: uuid.UUID
    target_id: uuid.UUID
    statemachine_id: uuid.UUID

from src.DBResolvers import (
    StateResolvers,
    StateMachineResolvers,
    StatemachineTypeResolvers,
    StatemachineCategoryResolvers,
    StateTransitionResolvers
)
state_page = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateResolvers.Page(GQLModel=StateGQLModel, WhereFilterModel=StateWhereFilter))

state_by_id = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateResolvers.ById(GQLModel=StateGQLModel))

statemachine_page = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateMachineResolvers.Page(GQLModel=StateMachineGQLModel, WhereFilterModel=StateMachineWhereFilter))

statemachine_by_id = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateMachineResolvers.ById(GQLModel=StateMachineGQLModel))

statetransition_page = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateTransitionResolvers.Page(GQLModel=StateTransitionGQLModel, WhereFilterModel=StateTransitionWhereFilter))

statetransition_by_id = strawberry.field(
    description="",
    permission_classes=[OnlyForAuthentized],
    resolver=StateTransitionResolvers.ById(GQLModel=StateTransitionGQLModel))

#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="Input structure - C operation")
class StatemachineInsertGQLModel:
    name: str = strawberry.field(description="name")   
    name_en: typing.Optional[str] = strawberry.field(description="name", default=None)   
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="Update structure - C operation")
class StatemachineUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberry.field(description="name", default=None)   
    name_en: typing.Optional[str] = strawberry.field(description="eng. name", default=None)   
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="Result of CU operations")
class StatemachineResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="Object of CU operation, final version")
    async def statemachine(self, info: strawberry.types.Info) -> StateMachineGQLModel:
        result = await StateMachineGQLModel.resolve_reference(info=info, id=self.id)
        return result

@strawberry.mutation(
    description="C operation",
    permission_classes=[OnlyForAuthentized])
async def statemachine_insert(self, info: strawberry.types.Info, statemachine: StatemachineInsertGQLModel) -> StatemachineResultGQLModel:
    return await encapsulateInsert(
        info=info,
        loader=StateMachineGQLModel.getLoader(info),
        entity=statemachine,
        result=StatemachineResultGQLModel(id=statemachine.id, msg="ok")
        )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def statemachine_update(self, info: strawberry.types.Info, statemachine: StatemachineUpdateGQLModel) -> StatemachineResultGQLModel:
    return await encapsulateUpdate(
        info=info,
        loader=StateMachineGQLModel.getLoader(info),
        entity=statemachine,
        result=StatemachineResultGQLModel(id=statemachine.id, msg="ok")
    )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def statemachine_delete(self, info: strawberry.types.Info, id: uuid.UUID) -> StatemachineResultGQLModel:
    return await encapsulateDelete(
        info=info,
        loader=StateMachineGQLModel.getLoader(info),
        id=id,
        result=StatemachineResultGQLModel(id=id, msg="ok")
    )

@strawberry.input(description="Input structure - C operation")
class StateInsertGQLModel:
    name: str = strawberry.field(description="name")   
    statemachine_id: uuid.UUID = strawberry.field(description="id of machine whichs state belongs to")
    name_en: typing.Optional[str] = strawberry.field(description="eng. name", default=None)   
    order: typing.Optional[int] = strawberry.field(description="order of states", default=None)
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="Update structure - C operation")
class StateUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    name: typing.Optional[str] = strawberry.field(description="name", default=None)   
    name_en: typing.Optional[str] = strawberry.field(description="eng. name", default=None)   
    order: typing.Optional[int] = strawberry.field(description="order of states", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="Result of CU operations")
class StateResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")
    machine_id: strawberry.Private[uuid.UUID] = None

    @strawberry.field(description="Object of CU operation, final version")
    async def state(self, info: strawberry.types.Info) -> typing.Optional[StateGQLModel]:
        result = await StateGQLModel.resolve_reference(info=info, id=self.id)
        return result
    
    @strawberry.field(description="statemachine - the owner of state")
    async def statemachine(self, info: strawberry.types.Info) -> typing.Optional[StateMachineGQLModel]:
        result = await StateMachineGQLModel.resolve_reference(info=info, id=self.machine_id)
        return result

@strawberry.mutation(
    description="C operation",
    permission_classes=[OnlyForAuthentized])
async def state_insert(self, info: strawberry.types.Info, state: StateInsertGQLModel) -> StateResultGQLModel:
    from .roleListGQLModel import RoleTypeListGQLModel
    loader = StateGQLModel.getLoader(info)
    dbrow = await loader.load(state.statemachine_id)
    result = (
        StateResultGQLModel(id=state.id, msg="ok", machine_id=dbrow.statemachine_id) 
        if dbrow else StateResultGQLModel(id=state.id, msg="fail")
    )   
    return await encapsulateInsert(
        info=info,
        loader=RoleTypeListGQLModel.getLoader(info),
        entity=state,
        result=result
        )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def state_update(self, info: strawberry.types.Info, state: StateUpdateGQLModel) -> StateResultGQLModel:
    from .roleListGQLModel import RoleTypeListGQLModel
    loader = StateGQLModel.getLoader(info)
    dbrow = await loader.load(state.id)
    result = (
        StateResultGQLModel(id=state.id, msg="ok", machine_id=dbrow.statemachine_id) 
        if dbrow else StateResultGQLModel(id=state.id, msg="fail")
    )   
    return await encapsulateUpdate(
        info=info,
        loader=RoleTypeListGQLModel.getLoader(info),
        entity=state,
        result=result
    )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def state_delete(self, info: strawberry.types.Info, id: uuid.UUID) -> StateResultGQLModel:
    return await encapsulateDelete(
        info=info,
        loader=StateGQLModel.getLoader(info),
        id=id,
        result=StateResultGQLModel(id=id, msg="ok")
    )


@strawberry.input(description="Input structure - C operation")
class StatetransitionInsertGQLModel:
    name: str = strawberry.field(description="name")   
    statemachine_id: uuid.UUID = strawberry.field(description="id of state machine")
    source_id: uuid.UUID = strawberry.field(description="id of state source")
    target_id: uuid.UUID = strawberry.field(description="id of state target")
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="eng. name", default=None)   
    
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="Update structure - C operation")
class StatetransitionUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="name", default=None)   
    name_en: typing.Optional[str] = strawberry.field(description="eng. name", default=None)   
    source_id: typing.Optional[uuid.UUID] = strawberry.field(description="id of state source", default=None)
    target_id: typing.Optional[uuid.UUID] = strawberry.field(description="id of state target", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="Result of CU operations")
class StatetransitionResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")
    machine_id: strawberry.Private[uuid.UUID] = None

    @strawberry.field(description="Object of CU operation, final version")
    async def statetransition(self, info: strawberry.types.Info) -> StateTransitionGQLModel:
        result = await StateTransitionGQLModel.resolve_reference(info=info, id=self.id)
        return result
  
    @strawberry.field(description="statemachine - the owner of state")
    async def statemachine(self, info: strawberry.types.Info) -> typing.Optional[StateMachineGQLModel]:
        result = await StateMachineGQLModel.resolve_reference(info=info, id=self.machine_id)
        return result

@strawberry.mutation(
    description="C operation",
    permission_classes=[OnlyForAuthentized])
async def statetransition_insert(self, info: strawberry.types.Info, statetransition: StatetransitionInsertGQLModel) -> StatetransitionResultGQLModel:
    return await encapsulateInsert(
        info=info,
        loader=StateTransitionGQLModel.getLoader(info),
        entity=statetransition,
        result=StatetransitionResultGQLModel(id=statetransition.id, msg="ok")
        )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def statetransition_update(self, info: strawberry.types.Info, statetransition: StatetransitionUpdateGQLModel) -> StatetransitionResultGQLModel:
    return await encapsulateUpdate(
        info=info,
        loader=StateTransitionGQLModel.getLoader(info),
        entity=statetransition,
        result=StatetransitionResultGQLModel(id=statetransition.id, msg="ok")
    )

@strawberry.mutation(
    description="U operation",
    permission_classes=[OnlyForAuthentized])
async def statetransition_delete(self, info: strawberry.types.Info, id: uuid.UUID) -> StatetransitionResultGQLModel:
    return await encapsulateDelete(
        info=info,
        loader=StateTransitionGQLModel.getLoader(info),
        id=id,
        result=StatetransitionResultGQLModel(id=id, msg="ok")
    )

# from enum import Enum
# @strawberry.enum(description="")
# class StateRoleTypeRight(Enum):
#     WRITE = 1
#     READ = 0

# @strawberry.input(description="")
# class StateRoleTypeInsertGQLModel:
#     state_id: uuid.UUID = strawberry.field(description="", default=None)
#     roletype_id: uuid.UUID = strawberry.field(description="", default=None)
#     level: StateRoleTypeRight = strawberry.field(description="")
#     createdby: strawberry.Private[uuid.UUID] = None 

# @strawberry.mutation(
#     description="Links roletype to state",
#     permission_classes=[OnlyForAuthentized])
# async def state_insert_role_type(self, info: strawberry.types.Info, staterole: StateRoleTypeInsertGQLModel) -> StateResultGQLModel:
#     stateloader = StateGQLModel.getLoader(info)
#     from .roleListGQLModel import RoleTypeListGQLModel
#     listloader = RoleTypeListGQLModel.getLoader(info)
#     staterow = await stateloader.load(staterole.state_id)
#     if staterole.level == StateRoleTypeRight.READ:
#         roletypelistitems = await listloader.filter_by(list_id=staterow.readerslist_id)
#     elif staterole.level == StateRoleTypeRight.WRITE:
#         roletypelistitems = await listloader.filter_by(list_id=staterow.writerslist_id)
#     else:
#         roletypelistitems = []
#     g = (r.id for r in roletypelistitems if r.type_id==staterole.roletype_id)
#     rowid = next(g, None)
#     if rowid:
#         return StateResultGQLModel(msg="fail", id=staterole.state_id)
#     return await encapsulateInsert(
#         info,
#         loader = RoleTypeListGQLModel.getLoader(info),
#         entity=staterole,
#         result=StateResultGQLModel(msg="ok", id=staterole.state_id)
#     )
    
# @strawberry.mutation(
#     description="Unlinks roletype from state",
#     permission_classes=[OnlyForAuthentized])
# async def state_delete_role_type(self, info: strawberry.types.Info, staterole: StateRoleTypeInsertGQLModel) -> StateResultGQLModel:
#     stateloader = StateGQLModel.getLoader(info)
#     from .roleListGQLModel import RoleTypeListGQLModel
#     listloader = RoleTypeListGQLModel.getLoader(info)
#     staterow = await stateloader.load(staterole.state_id)
#     if staterole.level == StateRoleTypeRight.READ:
#         roletypelistitems = await listloader.filter_by(list_id=staterow.readerslist_id)
#     elif staterole.level == StateRoleTypeRight.WRITE:
#         roletypelistitems = await listloader.filter_by(list_id=staterow.writerslist_id)
#     else:
#         roletypelistitems = []
#     g = (r.id for r in roletypelistitems if r.type_id==staterole.roletype_id)
#     rowid = next(g, None)
#     if rowid:
#         return await encapsulateDelete(
#             info,
#             loader = RoleTypeListGQLModel.getLoader(info),
#             id=rowid,
#             result=StateResultGQLModel(msg="ok", id=staterole.state_id)
#         )
#     return StateResultGQLModel(msg="fail", id=staterole.state_id)