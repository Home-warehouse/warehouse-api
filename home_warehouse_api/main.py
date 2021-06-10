import uvicorn
from fastapi import Depends, FastAPI
from starlette.graphql import GraphQLApp

from dependencies import get_query_token
from schema import schema

app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.debug = True

app.add_route('/graphql', GraphQLApp(schema))


@app.get("/")
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,
                log_level="info", reload=True)
