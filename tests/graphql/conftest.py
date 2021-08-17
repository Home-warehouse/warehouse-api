from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def authenticate():
    query = '''
    query login($email: String, $password: String){
        login(email: $email, password: $password){
          authenticated,
          accessToken
        }
    }
    '''
    executed = client.execute(query, variables={'email': 'test@email.com', 'password': 'PasswordField'})
    return executed


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
