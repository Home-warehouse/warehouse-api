from home_warehouse_api.schema import schema
from graphene.test import Client
import pytest

client = Client(schema)


@pytest.fixture
def create_account():
    query = '''
    mutation Account_create{
    createAccount(accountDetails:{
        email: "test@email.com",
        firstName: "FirstNameField"
        password: "PasswordField"
    }){
        created
    }
    }
    '''
    executed = client.execute(query)
    return executed


def test_create_account(create_account):
    assert create_account['data']['createAccount']['created']
