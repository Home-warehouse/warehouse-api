import graphene

from graphene_mongo import MongoengineObjectType
from graphene_mongo.fields import MongoengineConnectionField

from mongoengine import Document
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField

from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_columns import CustomColumnValueInput, CustomColumnValueModel
from resolvers.node import CustomNode

# Models

class ProductModel(Document):
    meta = {"collection": "products"}
    product_name = StringField()
    icon = StringField()
    custom_columns = ListField(EmbeddedDocumentField(CustomColumnValueModel))


# Types
class Product(MongoengineObjectType):

    class Meta:
        model = ProductModel
        interfaces = (CustomNode,)
        filter_fields = {
            'product_name': ['exact', 'icontains', 'istartswith']
        }


# Mutations

class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    product_name = graphene.String(required=True)
    icon = graphene.String()
    custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput))

class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(Product)

    class Arguments:
        product_details = ProductInput(required=True)

    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            icon=product_details.icon,
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
        found_objects = list(ProductModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            product_details["id"] = id
            product = ProductModel(**product_details)
            product.update(**product_details)
            return UpdateProductMutation(product=product, modified=True)
        return UpdateProductMutation(product=id, modified=False)
    mutate = permissions_checker(fn=mutate, permissions=PermissionsType(allow_any="user"))


class DeleteProductMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(parent, info, id=None):
        found_objects = list(ProductModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            ProductModel.delete(found_objects[0])
            return DeleteProductMutation(id=id, deleted=True)
        return DeleteProductMutation(id=id, deleted=False)

    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))

# Resolvers


class ProductsListsResolver(graphene.ObjectType):
    products_list = MongoengineConnectionField(Product)

    def resolve_products_list(parent, info):
        MongoengineConnectionField(Product)

    resolve_products_list = permissions_checker(
        resolve_products_list, PermissionsType(allow_any="user"))
