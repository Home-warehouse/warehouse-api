import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import ListField, StringField

from middlewares.permissions import PermissionsType, permissions_checker

# Models


class LocationModel(Document):
    meta = {"collection": "locations"}
    parent_id = ObjectIdField()
    location_name = StringField(required=True)
    description = StringField()
    products = ListField(ObjectIdField())

# Types


class Location(MongoengineObjectType):

    class Meta:
        model = LocationModel
        interfaces = (Node,)

# Mutations


class LocationInput(graphene.InputObjectType):
    id = graphene.ID()
    parent_id = graphene.ID()
    location_name = graphene.String()
    description = graphene.String()
    products = graphene.List(graphene.ID)


class CreateLocationMutation(graphene.Mutation):
    location = graphene.Field(Location)

    class Arguments:
        location_details = LocationInput(required=True)

    def mutate(parent, info, location_details=None):
        location = LocationModel(
            parent_id=location_details.parent_id,
            location_name=location_details.location_name,
            description=location_details.description,
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
        foundObjects = list(LocationModel.objects(
            **{"id": from_global_id(id)[1]}))
        if(len(foundObjects) > 0):
            location_details["id"] = from_global_id(id)[1]
            location = LocationModel(**location_details)
            location.update(**location_details)
            return UpdateLocationMutation(location=location, modified=True)
        else:
            return UpdateLocationMutation(location=id, modified=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

class DeleteLocationMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(LocationModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            LocationModel.delete(found_objects[0])
            return DeleteLocationMutation(
                id=from_global_id(id)[1], deleted=True)
        return DeleteLocationMutation(
            id=from_global_id(id)[1], deleted=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

# Resolvers


class LocationsListsResolver(graphene.ObjectType):
    locations = MongoengineConnectionField(Location)

    def resolve_locations(parent, info):
        MongoengineConnectionField(Location)

    resolve_locations = permissions_checker(
        resolve_locations, PermissionsType(allow_any="user"))
