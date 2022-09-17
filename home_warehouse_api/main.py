import sys
from os import getenv
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

logger.remove()
logger.add(sys.stderr, colorize=True, format = "{level}: {message}")

from schema import schema
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv("API_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.debug = getenv("DEBUG")

app.mount('/graphql', GraphQLApp(schema, on_get=make_graphiql_handler()))

@app.get("/")
def ping():
    '''API ping route for testing'''
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=getenv("API_HOST"),
        port=int(getenv("API_PORT")),
        reload=getenv("DEBUG")       
    )
