from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def create_raport(create_custom_column):
    '''This test requires minimum 1 custom_column object'''
    query = '''
    mutation Raport_create($cc: ID!) {
        createRaport(raportDetails: {
            raportName: "RaportNameField"
            showCustomColumns: [$cc]
            sortBy: {customColumn: $cc, value: "+"}
            filterBy: [{customColumn: $cc, comparison: EQUAL, value: "true"}]
            shortResults: 5
        }){
        raport {
            id
            raportName
        }
        }
    }
    '''
    id = create_custom_column['data']['createCustomColumn']['customColumn']['id']
    executed = client.execute(query, variables={'cc': id})
    return executed


def test_create_raport(create_raport):
    raport_name = create_raport['data']['createRaport']['raport']['raportName']
    assert raport_name == "RaportNameField"


def test_modify_single_raport(create_raport):
    query = '''
    mutation Raport_modify($raportID: ID!) {
        modifyRaport(raportDetails:{
            id: $raportID
            raportName:"NewNameField"
        }){
            modified
        }
    }
    '''
    raport_id = create_raport['data']['createRaport']['raport']['id']
    executed = client.execute(query, variables={'raportID': raport_id})
    assert executed == {
        "data": {
            "modifyRaport": {
                "modified": True
            }
        }
    }


def test_delete_raport(create_raport):
    query = '''
    mutation Raport_delete($raportID: ID!) {
        deleteRaport(id: $raportID) {
            deleted
        }
    }
    '''
    raport_id = create_raport['data']['createRaport']['raport']['id']
    executed = client.execute(query, variables={'raportID': raport_id})
    assert executed == {
        "data": {
            "deleteRaport": {
                "deleted": True
            }
        }
    }
