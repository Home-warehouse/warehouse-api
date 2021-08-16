import graphene
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.fields import EmbeddedDocumentListField, StringField
from models.common import BuildInputBoilerplate
from models.custom_columns import CustomColumnValueInput, CustomColumnValueModel
from node import CustomNode


# Models


class ProductModel(Document):
    '''Product model for mongoengine'''
    meta = {"collection": "products"}
    product_name = StringField()
    description = StringField()
    icon = StringField()
    custom_columns = EmbeddedDocumentListField(CustomColumnValueModel)


# Types


class Product(MongoengineObjectType):
    '''Product type for mongoengine'''
    class Meta:
        '''Product mongo object meta settings'''
        model = ProductModel
        interfaces = (CustomNode,)


class ProductInput(graphene.InputObjectType):
    '''Product input for graphene'''
    id = graphene.ID()


class ProductInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            product_name = graphene.String(required=self.creating_new)
            description = graphene.String()
            icon = graphene.String()
            custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput))
        return Input


ProductInputType = ProductInput().BuildInput()
CreateProductInputType = ProductInput(True).BuildInput()
