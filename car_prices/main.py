import os
from car_prices.train import build_model
from car_prices.inference import make_predictions
import pandas as pd
train_data_csv = pd.read_csv(r'../data/train.csv')
print(train_data_csv.info())
model_performance_dict = build_model(train_data_csv)
print(model_performance_dict)

user_data_csv = pd.read_csv(r'../data/test.csv')
print(len(user_data_csv))
print(user_data_csv.info())
user_data_csv["predictions"] = make_predictions(user_data_csv)

print(len(predictions))