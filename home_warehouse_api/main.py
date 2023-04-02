import sys
from os import getenv, path as opath
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, HTTPException, responses, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

# Load logger before schema to allow schema dependencies use it correctly 
logger.remove()
logger.add(sys.stderr, colorize=True, format = "{level}: {message}")

from schema import schema
load_dotenv()

def parse_bool_env(value):
    if value == "True":
        return True
    else:
        return False


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv("API_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.debug = parse_bool_env(getenv("DEBUG"))


# Backend APIs
backend = FastAPI()
backend.mount('/graphql/', GraphQLApp(schema, on_get=make_graphiql_handler()), name="graphql")

# Frontend WebApp
folder = "home_warehouse_api/app"

class SPA(StaticFiles):
    async def get_response(self, path: str, scope):
        if path == 'api':
            return responses.RedirectResponse('/api/graphql', status_code=status.HTTP_302_FOUND)
        else:
            try: 
                if path == ".":
                    return await super().get_response("index.html", scope)
                else:
                    file = opath.realpath(folder+"/"+path)
                    if opath.exists(file):
                        return FileResponse(file)
                    index = 'home_warehouse_api/app/index.html' 
                    return FileResponse(index)
            except HTTPException as e:
                if e.status_code == 404:
                    return await super().get_response("index.html", scope)
                else:
                    raise e

app.mount('/api', app=backend)
logger.info(f"GraphQL is available under /api/graphql")

if parse_bool_env(getenv("MOUNT_APP")):
    app.mount('/', SPA(directory="home_warehouse_api/app", html=True))
    logger.info(f"Web app is mounted under /")

# Serve
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=getenv("API_HOST"),
        port=int(getenv("PORT")),
        reload=getenv("DEBUG")       
    )
