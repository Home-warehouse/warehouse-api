import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp

from schema import schema


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:4200",
    "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.debug = True

app.add_route('/graphql', GraphQLApp(schema))


@app.get("/")
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,
                log_level="info", reload=True)
