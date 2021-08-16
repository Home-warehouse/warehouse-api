import graphene

from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, EmbeddedDocumentListField, IntField,
    ListField, ReferenceField, StringField
)

from middlewares.permissions import PermissionsType, permissions_checker
from models.common import BuildInputBoilerplate, FilterRaportInput, SortRaportInput
from models.custom_columns import CustomColumnModel
from node import CustomNode, EmbeddedNode

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


# Mutations

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


class CreateRaportMutation(graphene.Mutation):
    raport = graphene.Field(Raport, required=True)

    class Arguments:
        raport_details = CreateRaportInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, raport_details=None):
        raport = RaportModel(
            raport_name=raport_details.raport_name,
            description=raport_details.description,
            show_custom_columns=raport_details.show_custom_columns,
            sort_by=raport_details.sort_by,
            filter_by=raport_details.filter_by,
            short_results=raport_details.short_results
        )
        raport.save()
        return CreateRaportMutation(raport=raport)


class UpdateRaportMutation(graphene.Mutation):
    raport = graphene.Field(Raport, required=True)
    modified = graphene.Boolean(required=True)

    class Arguments:
        raport_details = RaportInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, raport_details=None):
        found_objects = list(RaportModel.objects(**{"id": raport_details['id']}))
        if len(found_objects) > 0:
            raport_details["id"] = raport_details['id']
            raport = RaportModel(**raport_details)
            raport.update(**raport_details)
            return UpdateRaportMutation(raport=raport, modified=True)
        return UpdateRaportMutation(raport=raport_details['id'], modified=False)


class DeleteRaportMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(RaportModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            RaportModel.delete(found_objects[0])
            return DeleteRaportMutation(id=id, deleted=True)
        return DeleteRaportMutation(id=id, deleted=False)

# Resolvers


class RaportsListsResolver(graphene.ObjectType):
    raports_list = MongoengineConnectionField(Raport)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_raports_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Raport, *args)
