from functools import wraps
from starlette.requests import Request
from services.auth import jwt_authorize
from pydantic import BaseModel
from starlette.requests import Request
from graphql import GraphQLError

ranks = ["user", "admin"]


class PermissionsType(BaseModel):
    '''Permissions type'''
    allow_any: str = "user"


def permissions_checker(permissions: PermissionsType):
    '''Check if permissions are sufficient'''
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # DEVONLY: Bypass checking permissions
            return fn(*args, **kwargs)
            request: Request = Request(args[1].context["request"])
            try:
                token = request.headers["authorization"]
                if not token:
                    raise GraphQLError("No access_token provided")
                decoded_token = jwt_authorize(request.headers["authorization"])
                if not decoded_token:
                    raise GraphQLError("Incorrect access_token provided")
                # Check how ranked user can gain access
                rank = decoded_token["rank"]
                user_rank_index = ranks.index(rank)
                # print("user rank", user_rank_index, "needed rank", ranks.index(permissions.allow_any))
                if ranks.index(permissions.allow_any) <= user_rank_index:
                    return fn(*args, **kwargs)
                else:
                    raise GraphQLError("Not enough permission")
            except GraphQLError as error_permission:
                return error_permission
        return wrapper
    return decorator
