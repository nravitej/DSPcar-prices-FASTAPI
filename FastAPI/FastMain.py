from typing import List
import csv
import databases
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import sessionmaker
from uvicorn import run
from inference import make_predictions
from fastapi.middleware.wsgi import WSGIMiddleware
import os
import urllib
import sqlalchemy

app = FastAPI()

class Car_details(BaseModel):
    #index: int
    Year: int
    Mileage: int
    City: str
    State: str
    Vin: str
    Make: str
    Model: str
    Prediction: int


class PdVal(BaseModel):
    df_dict: List[Car_details]


class pydanticfiletype(BaseModel):
    file: UploadFile = File(...)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# loaded_model = load('../models/predict.joblib')


@app.post('/prediction/')
async def get_probability(file: UploadFile = File(...)):
    dat = pd.read_json(file.file)
    dat = dat.T
    try:
        PdVal(df_dict=dat.to_dict(orient="records"))
    except ValidationError as e:
        print(e)
    print(dat)
    dat.to_csv(r"../data/Inferencedata/inference.csv", index=False)
    dat = pd.read_csv(r"../data/Inferencedata/inference.csv")
    dat = pd.DataFrame(dat)
    dat[["Year"]] = dat[["Year"]].astype(int)
    dat[["Mileage"]] = dat[["Mileage"]].astype(int)
    print(dat.info())
    print(len(make_predictions(dat)))
    dat["Prediction"] = make_predictions(dat)
 
    f = dat.iloc[0:10, :2]
    print(f)

    return dat.to_json()


if __name__ == "__main__":
    run("FastMain:app")
