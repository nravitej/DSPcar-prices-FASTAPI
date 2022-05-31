from typing import List

import pandas as pd
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, ValidationError
from uvicorn import run
from train import build_model
from inference import make_predictions
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class Car_details(BaseModel):
    Price:int
    Year: int
    Mileage: int
    City: str
    State: str
    Vin: str
    Make: str
    Model: str
class PdVal(BaseModel):
    df_dict: List[Car_details]


class pydanticfiletype(BaseModel):
    file: UploadFile = File(...)


#loaded_model = load('../models/predict.joblib')


@app.post('/train/')
async def get_probability(file: UploadFile = File(None, media_type=Car_details)):
    dat = pd.read_json(file.file)
    dat = dat.T
    dat[["Year"]]=dat[["Year"]].astype(int)
    dat[["Mileage"]]=dat[["Mileage"]].astype(int)
    dat[["Price"]]=dat[["Price"]].astype(int)
    print(dat.info())
    Modelinfo=build_model(dat)
    print(Modelinfo)

    return Modelinfo


if __name__ == "__main__":
    run("FastMainTest:app")
