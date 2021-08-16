from graphene_mongo.fields import MongoengineConnectionField
from middlewares.permissions import PermissionsType, permissions_checker
import graphene
from models.raports import Raport, RaportInputType, RaportModel, CreateRaportInputType


# Mutations


class CreateRaportMutation(graphene.Mutation):
    raport = graphene.Field(Raport, required=True)

    class Arguments:
        raport_details = CreateRaportInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, raport_details=None):
        raport = RaportModel(
            raport_name=raport_details.raport_name,
            description=raport_details.description,
            show_custom_columns=raport_details.show_custom_columns,
            sort_by=raport_details.sort_by,
            filter_by=raport_details.filter_by,
            short_results=raport_details.short_results
        )
        raport.save()
        return CreateRaportMutation(raport=raport)


class UpdateRaportMutation(graphene.Mutation):
    raport = graphene.Field(Raport, required=True)
    modified = graphene.Boolean(required=True)

    class Arguments:
        raport_details = RaportInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, raport_details=None):
        found_objects = list(RaportModel.objects(**{"id": raport_details['id']}))
        if len(found_objects) > 0:
            raport_details["id"] = raport_details['id']
            raport = RaportModel(**raport_details)
            raport.update(**raport_details)
            return UpdateRaportMutation(raport=raport, modified=True)
        return UpdateRaportMutation(raport=raport_details['id'], modified=False)


class DeleteRaportMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(RaportModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            RaportModel.delete(found_objects[0])
            return DeleteRaportMutation(id=id, deleted=True)
        return DeleteRaportMutation(id=id, deleted=False)


# Resolvers


class RaportsListsResolver(graphene.ObjectType):
    raports_list = MongoengineConnectionField(Raport)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_raports_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Raport, *args)
