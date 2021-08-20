from os import getenv
import graphene
from mongoengine import connect
from pymongo.errors import ConnectionFailure

# Models
from models.custom_column import CustomColumn
from models.product import Product
from models.location import Location
from models.account import Account
from models.raport import Raport
from models.automatization import Automatization


# Resolvers / mutations
from resolvers.raport import (
    CreateRaportMutation,
    DeleteRaportMutation,
    RaportsListsResolver,
    UpdateRaportMutation
)
from resolvers.account import (
    AccountResolvers,
    AccountsListsResolver,
    CreateAccountMutation,
    UpdateAccountMutation,
    DeleteAccountMutation
)
from resolvers.automatization import (
    AutomatizationsListResolver,
    CreateAutomatizationMutation,
    DeleteAutomatizationMutation
)
from resolvers.location import (
    CreateLocationMutation,
    LocationsListsResolver,
    UpdateLocationMutation,
    DeleteLocationMutation
)
from resolvers.product import (
    CreateProductMutation,
    UpdateProductMutation,
    DeleteProductMutation,
    ProductsListsResolver,
)
from resolvers.custom_column import (
    CreateCustomColumnMutation,
    CustomColumnsListsResolver,
    DeleteCustomColumnnMutation,
    UpdateCustomColumnMutation
)
from resolvers.products_filter import ProductsListFilteredResolver
from resolvers.authentication import AuthenticationResolvers
from resolvers.integration import IntegrationsResolvers
from services.generate_admin_account import create_admin_account


# Connect with database
try:
    connection = connect(
        alias="default",
        host=getenv("DB_URL"),
        serverSelectionTimeoutMS=3000
    )
    connection = connection.server_info()
    print("Connected with database")
    create_admin_account()
except ConnectionFailure as error:
    print("Could not connect with database")
    print(error)


class Mutation(graphene.ObjectType):
    '''Mutations list'''
    create_product = CreateProductMutation.Field()
    modify_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()

    create_location = CreateLocationMutation.Field()
    modify_location = UpdateLocationMutation.Field()
    delete_location = DeleteLocationMutation.Field()

    create_custom_column = CreateCustomColumnMutation.Field()
    modify_custom_column = UpdateCustomColumnMutation.Field()
    delete_custom_column = DeleteCustomColumnnMutation.Field()

    create_account = CreateAccountMutation.Field()
    modify_account = UpdateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()

    create_raport = CreateRaportMutation.Field()
    modify_raport = UpdateRaportMutation.Field()
    delete_raport = DeleteRaportMutation.Field()

    create_automatization = CreateAutomatizationMutation.Field()
    delete_automatization = DeleteAutomatizationMutation.Field()


class Query(
    CustomColumnsListsResolver,
    ProductsListsResolver,
    ProductsListFilteredResolver,
    LocationsListsResolver,
    RaportsListsResolver,
    AccountsListsResolver,
    AccountResolvers,
    AuthenticationResolvers,
    IntegrationsResolvers,
    AutomatizationsListResolver,
    graphene.ObjectType
):
    '''Resolvers list'''
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[]
    )
