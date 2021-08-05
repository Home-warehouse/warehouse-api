import json
import graphene

from graphene_mongo.fields import MongoengineConnectionField
from graphene_mongo import MongoengineObjectType

from bson.objectid import ObjectId

from mongoengine import Document
from mongoengine.fields import EmbeddedDocumentListField, StringField
from middlewares.automatizations import automatizations_checker

from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_columns import CustomColumnModel, CustomColumnValueInput, CustomColumnValueModel
from resolvers.node import CustomNode
from models.common import product_filter_fields

# Models


class ProductModel(Document):
    '''Product model for mongoengine'''
    meta = {"collection": "products"}
    product_name = StringField()
    description = StringField()
    icon = StringField()
    custom_columns = EmbeddedDocumentListField(CustomColumnValueModel)


# Types
class Product(MongoengineObjectType):
    '''Product type for mongoengine'''
    class Meta:
        '''Product mongo object meta settings'''
        model = ProductModel
        interfaces = (CustomNode,)


# Mutations

class ProductInput(graphene.InputObjectType):
    '''Product input for graphene'''
    id = graphene.ID()
    product_name = graphene.String(required=True)
    description = graphene.String()
    icon = graphene.String()
    custom_columns = graphene.InputField(graphene.List(CustomColumnValueInput))


class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(Product)

    class Arguments:
        product_details = ProductInput(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            description=product_details.description,
            icon=product_details.icon,
            custom_columns=product_details.custom_columns
        )
        product.save()
        automatizations_checker('product',
                                ProductsListFilteredResolver=ProductsListFilteredResolver,
                                parseRaportData=parseRaportData)
        return CreateProductMutation(product=product)


class UpdateProductMutation(graphene.Mutation):
    id = graphene.String(required=True)
    product = graphene.Field(Product)
    modified = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        product_details = ProductInput(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None, product_details=None):
        found_objects = list(ProductModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            product_details["id"] = id
            product = ProductModel(**product_details)
            product.update(**product_details)
            # automatizations_checker('product', id, product_details, ProductsListFilteredResolver)
            # kwargs.ProductsListFilteredResolver, kwargs.parseRaportData, integrated_element
            return UpdateProductMutation(product=product, modified=True)
        return UpdateProductMutation(product=id, modified=False)


class DeleteProductMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(ProductModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            ProductModel.delete(found_objects[0])
            return DeleteProductMutation(id=id, deleted=True)
        return DeleteProductMutation(id=id, deleted=False)


# Resolvers


class ProductsListsResolver(graphene.ObjectType):
    products_list = MongoengineConnectionField(Product)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_products_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Product, *args)


class ProductsListFilteredResolver(graphene.ObjectType):
    products = MongoengineConnectionField(Product)

    filter_sort_products = graphene.List(
        lambda: Product,
        **product_filter_fields
    )

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_filter_sort_products(parent, info, show_custom_columns, filter_by, sort_by, limit=20):
        parsed_ids_show = list(
            map(lambda doc: ObjectId(doc), show_custom_columns))
        parsed_filters = list(
            map(lambda obj: {"custom_columns.value": {str(obj.comparison): obj.value}}, filter_by))

        pipeline = [
            # FILTERS
            {"$match": ({"$and": parsed_filters} if len(
                parsed_filters) > 0 else {})},
            # Show custom columns
            {"$project": {
             "product_name": True,
             "description": True,
             "icon": True,
             "custom_columns":
             {"$filter": {
                 "input": "$custom_columns",
                 "as": "cc",
                 "cond": {"$in": ["$$cc.custom_column", parsed_ids_show]}
             }}
             }
             },
            # SORT
            {"$addFields": {
                "order": {
                    "$filter": {
                        "input": "$custom_columns",
                        "as": "cc",
                        "cond": {sort_by['value']:
                                 ["$$cc.custom_column",
                                  ObjectId(sort_by['custom_column'])
                                  ]
                                 }
                    }
                }
            }},
            {"$sort": {"order": int(sort_by['value'])}},
            {"$project": {"order": False}},
            # LIMIT
            {"$limit": limit},
        ]
        cursor = ProductModel.objects.aggregate(*pipeline)
        parsed = list(map(lambda doc: ProductModel._from_son(doc), cursor))
        return parsed


class parseRaportData:
    def parse_cc(self, cc):
        cc_details = CustomColumnModel.to_json(cc['custom_column'])
        return {"custom_column": json.loads(cc_details), "value": cc['value']}

    def parse_product(self, product):
        cc = list(map(lambda cc: self.parse_cc(cc), product['custom_columns']))
        product['custom_columns'] = cc
        return json.loads(ProductModel.to_json(product))

    def parseData(self, raportData):
        return list(map(lambda product: self.parse_product(product), raportData))
