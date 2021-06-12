import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import StringField

from middlewares.permissions import PermissionsType, permissions_checker

# Models


class DefaultProductModel(Document):
    meta = {"collection": "default_products"}
    product_name = StringField()
    icon = StringField()
    price_id = ObjectIdField()
    custom_columns = StringField()

# Types


class DefaultProduct(MongoengineObjectType):

    class Meta:
        model = DefaultProductModel
        interfaces = (Node,)

# Mutations


class DefaultProductInput(graphene.InputObjectType):
    id = graphene.ID()
    product_name = graphene.String(required=True)
    icon = graphene.String()
    price_id = graphene.ID()
    custom_columns = graphene.JSONString()


class CreateDefaultProductMutation(graphene.Mutation):
    defaultProduct = graphene.Field(DefaultProduct)
    created = graphene.Boolean()

    class Arguments:
        default_product_details = DefaultProductInput(required=True)

    def mutate(parent, info, default_product_details=None):
        default_product = DefaultProductModel(
            product_name=default_product_details.product_name,
            icon=default_product_details.icon,
            price_id=default_product_details.price_id,
            custom_columns=default_product_details.custom_columns
        )
        default_product.save()

        return CreateDefaultProductMutation(defaultProduct=default_product, created=True)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="admin"))

# Resolvers


class DefaultProductsListsResolver(graphene.ObjectType):
    default_products = MongoengineConnectionField(DefaultProduct)

    def resolve_default_products(parent, info):
        MongoengineConnectionField(DefaultProduct)

    resolve_default_products = permissions_checker(
        resolve_default_products, PermissionsType(allow_any="user"))
