import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import StringField

# Models


class LocationModel(Document):
    meta = {"collection": "locations"}
    parent_id = ObjectIdField()
    location_name = StringField(required=True)
    description = StringField()

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
