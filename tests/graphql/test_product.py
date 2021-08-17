from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def create_product():
    query = '''
    mutation Product_create {
    createProduct(productDetails: {
        productName: "ProductNameField"
        description: "DescriptionField"
    }){
        product {
        id
        productName
        }
    }
    }
    '''
    executed = client.execute(query)
    return executed


def test_create_product(create_product):
    productName = create_product['data']['createProduct']['product']['productName']
    assert productName == 'ProductNameField'


def test_modify_product(create_product):
    query = '''
    mutation Product_modify($productID: ID!){
        modifyProduct(productDetails:{
            id: $productID,
            productName:"NewProductNameField"
        }){
            modified
        }
    }
    '''
    product_id = create_product['data']['createProduct']['product']['id']
    executed = client.execute(query, variables={'productID': product_id})
    assert executed == {
        "data": {
            "modifyProduct": {
                "modified": True
            }
        }
    }


def test_list_products():
    query = '''
    query Products_list {
        productsList {
            edges {
            node {
                description
            }
            }
        }
    }
    '''
    executed = client.execute(query)
    assert executed['data']['productsList']['edges'][0]['node'] == {
            "description": "DescriptionField"
        }


def test_delete_product(create_product):
    query = '''
    mutation Product_delete($productID: ID!){
        deleteProduct(id: $productID){
            deleted
        }
    }
    '''
    product_id = create_product['data']['createProduct']['product']['id']
    executed = client.execute(query, variables={'productID': product_id})
    assert executed == {
            "data": {
                "deleteProduct": {
                    "deleted": True
                }
            }
        }
