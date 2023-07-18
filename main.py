from fastapi import FastAPI
from custom_narou_api.lib import result

app = FastAPI()


@app.get(path="/aaa")
def aaa():
    return result()