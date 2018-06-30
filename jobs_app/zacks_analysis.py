import pandas as pd
from pymongo import MongoClient

def create_zacks_df(stock, collection_name, table_id):
    client = MongoClient('localhost', 27017)
    db = client['ZACKS']
    db_cm = db[collection_name]
    data = db_cm.find({'Symbol': stock})

    # Convert Dictionary to dataframe and then convert to html table
    list_data = []

    for x in data:
        list_data.append(x)

    df = pd.DataFrame(list_data)
    df = df.to_html()
    df = df.replace('<table border="1" class="dataframe">',
                                  '<table id="'+ table_id + '" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
    return df
