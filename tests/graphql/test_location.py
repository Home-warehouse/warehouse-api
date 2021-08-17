from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def create_location():
    query = '''
   mutation Location_create {
    createLocation(locationDetails:{
        locationName: "LocationNameField"
    }){
        location{
        id
        locationName
        }
    }
    }
    '''
    executed = client.execute(query)
    return executed


def test_create_location(create_location):
    locationName = create_location['data']['createLocation']['location']['locationName']
    assert locationName == 'LocationNameField'


def test_modify_location(create_location):
    query = '''
    mutation Location_modify($locationID: ID!){
        modifyLocation(locationDetails:{
            id: $locationID,
            locationName:"NewLocationNameField"
        }){
            modified
        }
    }
    '''
    location_id = create_location['data']['createLocation']['location']['id']
    executed = client.execute(query, variables={'locationID': location_id})
    assert executed == {
        "data": {
            "modifyLocation": {
                "modified": True
            }
        }
    }

# TODO: add test for nested locations


def test_list_flat_locations():
    query = '''
    query flatedLocations {
        locationsList {
            edges {
            node {
                locationName
            }
            }
        }
    }
    '''
    executed = client.execute(query)
    assert executed['data']['locationsList']['edges'][0]['node'] == {
            "locationName": "LocationNameField"
        }


def test_delete_location(create_location):
    location_id = create_location['data']['createLocation']['location']['id']
    query = '''
    mutation Location_delete($locationID: ID!){
        deleteLocation(id: $locationID){
            deleted
        }
    }
    '''
    executed = client.execute(query, variables={'locationID': location_id})
    assert executed == {
            "data": {
                "deleteLocation": {
                    "deleted": True
                }
            }
        }
