from loguru import logger
from models.account import AccountModel
from services.hash_password import hash_password
import string
import random
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def create_admin_account():
    '''Create basic admin account'''
    found_objects = list(AccountModel.objects(
            **{"rank": "admin"}))
    if len(found_objects) == 0:
        testing = (getenv('TEST', 'False') == 'True')
        generated_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=15))
        admin_password = "test_password" if testing else generated_password
        hashed_password = hash_password(admin_password)
        account = AccountModel(
          new_account=True,
          email="home-warehouse@mail.com",
          password=hashed_password,
          rank="admin"
        )
        account.save()
        logger.info(f"""
        ---------------------------
        Running test env: {testing}
        ---------------------------
        Generating admin account
        email: home-warehouse@mail.com
        password: {admin_password}
        Please, change admin password to something else
        because anyone who will have access to this log will be able to login with admin account.
        Thanks! :)
        ---------------------------
        """)
