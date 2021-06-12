import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import StringField

from middlewares.permissions import PermissionsType, permissions_checker

# Models


class ProductModel(Document):
    meta = {"collection": "products"}
    product_name = StringField()
    icon = StringField()
    price_id = ObjectIdField()
    custom_columns = StringField()


# Types
class Product(MongoengineObjectType):

    class Meta:
        model = ProductModel
        interfaces = (Node,)
        filter_fields = {
            'product_name': ['exact', 'icontains', 'istartswith']
        }


# Mutations
class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    product_name = graphene.String(required=True)
    icon = graphene.String()
    price_id = graphene.ID()
    custom_columns = graphene.JSONString()


class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(Product)

    class Arguments:
        product_details = ProductInput(required=True)

    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            icon=product_details.icon,
            price_id=product_details.price_id,
            custom_columns=product_details.custom_columns
        )
        product.save()
        return CreateProductMutation(product=product)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class UpdateProductMutation(graphene.Mutation):
    id = graphene.String(required=True)
    product = graphene.Field(Product)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        product_details = ProductInput(required=True)

    def mutate(parent, info, id=None, product_details=None):
        found_objects = list(ProductModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            product_details["id"] = from_global_id(id)[1]
            product = ProductModel(**product_details)
            product.update(**product_details)
            return UpdateProductMutation(product=product, modified=True)
        return UpdateProductMutation(product=id, modified=False)
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


class DeleteProductMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(ProductModel.objects(
            **{"id": from_global_id(id)[1]}))
        if len(found_objects) > 0:
            ProductModel.delete(found_objects[0])
            return DeleteProductMutation(
                id=from_global_id(id)[1], deleted=True)
        return DeleteProductMutation(
            id=from_global_id(id)[1], deleted=False)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

# Resolvers


class ProductsListsResolver(graphene.ObjectType):
    products = MongoengineConnectionField(Product)

    def resolve_products(parent, info):
        MongoengineConnectionField(Product)

    resolve_products = permissions_checker(
        resolve_products, PermissionsType(allow_any="user"))
