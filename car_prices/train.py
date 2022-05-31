import sys
import os
sys.path.insert(0,os.getcwd()+'\car_prices')
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from preprocess import preprocess_data,clean_data

def build_model(train_data) -> dict:
    """
    data: input data file path(csv)
    :returns (dict) {"model_performance": "", "model_path": ""} 
    """
    data = train_data.copy()
    #split train and test data before preprocessing
    train_df, test_df = train_test_split(data, test_size=0.2)
    
    
    
    #clean train data 
    train_df = clean_data(train_df)
    X_train = train_df.drop('Price', axis=1)
    y_train = train_df['Price'].values

    #clean test data
    test_df = clean_data(test_df)
    X_test = test_df.drop('Price', axis=1)
    y_test = test_df['Price'].values

    dtype_obj_cols = [c for c in X_train.columns if X_train[c].dtype=='object' ]
    oe = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
    oe.fit(X_train[dtype_obj_cols])
            
    cols = ['Mileage', 'Age']
    scaler = StandardScaler()
    scaler.fit(X_train[cols])
    
    #save pickle file
    print('Saving pickle file (ordinal encoder)')
    if not os.path.exists('pickle_files/'):
        os.makedirs('pickle_files/')
    with open('pickle_files/oe.pkl', 'wb') as f:
        pickle.dump(oe, f)

        
    print('Saving pickle file (standard scaler)')
    if not os.path.exists('pickle_files/'):
        os.makedirs('pickle_files/')
    with open('pickle_files/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        

    
    
    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test)
    
    #model training
    model = LinearRegression()

    model.fit(X_train, y_train)

    
    

    
    if not os.path.exists('trained_model/'):
        os.makedirs('trained_model/')
    saved_model_path = 'trained_model/model.sav'
    print('Saving model pickle file in',saved_model_path)
    pickle.dump(model, open(saved_model_path, 'wb'))
    
    
    #model evaluation
    print('Model evaluation on train and test data....')
    
    train_prediction = model.predict(X_train)
    train_mse = mean_squared_error(y_train, train_prediction)
    print('Performance on train data (MSE):',train_mse)
    
    test_prediction = model.predict(X_test)
    test_mse = mean_squared_error(y_test, test_prediction)
    print('Performance on test data (MSE):',test_mse)
    
    
    
    
    return dict({'mse':test_mse,'model_path':saved_model_path}) 