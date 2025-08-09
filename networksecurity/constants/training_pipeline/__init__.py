# THIS FILE STORES THE CONSTANTS FOR DATA INGESTION PIPELINE
import os
import sys
import pandas as pd
import numpy as np


#---------------------------------Commom Constants and Variables---------------------------------
""" Defining Common Constant Variables
COMMON CONSTANT VARIABLES FOR TRAINING PIPELINE
"""
TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR : str = 'Artifacts'
FILE_NAME: str = 'phishingData.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEMA_FILE_PATH = os.path.join('data_schema','schema.yaml')

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = ("model.pkl")

#----------------------------------Data Ingestion Variables and DIR------------------------------

"""
DATA INGESTION related constants 
start with DATA_INGESTION_VAR_NAME
"""
DATA_INGESTION_COLLECTION_NAME: str= 'Network_Data'         # DB Name
DATA_INGESTION_DATABASE_NAME: str = 'RD_DB'                 # SCHEMA NAME
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'             # DATA INGESTION DIRECOTRY NAME
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'     # RAW data file
DATA_INGESTION_INGESTED_DIR: str = 'ingested'               # data sotred
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2          # 20% test size


#--------------------------------Data Validation Variables and DIR-------------------------------

"""
DATA VALIDATION related constants 
start with DATA_VALIDATION_VAR_NAME
"""
DATA_VALIDATION_DIR_NAME: str = 'data_validation'           # root directory for all validation artifacts
DATA_VALIDATION_VALID_DIR: str = 'validated'                # Subfolder where "clean" (schema-compliant, no drift) data is stored
DATA_VALIDATION_INVALID_DIR: str = 'invalidated'            # Subfolder for rejecting or quarantining bad data
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'      # Subfolder to output the drift report 
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml' # Filename for the drift report

#----------------------------------Data Transformation Variables and DIR------------------------------

"""
DATA TRANSFORMATION related constants 
start with DATA_TRANSFORMATION_VAR_NAME
"""
PREPROCESSNG_OBJECT_FILE_NAME:str = 'preprocessing.pkl'
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = 'transformed_data'
DATA_TRANSFORMATION_TRASFORMED_OBJECT_DIR:str = 'transformed_object'
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values": np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH:str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

#----------------------------------MODEL TRAINER Variables and DIR------------------------------

"""
MODEL TRAINER related constants 
start with MODEL_TRAINER_VAR_NAME
"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05

