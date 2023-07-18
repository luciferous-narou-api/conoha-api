from fastapi import FastAPI

import src.controllers as controllers
import src.models as models
from src.middlewares import MiddlewareCheckHeader, MiddlewareErrorHandling

app = FastAPI()

app.add_middleware(MiddlewareErrorHandling)
app.add_middleware(MiddlewareCheckHeader)


@app.get("/test")
def test():
    return controllers.test()


@app.get("/error")
def error():
    raise Exception("test")


@app.post("/get_information")
def get_information(item: models.ModelGetInformation):
    return controllers.get_information(model=item)
