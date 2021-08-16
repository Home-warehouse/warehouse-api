import datetime
import graphene
from starlette.requests import Request
from models.account import AccountModel
from services.hash_password import verify_password
from services.auth import jwt_authenticate, jwt_authorize


# Resolvers


class LoginType(graphene.ObjectType):
    '''Login type for graphene'''
    email = graphene.String()
    password = graphene.String()
    authenticated = graphene.Boolean()
    access_token = graphene.String()


def resolve_login(parent, info, email, password):
    '''Login resolver'''
    found_objects = list(AccountModel.objects(**{"email": email}))
    if len(found_objects) > 0:
        password_correct = verify_password(
            found_objects[0]["password"], password)
        if password_correct:
            rank = found_objects[0].rank
            object_id = str(found_objects[0].id)
            token = jwt_authenticate(object_id, rank)
            return LoginType(authenticated=True, access_token=token)
    return LoginType(authenticated=False)


_login = graphene.Field(
    description="Get access_token in form of JWT token",
    type=LoginType,
    resolver=resolve_login,
    email=graphene.String(default_value=None),
    password=graphene.String(default_value=None)
)


class RefreshTokenType(graphene.ObjectType):
    '''RefreshToken type for graphene'''
    email = graphene.String()
    password = graphene.String()
    refreshed = graphene.Boolean()
    access_token = graphene.String()


def resolve_refresh_token(parent, info):
    '''Refresh token resolver'''
    request: Request = Request(info.context["request"])
    decoded = jwt_authorize(request.headers["authorization"])
    if decoded:
        if datetime.datetime.fromtimestamp(decoded['exp']) > datetime.datetime.utcnow():
            return RefreshTokenType(refreshed=True, access_token=jwt_authenticate(
                decoded['client_id'], decoded['rank']))
    return RefreshTokenType(refreshed=False)


_refresh_token = graphene.Field(
    description='Refresh access_token by passing old one in headers as "Authorization" header',
    type=RefreshTokenType,
    resolver=resolve_refresh_token
)


class AuthenticationResolvers(graphene.ObjectType):
    login = _login
    refresh_token = _refresh_token
