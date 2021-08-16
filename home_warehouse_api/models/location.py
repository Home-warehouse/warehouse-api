import graphene

from graphene_mongo import MongoengineObjectType

from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.fields import BooleanField, EmbeddedDocumentField, ListField, ReferenceField, StringField
from mongoengine.queryset.base import PULL

from bson import ObjectId

from middlewares.permissions import PermissionsType, permissions_checker
from models.common import BuildInputBoilerplate
from models.custom_columns import CustomColumnValueInput, CustomColumnValueModel
from models.product import ProductModel
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

# Mutations


class LocationInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            root = graphene.Boolean()
            location_name = graphene.String(required=self.creating_new)
            description = graphene.String(required=self.creating_new)
            products = graphene.InputField(graphene.List(graphene.ID, required=self.creating_new), required=self.creating_new)
            childrens = graphene.InputField(graphene.List(graphene.ID, required=self.creating_new), required=self.creating_new)
            custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput, required=self.creating_new), required=self.creating_new)
        return Input


LocationInputType = LocationInput().BuildInput()
CreateLocationInputType = LocationInput(True).BuildInput()


class CreateLocationMutation(graphene.Mutation):
    location = graphene.Field(Location, required=True)

    class Arguments:
        location_details = CreateLocationInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, location_details=None):
        location = LocationModel(
            root=location_details.root,
            location_name=location_details.location_name,
            description=location_details.description,
            products=location_details.products,
            childrens=location_details.childrens,
            custom_columns=location_details.custom_columns
        )
        location.save()

        return CreateLocationMutation(location=location)


class UpdateLocationMutation(graphene.Mutation):
    location = graphene.Field(Location, required=True)
    modified = graphene.Boolean(required=True)

    class Arguments:
        location_details = LocationInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, location_details=None):
        found_objects = list(LocationModel.objects(**{"id": location_details['id']}))
        if len(found_objects) == 1:
            if location_details.products:
                for index in range(len(location_details.products)):
                    location_details.products[index] = ObjectId(location_details.products[index])
                location_details.products.extend(found_objects[0].products)

            if location_details.childrens:
                for index in range(len(location_details.childrens)):
                    location_details.childrens[index] = ObjectId(location_details.childrens[index])
                location_details.childrens.extend(found_objects[0].childrens)

            location_details["id"] = location_details['id']
            location = LocationModel(**location_details)
            location.update(**location_details)
            return UpdateLocationMutation(location=location, modified=True)
        return UpdateLocationMutation(location=location_details['id'], modified=False)


class DeleteLocationMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(LocationModel.objects(**{"id": id}))
        products = list(found_objects[0].products)
        parsed = list(map(lambda doc: doc.id, products))
        if len(found_objects) > 0:
            ProductModel.objects(id__in=parsed).delete()
            LocationModel.delete(found_objects[0])
            return DeleteLocationMutation(id=id, deleted=True)
        return DeleteLocationMutation(id=id, deleted=False)

# Resolvers


class LocationsListsResolver(graphene.ObjectType):
    locations_list = MongoengineConnectionField(Location)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_locations_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Location, *args)
