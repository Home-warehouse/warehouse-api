import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.fields import StringField

from services.hash_password import hash_password

# Models


class AccountModel(Document):
    meta = {"collection": "accounts"}
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField()
    password = StringField()

# Types


class Account(MongoengineObjectType):

    class Meta:
        model = AccountModel
        interfaces = (Node,)

# Mutations


class AccountInput(graphene.InputObjectType):
    id = graphene.ID()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()


class CreateAccountMutation(graphene.Mutation):
    account = graphene.Field(Account)

    class Arguments:
        account_details = AccountInput(required=True)

    def mutate(parent, info, account_details):
        account = AccountModel(
            email=account_details.email,
            first_name=account_details.first_name,
            last_name=account_details.last_name,
            password=hash_password(account_details.password),
        )
        account.save()

        return CreateAccountMutation(account=account)


class UpdateAccountMutation(graphene.Mutation):
    id = graphene.String(required=True)
    account = graphene.Field(Account)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        account_details = AccountInput(required=True)

    def mutate(parent, info, id=None, account_details=None):
        found_objects = list(AccountModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            account_details["id"] = from_global_id(id)[1]
            account = AccountModel(**account_details)
            account.update(**account_details)
            return UpdateAccountMutation(account=account, modified=True)
        return UpdateAccountMutation(account=id, modified=False)


class DeleteAccountMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(AccountModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            AccountModel.delete(found_objects[0])
            return DeleteAccountMutation(
                id=from_global_id(id)[1], deleted=True)
        return DeleteAccountMutation(
            id=from_global_id(id)[1], deleted=False)
