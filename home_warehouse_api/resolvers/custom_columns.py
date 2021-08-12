import graphene

from middlewares.automatizations import automatizations_checker

from graphene_mongo.fields import MongoengineConnectionField

from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_columns import CustomColumn, CustomColumnInput, CustomColumnModel


class CreateCustomColumnMutation(graphene.Mutation):
    custom_column = graphene.Field(CustomColumn)

    class Arguments:
        custom_column_details = CustomColumnInput(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, custom_column_details=None):
        custom_column = CustomColumnModel(
            name=custom_column_details.name,
            elements_allowed=custom_column_details.elements_allowed,
            values=custom_column_details.values,
            data_type=custom_column_details.data_type,
        )
        custom_column.save()
        automatizations_checker('custom_column')
        return CreateCustomColumnMutation(custom_column=custom_column)


class UpdateCustomColumnMutation(graphene.Mutation):
    id = graphene.String(required=True)
    custom_column = graphene.Field(CustomColumn)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        custom_column_details = CustomColumnInput(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None, custom_column_details=None):
        found_objects = list(CustomColumnModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            custom_column_details["id"] = id
            custom_column = CustomColumnModel(**custom_column_details)
            custom_column.update(**custom_column_details)
            automatizations_checker('custom_column')
            return UpdateCustomColumnMutation(custom_column=custom_column, modified=True)
        return UpdateCustomColumnMutation(custom_column=id, modified=False)


class DeleteCustomColumnnMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(CustomColumnModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            CustomColumnModel.delete(found_objects[0])
            automatizations_checker('custom_column')
            return DeleteCustomColumnnMutation(id=id, deleted=True)
        return DeleteCustomColumnnMutation(id=id, deleted=False)

# Resolvers


class CustomColumnsListsResolver(graphene.ObjectType):
    custom_columns_list = MongoengineConnectionField(CustomColumn)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_custom_columns_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(CustomColumn, *args)
