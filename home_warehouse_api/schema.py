import graphene
from graphene.relay import Node

from graphene_mongo import MongoengineConnectionField
from mongoengine import connect
from pymongo.errors import ConnectionFailure

from models.location import (
    CreateLocationMutation,
    UpdateLocationMutation,
    DeleteLocationMutation,
    Location
)
from models.product import (
    CreateProductMutation,
    UpdateProductMutation,
    DeleteProductMutation,
    Product
)
from models.product_price import (
    CreateProductPriceMutation,
    UpdateProductPriceMutation,
    DeleteProductPriceMutation,
    ProductPrice
)
from models.account import (
    CreateAccountMutation,
    UpdateAccountMutation,
    DeleteAccountMutation,
    Account
)

# Connect with database
try:
    connection = connect(
        alias="default",
        host="mongodb://127.0.0.1:27017/home-warehouse",
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

    create_product_price = CreateProductPriceMutation.Field()
    modify_product_price = UpdateProductPriceMutation.Field()
    delete_product_price = DeleteProductPriceMutation.Field()

    create_account = CreateAccountMutation.Field()
    modify_account = UpdateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()


class Query(graphene.ObjectType):
    node = Node.Field()

    locations_list = MongoengineConnectionField(Location)
    location = graphene.Field(Location)

    products_list = MongoengineConnectionField(Product)
    product = graphene.Field(Product)

    products_prices_list = MongoengineConnectionField(ProductPrice)
    product_price = graphene.Field(ProductPrice)

    accounts_list = MongoengineConnectionField(Account)
    account = graphene.Field(Account)


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        Location,
        Product])
