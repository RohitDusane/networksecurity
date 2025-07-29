import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

mongo_url = os.getenv("MONGO_DB_URL")
print(mongo_url)

import certifi
ca = certifi.where()  # to make secure HTTP connections

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


# ETL pipeline - reading data
class NetworkDataExtract:
    def __init__(self):
        try:
            # Initialize MongoDB Client here for reuse
            # self.mongo_client = pymongo.MongoClient(mongo_url, tls=True, tlsCAFile=ca)
            self.logging = logging
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    """
    Reads `CSV` file from filepath, resets index and
    converts the data into a list of JSON records 
    for MongoDB insertion
    """   
    def csv_to_json_converter(self, file_path):
        try:
            logging.info(f'Started reading `csv` data.....')
            # read and reset index of data
            data = pd.read_csv(file_path)
            logging.info(f'Reset and drop `Index`.')
            data.reset_index(drop=True, inplace=True)

            # converts data to json
            logging.info(f'Convert into JSON.....')
            records = data.to_dict(orient='records')
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def insert_records(self, records, database, collection):
        try:
            logging.info(f"Staring Data Insertion......")
            self.records = records
            self.database = database
            self.collection = collection

            # mongoDB Client
            self.mongo_client = pymongo.MongoClient(mongo_url)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info(f'Records added')
            return (len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


# Extract data and insetrt into Mongo DB
if __name__ == '__main__':
    logging.info('Starting Data Extraction!!!')
    file_path = 'Network_Data\\phisingData.csv'
    Database = 'RD_DB'
    Collection = 'Network_Data'

    obj = NetworkDataExtract()
    records = obj.csv_to_json_converter(file_path)
    print(records)
    number_of_records = obj.insert_records(records, Database, Collection)
    print(f"\n Number of recoreds inserted: {number_of_records}")