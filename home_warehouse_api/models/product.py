from graphene_mongo import MongoengineObjectType


from mongoengine import Document
from mongoengine.fields import EmbeddedDocumentListField, StringField

from models.custom_columns import CustomColumnValueModel
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
