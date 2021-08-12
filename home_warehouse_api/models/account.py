import graphene
from graphene_mongo.fields import MongoengineConnectionField
from resolvers.node import CustomNode

from services.auth import jwt_authorize
from graphene_mongo import MongoengineObjectType

from mongoengine import Document
from mongoengine.fields import StringField

from services.hash_password import hash_password, verify_password

from starlette.requests import Request
from middlewares.permissions import PermissionsType, permissions_checker
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

# Mutations


class AccountInput(graphene.InputObjectType):
    '''Account input for graphene'''
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
        old_password = graphene.String()

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, account_details=None, old_password=None):
        request: Request = Request(info.context["request"])
        object_id = jwt_authorize(request.headers["authorization"])[
            "client_id"]

        found_objects = list(AccountModel.objects(
            **{"id": object_id}))
        if len(found_objects) > 0:
            # TODO: Dont allow to change rank if not admin
            if old_password:
                if not verify_password(found_objects[0]["password"], old_password):
                    return UpdateAccountMutation(account=object_id, modified=False)
                else:
                    account_details["password"] = hash_password(account_details.password)
                    print(account_details)
            account_details["id"] = object_id
            account = AccountModel(**account_details)
            account.update(**account_details)
            return UpdateAccountMutation(account=account, modified=True)
        return UpdateAccountMutation(account=object_id, modified=False)


class DeleteAccountMutation(graphene.Mutation):
    deleted = graphene.Boolean()

    @permissions_checker(PermissionsType(allow_any="user"))
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


# Resolvers


class AccountsListsResolver(graphene.ObjectType):
    accounts_list = MongoengineConnectionField(Account)

    @permissions_checker(PermissionsType(allow_any="admin"))
    def resolve_accounts_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Account, *args)


class MyAccountType(graphene.ObjectType):
    email = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()


def resolve_my_accout(parent, info):
    request: Request = Request(info.context["request"])
    decoded = jwt_authorize(request.headers["authorization"])
    found_objects = list(AccountModel.objects(**{"id": decoded["client_id"]}))
    if len(found_objects) > 0:
        account = found_objects[0]
        return MyAccountType(email=account["email"], firstName=account["first_name"], lastName=account["last_name"])


_my_account = graphene.Field(
    description='Get account information about your account',
    type=MyAccountType,
    resolver=resolve_my_accout,
    email=graphene.String(default_value=None),
)


class AccountResolvers(graphene.ObjectType):
    myAccount = _my_account
