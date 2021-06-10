import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from graphql_relay.node.node import from_global_id

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import DateTimeField, FloatField, StringField

# Models


class ProductModel(Document):
    meta = {"collection": "products"}
    product_name = StringField()
    icon = StringField()
    description = StringField()
    notes = StringField()
    expiration_date = DateTimeField()
    count = FloatField()
    default_count = FloatField()
    priceId = ObjectIdField()


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
    description = graphene.String()
    notes = graphene.String()
    expiration_date = graphene.DateTime()
    count = graphene.Float()
    default_count = graphene.Float()
    priceId = graphene.ID()


class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(Product)

    class Arguments:
        product_details = ProductInput(required=True)

    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            icon=product_details.icon,
            description=product_details.description,
            notes=product_details.notes,
            expiration_date=product_details.expiration_date,
            count=product_details.count,
            default_count=product_details.default_count,
            priceId=product_details.priceId
        )
        product.save()
        return CreateProductMutation(product=product)


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
