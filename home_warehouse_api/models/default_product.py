import graphene

from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import DateTimeField, FloatField, StringField

# Models


class DefaultProductModel(Document):
    meta = {"collection": "default_products"}
    name = StringField()
    icon = StringField()
    description = StringField()
    notes = StringField()
    expiration_date = DateTimeField()
    count = FloatField()
    default_count = FloatField()
    priceId = ObjectIdField()

# Types


class DefaultProduct(MongoengineObjectType):

    class Meta:
        model = DefaultProductModel
        interfaces = (Node,)

# Mutations


class DefaultProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    icon = graphene.String()
    description = graphene.String()
    notes = graphene.String()
    expiration_date = graphene.DateTime()
    count = graphene.Float()
    default_count = graphene.Float()
    priceId = graphene.ID()


class CreateDefaultProductMutation(graphene.Mutation):
    defaultProduct = graphene.Field(DefaultProduct)

    class Arguments:
        default_product_details = DefaultProductInput(required=True)

    def mutate(parent, default_product_details=None):
        default_product = DefaultProductModel(
            name=default_product_details.name,
            icon=default_product_details.icon,
            description=default_product_details.description,
            notes=default_product_details.notes,
            expiration_date=default_product_details.expiration_date,
            count=default_product_details.count,
            default_count=default_product_details.default_count,
            priceId=default_product_details.priceId
        )
        default_product.save()

        return CreateDefaultProductMutation(defaultProduct=default_product)
