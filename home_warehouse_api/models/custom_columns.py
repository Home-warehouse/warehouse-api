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

# Resolvers


class CustomColumnsListsResolver(graphene.ObjectType):
    custom_columns_list = MongoengineConnectionField(CustomColumn)

    def resolve_custom_columns_list(parent, info):
        MongoengineConnectionField(CustomColumn)

    resolve_custom_columns_list = permissions_checker(
        resolve_custom_columns_list, PermissionsType(allow_any="user"))
