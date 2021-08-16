import graphene
from graphene_mongo.fields import MongoengineConnectionField
from middlewares.automatizations import automatizations_checker
from middlewares.permissions import PermissionsType, permissions_checker
from models.product import CreateProductInputType, Product, ProductInputType, ProductModel


# Mutations


class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(Product, required=True)

    class Arguments:
        product_details = CreateProductInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, product_details=None):
        product = ProductModel(
            product_name=product_details.product_name,
            description=product_details.description,
            icon=product_details.icon,
            custom_columns=product_details.custom_columns
        )
        product.save()
        automatizations_checker('product')
        return CreateProductMutation(product=product)


class UpdateProductMutation(graphene.Mutation):
    product = graphene.Field(Product, required=True)
    modified = graphene.Boolean(required=True)

    class Arguments:
        product_details = ProductInputType(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, product_details=None):
        found_objects = list(ProductModel.objects(**{"id": product_details['id']}))
        if len(found_objects) > 0:
            product_details["id"] = product_details['id']
            product = ProductModel(**product_details)
            product.update(**product_details)
            automatizations_checker('product')
            return UpdateProductMutation(product=product, modified=True)
        return UpdateProductMutation(product=product_details['id'], modified=False)


class DeleteProductMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    deleted = graphene.Boolean(required=True)

    class Arguments:
        id = graphene.ID(required=True)

    @permissions_checker(PermissionsType(allow_any="user"))
    def mutate(parent, info, id=None):
        found_objects = list(ProductModel.objects(**{"id": id}))
        if len(found_objects) > 0:
            ProductModel.delete(found_objects[0])
            automatizations_checker('product')
            return DeleteProductMutation(id=id, deleted=True)
        return DeleteProductMutation(id=id, deleted=False)


# Resolvers


class ProductsListsResolver(graphene.ObjectType):
    products_list = MongoengineConnectionField(Product)

    @permissions_checker(PermissionsType(allow_any="user"))
    def resolve_products_list(parent, info, *args, **kwargs):
        MongoengineConnectionField(Product, *args)
