from os import getenv
import graphene
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.fields import GenericReferenceField, ListField, StringField
from models.common import BuildInputBoilerplate
from models.raport import RaportModel
from node import CustomNode
import enum

# Models


class AutomatizationModel(Document):
    '''Automatization model for mongoengine'''
    meta = {"collection": "automatizations"}
    app = StringField()
    automatization_name = StringField()
    config = StringField()
    element_integrated = GenericReferenceField(choices=['RaportModel'])
    elements_monitored = ListField(StringField())


# Types


class Automatization(MongoengineObjectType):
    '''Automatization type for mongoengine'''
    class Meta:
        model = AutomatizationModel
        interfaces = (CustomNode,)


class integratedElementType(graphene.Enum):
    RAPORT = 'RAPORT'


class monitoredElementType(graphene.Enum):
    PRODUCT = 'PRODUCT'
    LOCATION = 'LOCATION'
    CUSTOM_COLUMN = 'CUSTOM_COLUMN'


appTypes = [('None', 'None')]
if getenv("INTEGRATION_EVERNOTE_TOKEN"):
    appTypes.append(('EVERNOTE', 'EVERNOTE'))


def generateAppTypeGraphene():

    if(len(appTypes)):
        class appTypeGraphene(graphene.Enum):

            class Meta():
                enum = enum.Enum('appTypes', dict(appTypes))

        return appTypeGraphene


appTypeGraphene = generateAppTypeGraphene()


class ElementInput(graphene.InputObjectType):
    '''Element input for graphene'''
    elementType = graphene.InputField(integratedElementType, required=True)
    elementID = graphene.ID(required=True)


class AutomatizationInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            automatization_name = graphene.String(required=self.creating_new, description="Automatization name")
            app = graphene.InputField(appTypeGraphene, required=self.creating_new,
                                      description="Integration app used for automatization")
            config = graphene.String(required=self.creating_new, description="Integration configuration as JSON string")
            element_integrated = graphene.InputField(ElementInput, required=self.creating_new)
            elements_monitored = graphene.InputField(graphene.List(monitoredElementType), required=self.creating_new)
        return Input


AutomatizationInputType = AutomatizationInput().BuildInput()
CreateAutomatizationInputType = AutomatizationInput(True).BuildInput()
