from models.account import AccountModel
from services.hash_password import hash_password


def create_admin_account():
    '''Create basic admin account'''
    found_objects = list(AccountModel.objects(
            **{"rank": "admin"}))
    if len(found_objects) == 0:
        print("Generating admin account")
        account = AccountModel(
          new_account=True,
          email="home-warehouse@mail.com",
          password=hash_password("home-warehouse-supervisor"),
          rank="admin"
        )
        account.save()
