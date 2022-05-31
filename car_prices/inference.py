import pandas as pd
import numpy as np
import pickle
import sys
import os
sys.path.insert(0,os.getcwd()+'\car_prices')
from preprocess import preprocess_data,clean_data

def make_predictions(test_data) -> np.ndarray:
    
    """
    df: unseen test data as a csv
    returns predictions (wine quality) as a numpy array
      """
    
    df = test_data.copy()
    #print(df.info())
    
    
    
    #Load model
    
    filename = 'trained_model/model.sav'
    # load the model from disk
    print('Loading the trained model...')
    model = pickle.load(open(filename, 'rb'))
    
    #id_values = df['Id'].values
    print('Preprocessing test data...')
    df = clean_data(df)
    print("length of preprocessed dataframe",len(df))
    X_test = preprocess_data(df)
    
    print('Return predictions on unseen test data...')
    y_test_pred = model.predict(X_test)

    return y_test_pred    