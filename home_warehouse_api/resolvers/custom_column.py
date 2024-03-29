import graphene
from graphene_mongo.fields import MongoengineConnectionField
from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_column import CreateCustomColumnInputType, CustomColumn, CustomColumnInputType, CustomColumnModel


# Mutations


class CreateCustomColumnMutation(graphene.Mutation):
    custom_column = graphene.Field(CustomColumn)
    created = graphene.Boolean(required=True)

    class Arguments:
        custom_column_details = CreateCustomColumnInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, custom_column_details=None):
        custom_column = CustomColumnModel(
            index=custom_column_details.index,
            custom_column_name=custom_column_details.custom_column_name,
            elements_allowed=custom_column_details.elements_allowed,
            values=custom_column_details.values,
            data_type=custom_column_details.data_type,
        )
        custom_column.save()
        return CreateCustomColumnMutation(custom_column=custom_column, created=True)


class UpdateCustomColumnMutation(graphene.Mutation):
    custom_columns = graphene.List(CustomColumn, required=True)
    modified = graphene.Boolean(required=True)

    class Arguments:
        input = graphene.List(CustomColumnInputType, required=True, description="List of custom columns to be updated")

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, input=None):
        custom_columns_output = []
        for cc in input:
            found_objects = list(CustomColumnModel.objects(**{"id": cc['id']}))
            if len(found_objects) > 0:
                custom_column = CustomColumnModel(**cc)
                custom_column.update(**cc)
                custom_column.update(set__values=cc.values)
                custom_columns_output.append(custom_column)
            else:
                return UpdateCustomColumnMutation(custom_columns=None, modified=False)
        return UpdateCustomColumnMutation(custom_columns=custom_columns_output, modified=True)


class DeleteCustomColumnnMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(CustomColumnModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            CustomColumnModel.delete(found_objects[0])
            return DeleteCustomColumnnMutation(id=id, deleted=True)
        return DeleteCustomColumnnMutation(id=id, deleted=False)


# Resolvers


class CustomColumnsListsResolver(graphene.ObjectType):
    custom_columns_list = MongoengineConnectionField(CustomColumn)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_custom_columns_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(CustomColumn, *args)
