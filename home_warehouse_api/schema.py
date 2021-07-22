import os
from dotenv import load_dotenv
import graphene

from mongoengine import connect
from pymongo.errors import ConnectionFailure

# Models
from models.custom_columns import (
    CreateCustomColumnMutation,
    CustomColumn,
    CustomColumnsListsResolver,
    DeleteCustomColumnnMutation,
    UpdateCustomColumnMutation
)

from models.location import (
    CreateLocationMutation,
    LocationsListsResolver,
    UpdateLocationMutation,
    DeleteLocationMutation,
    Location
)

from models.product import (
    CreateProductMutation,
    ProductsListFilteredResolver,
    UpdateProductMutation,
    DeleteProductMutation,
    ProductsListsResolver,
    Product
)

from models.raports import (
    CreateRaportMutation,
    DeleteRaportMutation,
    RaportsListsResolver,
    UpdateRaportMutation
)

from models.account import (
    AccountResolvers,
    AccountsListsResolver,
    CreateAccountMutation,
    UpdateAccountMutation,
    DeleteAccountMutation,
    Account
)

from resolvers.authentication import AuthenticationResolvers

load_dotenv()

# Connect with database
try:
    connection = connect(
        alias="default",
        host=os.getenv("DB_URL"),
        serverSelectionTimeoutMS=3000
    )
    connection = connection.server_info()
    print("Connected with databaase")
except ConnectionFailure as error:
    print(error)


class Mutation(graphene.ObjectType):
    create_location = CreateLocationMutation.Field()
    modify_location = UpdateLocationMutation.Field()
    delete_location = DeleteLocationMutation.Field()

    create_custom_column = CreateCustomColumnMutation.Field()
    modify_custom_column = UpdateCustomColumnMutation.Field()
    delete_custom_column = DeleteCustomColumnnMutation.Field()

    create_product = CreateProductMutation.Field()
    modify_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()

    create_account = CreateAccountMutation.Field()
    modify_account = UpdateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()

    create_raport = CreateRaportMutation.Field()
    modify_raport = UpdateRaportMutation.Field()
    delete_raport = DeleteRaportMutation.Field()


class Query(
    CustomColumnsListsResolver,
    ProductsListsResolver,
    ProductsListFilteredResolver,
    LocationsListsResolver,
    RaportsListsResolver,
    AccountsListsResolver,
    AccountResolvers,
    AuthenticationResolvers,
    graphene.ObjectType
    ):
    pass

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        CustomColumn,
        Location,
        Product,
        Account,
    ])
