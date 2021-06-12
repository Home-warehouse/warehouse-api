from datetime import datetime

import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    FloatField,
    ListField,
    StringField
)

from middlewares.permissions import PermissionsType, permissions_checker
from models.default_product import DefaultProduct

# Models


class PriceRegistrationModel(EmbeddedDocument):
    shop_name = StringField()
    price = FloatField()
    notes = StringField()
    registration_date = DateTimeField(default=datetime.now)


class ProductPriceModel(Document):
    meta = {"collection": "products_prices"}
    product_name = StringField()
    shop_prices = ListField(EmbeddedDocumentField(PriceRegistrationModel))


# Types
class ProductPrice(MongoengineObjectType):

    class Meta:
        model = ProductPriceModel
        interfaces = (Node,)


class PriceRegistration(MongoengineObjectType):
    class Meta:
        model = PriceRegistrationModel
        interfaces = (Node,)


# Mutations
class PriceRegistrationInput(graphene.InputObjectType):
    shop_name = graphene.String()
    price = graphene.Float(required=True)
    notes = graphene.String()
    registration_date = graphene.DateTime()


class ProductPriceInput(graphene.InputObjectType):
    id = graphene.ID()
    product_name = graphene.String(required=True)
    shop_prices = graphene.List(PriceRegistrationInput)


class CreateProductPriceMutation(graphene.Mutation):
    productPrice = graphene.Field(ProductPrice)

    class Arguments:
        productPrice_details = ProductPriceInput(required=True)

    def mutate(parent, info, productPrice_details=None):
        productPrice = ProductPriceModel(
            product_name=productPrice_details.product_name,
            shop_prices=productPrice_details.shop_prices
        )
        productPrice.save()

        return CreateProductPriceMutation(productPrice=productPrice)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

class UpdateProductPriceMutation(graphene.Mutation):
    id = graphene.String(required=True)
    productPrice = graphene.Field(ProductPrice)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        productPrice_details = ProductPriceInput(required=True)

    def mutate(parent, info, id=None, productPrice_details=None):
        found_objects = list(ProductPriceModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            productPrice_details["id"] = from_global_id(id)[1]
            product_price = ProductPriceModel(**productPrice_details)
            product_price.update(**productPrice_details)
            return UpdateProductPriceMutation(
                productPrice=product_price, modified=True)
        else:
            return UpdateProductPriceMutation(productPrice=id, modified=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

class DeleteProductPriceMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(ProductPriceModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            ProductPriceModel.delete(found_objects[0])
            return DeleteProductPriceMutation(
                id=from_global_id(id)[1], deleted=True)
        return DeleteProductPriceMutation(
            id=from_global_id(id)[1], deleted=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))
    
# Resolvers


class DefaultPricesListsResolver(graphene.ObjectType):
    default_prices = MongoengineConnectionField(DefaultProduct)

    def resolve_default_prices(parent, info):
        MongoengineConnectionField(DefaultProduct)

    resolve_default_prices = permissions_checker(
        resolve_default_prices, PermissionsType(allow_any="user"))

