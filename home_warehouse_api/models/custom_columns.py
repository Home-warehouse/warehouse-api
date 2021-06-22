import graphene
from graphene.relay.node import Node

from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import ListField, ReferenceField, StringField

from middlewares.permissions import PermissionsType, permissions_checker
from resolvers.node import CustomNode

# Models


class CustomColumnModel(Document):
    meta = {"collection": "custom_columns"}
    name = StringField(required=True)
    elements_allowed = ListField(StringField())
    data_type = StringField()


class CustomColumnValueModel(EmbeddedDocument):
    custom_column = ReferenceField(CustomColumnModel)
    value = StringField()


# Types
class CustomColumn(MongoengineObjectType):

    class Meta:
        model = CustomColumnModel
        interfaces = (CustomNode,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith']
        }


class CustomColumnValue(MongoengineObjectType):
    class Meta:
        model = CustomColumnValueModel
        interfaces = (CustomNode, )


# Mutations

class CustomColumnValueInput(graphene.InputObjectType):
    custom_column = graphene.ID(required=True)
    value = graphene.String()


class CustomColumnInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    elements_allowed = graphene.List(graphene.String, required=True)
    data_type = graphene.String(required=True)


class CreateCustomColumnMutation(graphene.Mutation):
    custom_column = graphene.Field(CustomColumn)

    class Arguments:
        custom_column_details = CustomColumnInput(required=True)

    def mutate(parent, info, custom_column_details=None):
        custom_column = CustomColumnModel(
            name=custom_column_details.name,
            elements_allowed=custom_column_details.elements_allowed,
            data_type=custom_column_details.data_type,
        )
        custom_column.save()
        return CreateCustomColumnMutation(custom_column=custom_column)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class UpdateCustomColumnMutation(graphene.Mutation):
    id = graphene.String(required=True)
    custom_column = graphene.Field(CustomColumn)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        custom_column_details = CustomColumnInput(required=True)

    def mutate(parent, info, id=None, custom_column_details=None):
        found_objects = list(CustomColumnModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            custom_column_details["id"] = id
            custom_column = CustomColumnModel(**custom_column_details)
            custom_column.update(**custom_column_details)
            return UpdateCustomColumnMutation(custom_column=custom_column, modified=True)
        return UpdateCustomColumnMutation(custom_column=id, modified=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class DeleteCustomColumnnMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(CustomColumnModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            CustomColumnModel.delete(found_objects[0])
            return DeleteCustomColumnnMutation(id=id, deleted=True)
        return DeleteCustomColumnnMutation(id=id, deleted=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))
# Resolvers


class CustomColumnsListsResolver(graphene.ObjectType):
    custom_columns_list = MongoengineConnectionField(CustomColumn)

    def resolve_custom_columns_list(parent, info):
        MongoengineConnectionField(CustomColumn)

    resolve_custom_columns_list = permissions_checker(
        resolve_custom_columns_list, PermissionsType(allow_any="user"))
