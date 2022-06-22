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
host_server = os.environ.get('Host', 'ec2-3-230-122-20.compute-1.amazonaws.com')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('Port', '5432')))
database_name = os.environ.get('Database', 'd59neqiqc668vc')
db_username = urllib.parse.quote_plus(str(os.environ.get('User', 'otbgdaygwxniqq')))
db_password = urllib.parse.quote_plus(str(os.environ.get('Password', '741b2f1e4cb951ab402009d479b9073f765ee5234f0f36537ee592f9ebaec8e0')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port,
                                                               database_name, ssl_mode)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

CarPrices = sqlalchemy.Table(
    "CarPrices",
    metadata,
    sqlalchemy.Column("index", sqlalchemy.Integer,sqlalchemy.Sequence("CarPrices_index_seq"),autoincrement=True),
    sqlalchemy.Column("Year", sqlalchemy.Integer),
    sqlalchemy.Column("Mileage", sqlalchemy.Float),
    sqlalchemy.Column("City", sqlalchemy.String),
    sqlalchemy.Column("State", sqlalchemy.String),
    sqlalchemy.Column("Vin", sqlalchemy.String),
    sqlalchemy.Column("Make", sqlalchemy.String),
    sqlalchemy.Column("Model", sqlalchemy.String),
    sqlalchemy.Column("Prediction", sqlalchemy.String),

)


engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def save_predictions(records):
    print(records)
    query = records.to_sql("CarPrices", con=engine, if_exists='append')
    # query = CarPrices.insert().values(records)
    # print(query)
    #last_record_id = query
    return 1


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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
    save_predictions(dat)

    f = dat.iloc[0:10, :2]
    print(f)

    return dat.to_json()


if __name__ == "__main__":
    run("FastMain:app")
