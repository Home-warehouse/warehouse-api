import graphene

from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, ListField, ReferenceField, StringField

from middlewares.permissions import PermissionsType, permissions_checker
from resolvers.node import CustomNode, EmbeddedNode

# Models


class IntegrationSettingsModel(EmbeddedDocument):
    '''IntegrationSettings model for mongoengine'''
    intergration_app = StringField()
    intergration_func = StringField()


class AutomatizationModel(Document):
    '''Automatization model for mongoengine'''
    meta = {"collection": "automatizations"}
    name = StringField(required=True)
    element = StringField()
    integration = EmbeddedDocumentField(IntegrationSettingsModel)

# Types


class Automatization(MongoengineObjectType):
    '''Automatization type for mongoengine'''

    class Meta:
        model = AutomatizationModel
        interfaces = (CustomNode,)


# Mutations


# class CustomColumnValueInput(graphene.InputObjectType):
#     '''CustomColumnValue input for graphene'''
#     custom_column = graphene.ID(required=True)
#     value = graphene.String()


class AutomatizationInput(graphene.InputObjectType):
    '''Automatization input for graphene'''
    id = graphene.ID()
    name = graphene.String(required=True)
    elements_allowed = graphene.List(graphene.String, required=True)
    values = graphene.List(graphene.String, required=True)
    data_type = graphene.String(required=True)


# class CreateCustomColumnMutation(graphene.Mutation):
#     custom_column = graphene.Field(CustomColumn)

#     class Arguments:
#         custom_column_details = CustomColumnInput(required=True)

#     @permissions_checker(PermissionsType(allow_any="user"))
#     def mutate(parent, info, custom_column_details=None):
#         custom_column = CustomColumnModel(
#             name=custom_column_details.name,
#             elements_allowed=custom_column_details.elements_allowed,
#             values=custom_column_details.values,
#             data_type=custom_column_details.data_type,
#         )
#         custom_column.save()
#         return CreateCustomColumnMutation(custom_column=custom_column)


# class UpdateCustomColumnMutation(graphene.Mutation):
#     id = graphene.String(required=True)
#     custom_column = graphene.Field(CustomColumn)
#     modified = graphene.Boolean()

#     class Arguments:
#         id = graphene.String(required=True)
#         custom_column_details = CustomColumnInput(required=True)

#     @permissions_checker(PermissionsType(allow_any="user"))
#     def mutate(parent, info, id=None, custom_column_details=None):
#         found_objects = list(CustomColumnModel.objects(**{"id": id}))
#         if len(found_objects) > 0:
#             custom_column_details["id"] = id
#             custom_column = CustomColumnModel(**custom_column_details)
#             custom_column.update(**custom_column_details)
#             return UpdateCustomColumnMutation(custom_column=custom_column, modified=True)
#         return UpdateCustomColumnMutation(custom_column=id, modified=False)


# class DeleteCustomColumnnMutation(graphene.Mutation):
#     id = graphene.ID(required=True)
#     deleted = graphene.Boolean()

#     class Arguments:
#         id = graphene.ID(required=True)

#     @permissions_checker(PermissionsType(allow_any="user"))
#     def mutate(parent, info, id=None):
#         found_objects = list(CustomColumnModel.objects(**{"id": id}))
#         if len(found_objects) > 0:
#             CustomColumnModel.delete(found_objects[0])
#             return DeleteCustomColumnnMutation(id=id, deleted=True)
#         return DeleteCustomColumnnMutation(id=id, deleted=False)
# Resolvers


# class CustomColumnsListsResolver(graphene.ObjectType):
#     custom_columns_list = MongoengineConnectionField(CustomColumn)

#     @permissions_checker(PermissionsType(allow_any="user"))
#     def resolve_custom_columns_list(parent, info, *args, **kwargs):
#         MongoengineConnectionField(CustomColumn, *args)
