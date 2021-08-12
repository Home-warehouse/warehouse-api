import graphene

from graphene_mongo import MongoengineObjectType

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import ListField, ReferenceField, StringField

from resolvers.node import CustomNode, EmbeddedNode

# Models


class CustomColumnModel(Document):
    '''CustomColumn model for mongoengine'''
    meta = {"collection": "custom_columns"}
    name = StringField(required=True)
    elements_allowed = ListField(StringField())
    values = ListField(StringField())
    data_type = StringField()


class CustomColumnValueModel(EmbeddedDocument):
    '''CustomColumnValue model for mongoengine'''
    custom_column = ReferenceField(CustomColumnModel)
    value = StringField()


# Types
class CustomColumn(MongoengineObjectType):
    '''CustomColumn type for mongoengine'''

    class Meta:
        model = CustomColumnModel
        interfaces = (CustomNode,)


class CustomColumnValue(MongoengineObjectType):
    '''CustomColumnValue type for mongoengine'''
    class Meta:
        model = CustomColumnValueModel
        interfaces = (EmbeddedNode, )


# Graphene Input


class CustomColumnValueInput(graphene.InputObjectType):
    '''CustomColumnValue input for graphene'''
    custom_column = graphene.ID(required=True)
    value = graphene.String()


class CustomColumnInput(graphene.InputObjectType):
    '''CustomColumn input for graphene'''
    id = graphene.ID()
    name = graphene.String(required=True)
    elements_allowed = graphene.List(graphene.String, required=True)
    values = graphene.List(graphene.String, required=True)
    data_type = graphene.String(required=True)
