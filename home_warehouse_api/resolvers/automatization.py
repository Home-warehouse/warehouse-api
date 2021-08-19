import graphene
from graphene_mongo.fields import MongoengineConnectionField
from middlewares.permissions import PermissionsType, permissions_checker
from models.automatization import Automatization, AutomatizationModel, CreateAutomatizationInputType
from models.raport import RaportModel


# Mutations


def findElementReference(elementType: str, elementID: str):
    if elementType == "RAPORT":
        return RaportModel.objects(**{"id": elementID})[0]


class CreateAutomatizationMutation(graphene.Mutation):
    automatization = graphene.Field(Automatization)
    created = graphene.Boolean(required=True)

    class Arguments:
        automatization_details = CreateAutomatizationInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, automatization_details=None):

        element_integrated = findElementReference(
            automatization_details.element_integrated.elementType,
            automatization_details.element_integrated.elementID
        )

        automatization = AutomatizationModel(
            app=automatization_details.app,
            automatization_name=automatization_details.automatization_name,
            config=automatization_details.config,
            element_integrated=element_integrated,
            elements_monitored=automatization_details.elements_monitored,
        )
        automatization.save()
        return CreateAutomatizationMutation(automatization=automatization, created=True)


class DeleteAutomatizationMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(AutomatizationModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            AutomatizationModel.delete(found_objects[0])
            return DeleteAutomatizationMutation(id=id, deleted=True)
        return DeleteAutomatizationMutation(id=id, deleted=False)


# Resolvers


class AutomatizationsListResolver(graphene.ObjectType):
    automatizations_list = MongoengineConnectionField(Automatization)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_automatizations_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Automatization, *args)
