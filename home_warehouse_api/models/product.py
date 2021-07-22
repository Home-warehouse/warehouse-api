import graphene

from graphene_mongo.fields import MongoengineConnectionField
from graphene_mongo import MongoengineObjectType
from bson.objectid import ObjectId

from mongoengine import Document
from mongoengine.fields import EmbeddedDocumentListField, StringField

from middlewares.permissions import PermissionsType, permissions_checker
from models.custom_columns import CustomColumnValueInput, CustomColumnValueModel
from resolvers.node import CustomNode

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
    '''Product type for Mongoengine ObjectType'''
    class Meta:
        '''Product mongo object meta settings'''
        model = ProductModel
        interfaces = (CustomNode,)
        filter_fields = {
            'product_name': ['exact', 'icontains', 'istartswith']
        }


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

    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            description=product_details.description,
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
    mutate = permissions_checker(
        fn=mutate, permissions=PermissionsType(allow_any="user"))


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

    def resolve_products_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Product, *args)

    resolve_products_list = permissions_checker(
        resolve_products_list, PermissionsType(allow_any="user"))


class sortByEnum(graphene.Enum):
    ASC = 'ASC'
    DESC = 'DESC'

    @property
    def description(self):
        if self == sortByEnum.ASC:
            return 'Sort Ascending'
        if self == sortByEnum.DESC:
            return 'Sort Descending'


class ProductsListFilteredResolver(graphene.ObjectType):
    products = MongoengineConnectionField(Product)
    filter_products = graphene.List(
        lambda: Product,
        custom_column_ids=graphene.List(
            graphene.String,
            description="List of IDs of custom columns which are present in products"
        ),
        sortByValue=sortByEnum()
    )

    def resolve_filter_products(parent, info, custom_column_ids, sortByValue=''):
        parsed_ids = list(map(lambda id: ObjectId(id), custom_column_ids))
        query = ProductModel.objects(
            __raw__={'custom_columns.custom_column': {'$in': parsed_ids}})
        query = query.order_by(sortByValue+'custom_columns.value')
        return query

    resolve_filter_products = permissions_checker(
        resolve_filter_products, PermissionsType(allow_any="user"))
