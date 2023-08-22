import pandas as pd
from pathlib import Path
from utils import input_valid_file_path, VCC_or_AB

def read_dataframe():
    file_path = input_valid_file_path()
    xlsx_file = Path(file_path)
    df = pd.read_excel(xlsx_file, index_col=0)
    return df

def prepare_dataframe(df):
    title = VCC_or_AB()
    df.columns = df.iloc[0]
    #remove first row from DataFrame
    df = df[1:]

    #view updated DataFrame
    df['Job Posting Submit Date'] = pd.to_datetime(df['Job Posting Submit Date'])
    df = df.set_index(df['Job Posting Submit Date'])
    df = df.sort_index()
    #print(df)
    df = df.dropna(how='all')

    #new column with year
    df['year'] = df['Job Posting Submit Date'].dt.year
    #print(df)

    df_freq = df.pivot_table(index = [title], columns=['year'], aggfunc ='size')
    df_freq = df_freq.fillna(0)
    
    return df_freq
