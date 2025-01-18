import pandas as pd
import re

def load_data(data):
    loaded_data=pd.read_csv(data)
    return loaded_data

def preprocessing_data(data):
    preprocessed = data.dropna(subset=['Message'])
    return preprocessed