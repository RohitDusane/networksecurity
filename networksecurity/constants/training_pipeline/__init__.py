# THIS FILE STORES THE CONSTANTS FOR DATA INGESTION PIPELINE
import os
import sys
import pandas as pd
import numpy as np


#---------------------------------Commom Constants and Variables----------------------------------------
""" Defining Common Constant Variables
COMMON CONSTANT VARIABLES FOR TRAINING PIPELINE
"""
TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR : str = 'Artifacts'
FILE_NAME: str = 'phishingData.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

#----------------------------------Data Ingestion Variables and DIR------------------------------

"""
DATA INGESTION related constants 
start with DATA_INGESTION_VAR_NAME
"""
DATA_INGESTION_COLLECTION_NAME: str= 'Network_Data'         # DB Name
DATA_INGESTION_DATABASE_NAME: str = 'RD_DB'                 # SCHEMA NAME
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'             # DATA INGESTION DIRECOTRY NAME
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'     # 
DATA_INGESTION_INGESTED_DIR: str = 'ingested'               # data sotred
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2          # 20% test size


#---------------------------------------------------------------------------------------------