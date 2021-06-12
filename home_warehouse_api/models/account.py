import graphene
from graphene_mongo.fields import MongoengineConnectionField

from services.auth import jwt_authorize
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql_relay.node.node import from_global_id, to_global_id

from mongoengine import Document
from mongoengine.fields import StringField

from services.hash_password import hash_password

from starlette.requests import Request
from middlewares.permissions import PermissionsType, permissions_checker
# Models


class AccountModel(Document):
    meta = {"collection": "accounts"}
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    password = StringField()
    rank = StringField()

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
    rank = graphene.String()


class CreateAccountMutation(graphene.Mutation):
    account = graphene.Field(Account)
    created = graphene.Boolean()

    class Arguments:
        account_details = AccountInput(required=True)

    def mutate(parent, info, account_details=None):
        found_objects = list(AccountModel.objects(
            **{"email": account_details.email}))
        if len(found_objects) == 0:
            account = AccountModel(
                email=account_details.email,
                first_name=account_details.first_name,
                last_name=account_details.last_name,
                password=hash_password(account_details.password),
                rank="user"
            )
            account.save()

            return CreateAccountMutation(account=account, created=True)
        return CreateAccountMutation(created=False)


class UpdateAccountMutation(graphene.Mutation):
    account = graphene.Field(Account)
    modified = graphene.Boolean()

    class Arguments:
        account_details = AccountInput(required=True)

    def mutate(parent, info, account_details=None):
        request: Request = Request(info.context["request"])
        object_id = jwt_authorize(request.headers["authorization"])[
            "client_id"]

        found_objects = list(AccountModel.objects(
            **{"id": object_id}))
        if len(found_objects) > 0:
            account_details["id"] = object_id
            account_details["password"] = hash_password(
                account_details.password)
            account = AccountModel(**account_details)
            account.update(**account_details)
            return UpdateAccountMutation(account=account, modified=True)
        return UpdateAccountMutation(account=to_global_id(object_id), modified=False)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class DeleteAccountMutation(graphene.Mutation):
    deleted = graphene.Boolean()

    def mutate(parent, info):
        request: Request = Request(info.context["request"])
        object_id = jwt_authorize(request.headers["authorization"])[
            "client_id"]

        found_objects = list(AccountModel.objects(
            **{"id": object_id}))

        if len(found_objects) > 0:
            AccountModel.delete(found_objects[0])
            return DeleteAccountMutation(deleted=True)
        return DeleteAccountMutation(deleted=False)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

# Resolvers


class AccountssListsResolver(graphene.ObjectType):
    accounts = MongoengineConnectionField(Account)

    def resolve_accounts(parent, info):
        MongoengineConnectionField(Account)

    resolve_accounts = permissions_checker(
        resolve_accounts, PermissionsType(allow_any="admin"))
