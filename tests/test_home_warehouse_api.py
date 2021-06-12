from home_warehouse_api import __version__
from home_warehouse_api.schema import schema

from tests.account import test_account



# Test creating account
test_account(schema)

def test_version():
    assert __version__ == '0.1.0'
