from models.common import BuildInputBoilerplate
import graphene
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.fields import BooleanField, EmbeddedDocumentField, ListField, ReferenceField, StringField
from mongoengine.queryset.base import PULL
from models.custom_column import CustomColumnValueInput, CustomColumnValueModel
from node import CustomNode


# Models


class LocationModel(Document):
    '''Location model for mongoengine'''
    meta = {"collection": "locations"}
    root = BooleanField()
    location_name = StringField()
    description = StringField()
    products = ListField(ReferenceField(
        'ProductModel', reverse_delete_rule=PULL))
    childrens = ListField(ReferenceField(
        'LocationModel', reverse_delete_rule=PULL))
    custom_columns = ListField(EmbeddedDocumentField(CustomColumnValueModel))


# Types


class Location(MongoengineObjectType):
    '''Location type for mongoengine'''
    class Meta:
        model = LocationModel
        interfaces = (CustomNode, )
        filter_fields = {
            'id': ['exact'],
            'root': ['exact']
        }


class LocationInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            root = graphene.Boolean()
            location_name = graphene.String(required=self.creating_new)
            description = graphene.String()
            products = graphene.InputField(graphene.List(graphene.ID, required=self.creating_new))
            childrens = graphene.InputField(graphene.List(graphene.ID,  required=self.creating_new))
            custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput, required=self.creating_new))
        return Input


LocationInputType = LocationInput().BuildInput()
CreateLocationInputType = LocationInput(True).BuildInput()
