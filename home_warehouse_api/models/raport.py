import graphene
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, EmbeddedDocumentListField, IntField,
    ListField, ReferenceField, StringField
)
from models.custom_column import CustomColumnModel
from node import CustomNode, EmbeddedNode
from models.common import BuildInputBoilerplate, FilterRaportInput, SortRaportInput


# Models


class SortRaportModel(EmbeddedDocument):
    '''SortRaport model for mongoengine'''
    custom_column = ReferenceField(CustomColumnModel)
    value = StringField()


class FilterRaportModel(EmbeddedDocument):
    '''FilterRaport model for mongoengine'''
    custom_column = ReferenceField(CustomColumnModel)
    comparison = StringField()
    value = StringField()


class RaportModel(Document):
    '''Raport model for mongoengine'''
    meta = {"collection": "raports"}
    raport_name = StringField()
    description = StringField()
    show_custom_columns = ListField(ReferenceField(CustomColumnModel))
    sort_by = EmbeddedDocumentField(SortRaportModel)
    filter_by = EmbeddedDocumentListField(FilterRaportModel)
    short_results = IntField()


# Types


class SortRaport(MongoengineObjectType):
    '''SortRaport type for mongoengine'''
    class Meta:
        model = SortRaportModel
        interfaces = (EmbeddedNode,)


class FilterRaport(MongoengineObjectType):
    '''FilterRaport type for mongoengine'''
    class Meta:
        model = FilterRaportModel
        interfaces = (EmbeddedNode,)


class Raport(MongoengineObjectType):
    '''Raport type for mongoengine'''
    class Meta:
        '''Raport mongo object meta settings'''
        model = RaportModel
        interfaces = (CustomNode,)
        filter_fields = {
            'id': ['exact']
        }


class RaportInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            raport_name = graphene.String(required=self.creating_new)
            description = graphene.String(required=self.creating_new)
            show_custom_columns = graphene.InputField(graphene.List(graphene.ID), required=self.creating_new)
            sort_by = graphene.InputField(SortRaportInput, required=self.creating_new)
            filter_by = graphene.InputField(graphene.List(FilterRaportInput), required=self.creating_new)
            short_results = graphene.Int()
        return Input


RaportInputType = RaportInput().BuildInput()
CreateRaportInputType = RaportInput(True).BuildInput()
