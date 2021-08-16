import graphene
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import IntField, ListField, ReferenceField, StringField
from models.common import BuildInputBoilerplate
from node import CustomNode, EmbeddedNode


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


class elementsAllowedType(graphene.Enum):
    PRODUCTS = 'products'
    LOCATIONS = 'locations'


class dataTypesType(graphene.Enum):
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    SELECT = 'select'


class CustomColumnValueInput(graphene.InputObjectType):
    '''CustomColumnValue input for graphene'''
    custom_column = graphene.ID(required=True)
    value = graphene.String()


class CustomColumnInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            index = graphene.Int(required=self.creating_new)
            name = graphene.String(required=self.creating_new)
            elements_allowed = graphene.InputField(graphene.List(elementsAllowedType), required=self.creating_new)
            values = graphene.InputField(graphene.List(graphene.String), required=self.creating_new)
            data_type = graphene.InputField(dataTypesType, required=self.creating_new)
        return Input


CustomColumnInputType = CustomColumnInput().BuildInput()
CreateCustomColumnInputType = CustomColumnInput(True).BuildInput()
