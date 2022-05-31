from typing import List

import pandas as pd
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, ValidationError
from uvicorn import run
from inference import make_predictions

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class Car_details(BaseModel):
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
    dat.to_csv(r"../data/Inferencedata/inference.csv",index=False)
    dat=pd.read_csv(r"../data/Inferencedata/inference.csv")
    dat = pd.DataFrame(dat)
    dat[["Year"]] = dat[["Year"]].astype(int)
    dat[["Mileage"]] = dat[["Mileage"]].astype(int)
    print(dat.info())
    print(len(make_predictions(dat)))
    dat["predictions"] = make_predictions(dat)

    f = dat.iloc[0:10, :2]
    print(f)

    return dat.to_json()
    # predictions = loaded_model(dat)
    print(type(file.file))
    if file is not None:
        print("File uploaded")

    return file


if __name__ == "__main__":
    run("FastMain:app")
