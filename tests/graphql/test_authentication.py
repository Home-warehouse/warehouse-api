from starlette.datastructures import Headers
from home_warehouse_api.schema import schema
from starlette.requests import Request
from graphene.test import Client

client = Client(schema)


def test_authenticate(authenticate):
    assert authenticate['data']['login']['authenticated']


def test_refresh_token(authenticate):
    query = '''
    query updateToken {
        refreshToken{
         refreshed
       }
     }
    '''
    headers = {'Authorization': authenticate['data']['login']['accessToken']}
    request = Request({
        "type": "http",
        "headers": Headers(headers).raw
    })
    executed = client.execute(query, context={'request': request})
    assert executed == {
        "data": {
            "refreshToken": {
                "refreshed": True
            }
        }
    }
