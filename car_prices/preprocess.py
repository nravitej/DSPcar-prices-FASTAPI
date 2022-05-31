import pandas as pd
import pickle
import numpy as np

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    
    """
    input: input dataframe - train or test
    output: return clean dataframe - without nan values and duplicates 
    """
    print('cleaning data')
    df['Age'] = pd.datetime.now().year - df['Year']
    df.drop('Vin', axis=1, inplace=True)
    print('Removing nan values and duplicates (if any)')
    na_ = df.isnull().values.sum()
    dupl_ix = df[df.duplicated().values].index
    dupl_ = len(dupl_ix)
    
    print('# of NA:',na_)
    print('# of Duplicated:',dupl_)
    # if len(dupl_ix)>0:
    #     print('removing duplicates...')
    #     df = df.drop(index=dupl_ix)
    
    return df    


def preprocess_data(df:pd.DataFrame) -> pd.DataFrame:
    
    """
    input: input array - train or test
    output: return preprocessed array - train or test
    """
    #min max scaler
    

    
    with open('pickle_files/oe.pkl', 'rb') as f:
        print('Loading pickle file (ordinal encoder)')
        oe = pickle.load(f)
        
    with open('pickle_files/scaler.pkl', 'rb') as f:
        print('Loading pickle file (standard scaler)')
        scaler = pickle.load(f)
        
    dtype_obj_cols = [c for c in df.columns if df[c].dtype=='object']
    print(dtype_obj_cols)
    
    df[dtype_obj_cols] = oe.transform(df[dtype_obj_cols])
        
    cols = ['Mileage', 'Age']
    for c in cols:
        df[cols] = scaler.transform(df[cols])
        
    
        
    
    
    return df