from uoishelpers.resolvers import createDBResolvers
from uoishelpers.resolvers import DBResolver

from src.DBDefinitions import BaseModel


DBResolvers = createDBResolvers(BaseModel)

from src.DBDefinitions import (
    BaseModel,
    StateModel,
    StateMachineModel,
    StateTransitionModel,
    StatemachineTypeModel,
    StatemachineCategoryModel
    )

StateResolvers = DBResolver(StateModel)
StateMachineResolvers = DBResolver(StateMachineModel)
StateTransitionResolvers = DBResolver(StateTransitionModel)
StatemachineTypeResolvers = DBResolver(StatemachineTypeModel)
StatemachineCategoryResolvers = DBResolver(StatemachineCategoryModel)