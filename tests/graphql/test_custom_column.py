from home_warehouse_api.schema import schema
from graphene.test import Client

client = Client(schema)


def test_create_custom_column(create_custom_column):
    cc_name = create_custom_column['data']['createCustomColumn']['customColumn']['customColumnName']
    assert cc_name == "Custom column name"


def test_modify_single_custom_column(create_custom_column):
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
    cc_id = create_custom_column['data']['createCustomColumn']['customColumn']['id']
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
    query = '''
    mutation CC_delete($id: ID!){
        deleteCustomColumn(id: $id){
            deleted
        }
    }
    '''
    cc_id = create_custom_column['data']['createCustomColumn']['customColumn']['id']
    executed = client.execute(query, variables={'id': cc_id})
    assert executed == {
        "data": {
            "deleteCustomColumn": {
                "deleted": True
            }
        }
    }
