import graphene

from graphene_mongo import MongoengineObjectType

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import IntField, ListField, ReferenceField, StringField

from resolvers.node import CustomNode, EmbeddedNode

# Models


class CustomColumnModel(Document):
    '''CustomColumn model for mongoengine'''
    meta = {"collection": "custom_columns"}
    name = StringField()
    index = IntField()
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
class elementsAllowedType(graphene.Enum):
    products = 'products'
    locations = 'locations'


class dataTypesType(graphene.Enum):
    text = 'text'
    number = 'number'
    date = 'date'
    select = 'select'


class CustomColumnValueInput(graphene.InputObjectType):
    '''CustomColumnValue input for graphene'''
    custom_column = graphene.ID(required=True)
    value = graphene.String()


class CustomColumnInput(graphene.InputObjectType):
    '''CustomColumn input for graphene'''
    id = graphene.ID()
    index = graphene.Int()
    name = graphene.String()
    elements_allowed = graphene.InputField(graphene.List(elementsAllowedType))
    values = graphene.List(graphene.String)
    data_type = graphene.InputField(dataTypesType)
