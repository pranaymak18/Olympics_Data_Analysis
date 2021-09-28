import pandas as pd


def preprocess(df,region_df):
    #global df,region_df
    #Filter Summer Olympics data
    df = df[df['Season'] == 'Summer']
    #Left Join on df and region_df
    df = df.merge(region_df, on='NOC', how='left')
    #Drop duplicate
    df.drop_duplicates(inplace=True)
    #Encoding Medal
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

