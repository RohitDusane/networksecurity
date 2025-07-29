# Function to read from Mongodb, 
# export colletion as dataframe,
# Export data in feature store,
# split train-test and store in artifacts

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

mongo_url = os.getenv("MONGO_DB_URL")

"""Creating the DataIngestion Class
    A modular DataIngestion class is created, which initializes 
    with the DataIngestionConfig. 
    Exception handling is implemented using try-except blocks
"""
class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    """
    Read data from MONGODB and covert to DataFrame
    Exporting Collection as DataFrame
    A function is defined to export a MongoDB collection as a pandas DataFrame. 
    The function connects to MongoDB, retrieves the collection, and converts it to a DataFrame. 
    The '_id' column is dropped if present, and any 'na' values are replaced with numpy's NaN.
    """
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(mongo_url)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if '_id'in df.columns.to_list():
                df = df.drop(columns=['_id'], axis=1)
                df.replace({'na':np.nan}, inplace=True)
            
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """
    Create FEATURE STORE and save raw.csv data
    Exporting Data to Feature Store
    To export the DataFrame to a CSV file in the feature store directory. 
    The directory is created if it does not exist
    """
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            # feature store filepath
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Create the `FeatureStore` folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            # save the dataframe as csv
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """
    Splitting Data into Train and Test Sets
    A function is defined to split the data into train and test sets 
    using scikit-learn's train_test_split. The resulting sets are 
    saved as CSV files in the appropriate directories.
    """
    def split_data_as_train_test_data(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe,
                                                   test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Performed Train-Test Split")

            logging.info(f"Exited train-test split method")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting Train-Test filepath")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info(f"Exported train-test file path")
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """
    The main function to initiate data ingestion calls the previously defined 
    steps in sequence and returns the data ingestion artifact.
    """
    def initiate_data_ingestion(self):
        try:
            # dataframe=self.export_collection_as_dataframe()
            # dataframe=self.export_data_into_feature_store(dataframe)
            # self.split_data_as_train_test_data(dataframe)
            # dataingestionartifact = self.DataIngestionArtifact(
            #     trained_file_path = self.data_ingestion_config.training_file_path,
            #     test_file_path = self.data_ingestion_config.test_file_path
            # )
            # return dataingestionartifact
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test_data(df)
            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)