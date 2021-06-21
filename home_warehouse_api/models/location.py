import graphene
from graphene.types.scalars import Boolean

from graphene_mongo import MongoengineObjectType

from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.fields import BooleanField, EmbeddedDocumentField, ListField, ReferenceField, StringField
from mongoengine.queryset.base import PULL

from bson import ObjectId

from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_columns import CustomColumnValueInput, CustomColumnValueModel
from models.product import ProductModel
from resolvers.node import CustomNode

# Models


class LocationModel(Document):
    meta = {"collection": "locations"}
    root = BooleanField()
    location_name = StringField(required=True)
    description = StringField()
    products = ListField(ReferenceField(
        ProductModel, reverse_delete_rule=PULL))
    childrens = ListField(ReferenceField(
        'LocationModel', reverse_delete_rule=PULL))
    custom_columns = ListField(EmbeddedDocumentField(CustomColumnValueModel))

# Types


class Location(MongoengineObjectType):

    class Meta:
        model = LocationModel
        interfaces = (CustomNode, )
        filter_fields = {
            'id': ['exact'],
            'root': ['exact'],
            'location_name': ['exact', 'icontains', 'istartswith']
        }

# Mutations


class LocationInput(graphene.InputObjectType):
    id = graphene.ID()
    root = graphene.Boolean()
    location_name = graphene.String()
    description = graphene.String()
    products = graphene.List(graphene.ID)
    childrens = graphene.List(graphene.ID)
    custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput))
    


class CreateLocationMutation(graphene.Mutation):
    location = graphene.Field(Location)

    class Arguments:
        location_details = LocationInput(required=True)

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
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class UpdateLocationMutation(graphene.Mutation):
    id = graphene.String(required=True)
    location = graphene.Field(Location)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        location_details = LocationInput(required=True)

    def mutate(parent, info, id=None, location_details=None):
        found_objects = list(LocationModel.objects(**{"id": id}))
        if len(found_objects) == 1:
            if location_details.products:
                for index, item in enumerate(location_details.products):
                    location_details.products[index] = ObjectId(
                        location_details.products[index])
                location_details.products.extend(found_objects[0].products)

            if location_details.childrens:
                for index, item in enumerate(location_details.childrens):
                    location_details.childrens[index] = ObjectId(
                        location_details.childrens[index])
                location_details.childrens.extend(found_objects[0].childrens)

            location_details["id"] = id
            location = LocationModel(**location_details)
            location.update(**location_details)
            return UpdateLocationMutation(location=location, modified=True)
        return UpdateLocationMutation(location=id, modified=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class DeleteLocationMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(LocationModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            LocationModel.delete(found_objects[0])
            return DeleteLocationMutation(id=id, deleted=True)
        return DeleteLocationMutation(id=id, deleted=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

# Resolvers


class LocationsListsResolver(graphene.ObjectType):
    locations_list = MongoengineConnectionField(Location)

    def resolve_locations_list(parent, info, **kwargs):
        MongoengineConnectionField(Location)

    resolve_locations_list = permissions_checker(
        resolve_locations_list, PermissionsType(allow_any="user"))
