import graphene
from graphene.types.json import JSONString

from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.fields import DictField, GenericReferenceField, ListField, StringField

from middlewares.permissions import PermissionsType, permissions_checker
# from models.location import LocationModel
# from models.product import ProductModel
from models.raports import RaportModel
from resolvers.node import CustomNode

# Models


class AutomatizationModel(Document):
    '''Automatization model for mongoengine'''
    meta = {"collection": "automatizations"}
    app = StringField()
    name = StringField()
    config = StringField()
    element_integrated = GenericReferenceField(choices=[RaportModel])
    elements_monitored = ListField(StringField())

# Types


class Automatization(MongoengineObjectType):
    '''Automatization type for mongoengine'''
    class Meta:
        model = AutomatizationModel
        interfaces = (CustomNode,)

# Mutations


class elementType(graphene.Enum):
    PRODUCT = 'product'
    LOCATION = 'location'
    RAPORT = 'raport'


class appType(graphene.Enum):
    EVERNOTE = 'evernote'


class ElementInput(graphene.InputObjectType):
    '''Element input for graphene'''
    elementType = graphene.InputField(elementType, required=True)
    elementID = graphene.ID(required=True)


class AutomatizationInput(graphene.InputObjectType):
    '''Automatization input for graphene'''
    id = graphene.ID()
    name = graphene.String(required=True, description="Automatization name")
    app = graphene.InputField(appType, required=True, description="Integration app used for automatization")
    config = graphene.String(required=True, description="Integration configuration as JSON string")
    element_integrated = graphene.InputField(ElementInput, required=True)
    elements_monitored = graphene.InputField(graphene.List(elementType),
                                             required=True, description="One of: 'product', 'localization; ")


def findElementReference(elementType: str, elementID: str):
    if elementType == "raport":
        return RaportModel.objects(**{"id": elementID})[0]
    # if elementType == "product":
    #     return ProductModel.objects(**{"id": elementID})[0]
    # elif elementType == "location":
    #     return LocationModel.objects(**{"id": elementID})[0]


class CreateAutomatizationMutation(graphene.Mutation):
    automatization = graphene.Field(Automatization)

    class Arguments:
        automatization_details = AutomatizationInput(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, automatization_details=None):

        element_integrated = findElementReference(
            automatization_details.element_integrated.elementType,
            automatization_details.element_integrated.elementID
        )

        automatization = AutomatizationModel(
            app=automatization_details.app,
            name=automatization_details.name,
            config=automatization_details.config,
            element_integrated=element_integrated,
            elements_monitored=automatization_details.elements_monitored,
        )
        automatization.save()
        return CreateAutomatizationMutation(automatization=automatization)


class DeleteAutomatizationMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(AutomatizationModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            AutomatizationModel.delete(found_objects[0])
            return DeleteAutomatizationMutation(id=id, deleted=True)
        return DeleteAutomatizationMutation(id=id, deleted=False)

# Resolvers


class AutomatizationsListResolver(graphene.ObjectType):
    automatizations_list = MongoengineConnectionField(Automatization)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_automatizations_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Automatization, *args)
