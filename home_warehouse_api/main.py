import sys
from os import getenv
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp
from loguru import logger

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

app.add_route('/graphql', GraphQLApp(schema))

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
