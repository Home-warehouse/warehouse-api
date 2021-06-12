import datetime
import graphene
from starlette.requests import Request

from models.account import AccountModel
from models.location import LocationModel

from services.hash_password import verify_password
from services.auth import jwt_authenticate, jwt_authorize


class AuthenticationResolver(graphene.ObjectType):
    login = graphene.String(email=graphene.String(),
                            password=graphene.String())

    def resolve_login(parent, info, email, password):
        found_objects = list(AccountModel.objects(**{"email": email}))
        if len(found_objects) > 0:
            password_correct = verify_password(
                found_objects[0]["password"], password)
            if password_correct:
                rank = found_objects[0].rank
                object_id = str(found_objects[0].id)
                token = jwt_authenticate(object_id, rank)
            return {"authentication": True, "access_token": token}
        return {"authentication": False}

    refresh_token = graphene.String(access_token=graphene.String())

    def resolve_refresh_token(parent, info):
        request: Request = Request(info.context["request"])
        decoded = jwt_authorize(request.headers["authorization"])
        print(decoded)
        if decoded:
            if datetime.datetime.fromtimestamp(decoded['exp']) > datetime.datetime.utcnow():
                return {
                    "refreshed": True,
                    "access_token": jwt_authenticate(decoded['client_id'], decoded['rank'])
                }
        return {"refreshed": False}

    def resolve_pepege(parent, info, test):
        found_objects = list(LocationModel.objects(**{}))
        return {"found": found_objects}