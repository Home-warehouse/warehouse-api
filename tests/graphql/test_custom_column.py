from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def create_custom_column():
    query = '''
    mutation CC_create{
        createCustomColumn(customColumnDetails:{
            customColumnName:"Custom column name"
            index: 0,
            elementsAllowed: [PRODUCTS, LOCATIONS]
            dataType: DATE
        }){
            customColumn{
                id
                customColumnName
            }
        }
    }
    '''
    executed = client.execute(query)
    return executed


def test_create_custom_column(create_custom_column):
    cc_name = create_custom_column['data']['createCustomColumn']['customColumn']['customColumnName']
    assert cc_name == "Custom column name"


def test_update_single_custom_column(create_custom_column):
    cc_id = create_custom_column['data']['createCustomColumn']['customColumn']['id']

    query = '''
    mutation CC_modify($id: ID!){
        modifyCustomColumn(
            input:[
                {
                    id: $id,
                    index: 1
                },
            ]
        ){
            customColumns{
                id
                index
            }
            modified
        }
    }
    '''
    executed = client.execute(query, variables={'id': cc_id})
    cc_index = executed['data']['modifyCustomColumn']['customColumns'][0]['index']
    assert cc_index == 1


def test_list_custom_columns():
    query = '''
    query CC_list{
        customColumnsList {
            edges {
                node {
                    dataType
                    elementsAllowed
                    customColumnName
                }
            }
        }
    }
    '''
    executed = client.execute(query)
    assert executed['data']['customColumnsList']['edges'][0]['node'] == {
            "dataType": "date",
            "elementsAllowed": [
              "products",
              "locations"
            ],
            "customColumnName": "Custom column name"
        }


def test_delete_custom_column(create_custom_column):
    cc_id = create_custom_column['data']['createCustomColumn']['customColumn']['id']
    query = '''
    mutation CC_delete($id: ID!){
        deleteCustomColumn(id: $id){
            deleted
        }
    }
    '''
    executed = client.execute(query, variables={'id': cc_id})
    assert executed == {
        "data": {
            "deleteCustomColumn": {
                "deleted": True
            }
        }
    }
