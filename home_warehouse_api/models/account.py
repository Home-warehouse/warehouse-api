import graphene
from models.common import BuildInputBoilerplate
from node import CustomNode
from graphene_mongo import MongoengineObjectType
from mongoengine import Document
from mongoengine.fields import StringField


# Models


class AccountModel(Document):
    '''Account model for mongoengine'''
    meta = {"collection": "accounts"}
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    password = StringField()
    rank = StringField()


# Types


class Account(MongoengineObjectType):
    '''Account type for mongoengine'''
    class Meta:
        model = AccountModel
        interfaces = (CustomNode,)


class AccountInput(BuildInputBoilerplate):
    def BuildInput(self):
        class Input(graphene.InputObjectType):
            class Meta:
                name = self.name
            id = graphene.ID()
            email = graphene.String(required=self.creating_new)
            first_name = graphene.String(required=self.creating_new)
            last_name = graphene.String()
            password = graphene.String(required=self.creating_new)
            rank = graphene.String()

        return Input


AccountInputType = AccountInput().BuildInput()
CreateAccountInputType = AccountInput(True).BuildInput()
