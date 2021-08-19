import json
import graphene
from graphene_mongo.fields import MongoengineConnectionField
from bson.objectid import ObjectId
from middlewares.permissions import PermissionsType, permissions_checker
from models.common import product_filter_fields
from models.custom_column import CustomColumnModel
from models.product import Product, ProductModel


# Resolvers


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
    def __init__(self):
        pass

    def parse_cc(self, cc):
        cc_details = CustomColumnModel.to_json(cc['custom_column'])
        return {"custom_column": json.loads(cc_details), "value": cc['value']}

    def parse_product(self, product):
        cc = list(map(lambda cc: self.parse_cc(cc), product['custom_columns']))
        product['custom_columns'] = cc
        return json.loads(ProductModel.to_json(product))

    def parseData(self, raportData):
        return list(map(lambda product: self.parse_product(product), raportData))
