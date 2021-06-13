import os
from dotenv import load_dotenv
import graphene
from graphene.relay import Node

from mongoengine import connect
from pymongo.errors import ConnectionFailure

# Models

from models.location import (
    CreateLocationMutation,
    LocationsListsResolver,
    UpdateLocationMutation,
    DeleteLocationMutation,
    Location
)
from models.product import (
    CreateProductMutation,
    UpdateProductMutation,
    DeleteProductMutation,
    ProductsListsResolver,
    Product
)
from models.default_product import (
    CreateDefaultProductMutation,
    DefaultProduct,
    DefaultProductsListsResolver
)
from models.product_price import (
    CreateProductPriceMutation,
    DefaultPricesListsResolver,
    UpdateProductPriceMutation,
    DeleteProductPriceMutation,
    ProductPrice
)
from models.account import (
    AccountssListsResolver,
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

    create_product = CreateProductMutation.Field()
    modify_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()

    create_default_product = CreateDefaultProductMutation.Field()

    create_product_price = CreateProductPriceMutation.Field()
    modify_product_price = UpdateProductPriceMutation.Field()
    delete_product_price = DeleteProductPriceMutation.Field()

    create_account = CreateAccountMutation.Field()
    modify_account = UpdateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()


class Query(
    DefaultPricesListsResolver,
    DefaultProductsListsResolver,
    ProductsListsResolver,
    LocationsListsResolver,
    AccountssListsResolver,
    AuthenticationResolvers,
    graphene.ObjectType
    ):
    pass

    node = Node.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        Location,
        Product,
        ProductPrice,
        DefaultProduct,
        Account,
    ])
