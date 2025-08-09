# # Importing Constants in the Config Entity

# """
# This allows the configuration entity to access all 
# necessary values for the data ingestion process.
# """
# import os
# import sys
# from datetime import datetime
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.constants import training_pipeline

# print(training_pipeline.PIPELINE_NAME)
# print(training_pipeline.ARTIFACT_DIR)

# # Creating Configuration Classes
# # Define a class for the data ingestion configuration. 
# # This class will initialize all required paths and parameters 
# # using the constants imported earlier. The class should also include 
# # a timestamp for tracking purposes.

# class TrainingPipelineConfig:
#     def __init__(self, timestamp=datetime.now()):
#         timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
#         self.timestamp: str=timestamp
#         self.pipeline_name = training_pipeline.PIPELINE_NAME
#         self.artifact_dir = training_pipeline.ARTIFACT_DIR
#         self.artifact_dir_with_timestamp = os.path.join(self.artifact_dir,timestamp)
        
# # Create DataIngestion Config
# class DataIngestionConfig:
#     def __init__(self, training_pipeline_config:TrainingPipelineConfig):
#         self.data_ingestion_dir : str = os.path.join(
#             training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
#         )
#         self.feature_store_file_path : str = os.path.join(
#             self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
#         )
#         self.training_file_path : str =os.path.join(self.data_ingestion_dir,
#                                                     training_pipeline.DATA_INGESTION_DIR_NAME,
#                                                     training_pipeline.TRAIN_FILE_NAME)
#         self.test_file_path: str = os.path.join(self.data_ingestion_dir,
#                                                 training_pipeline.DATA_INGESTION_DIR_NAME,
#                                                 training_pipeline.TEST_FILE_NAME)
#         self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
#         self.collection_name: str= training_pipeline.DATA_INGESTION_COLLECTION_NAME
#         self.database_name: str= training_pipeline.DATA_INGESTION_DATABASE_NAME


# if __name__=="__main__":
#     try:
#         training_pipeline_config=TrainingPipelineConfig
#         data_ingestion_config = DataIngestionConfig(training_pipeline_config)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)


import os
import sys
from datetime import datetime
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = training_pipeline.ARTIFACT_DIR
        self.artifact_dir_with_timestamp = os.path.join(self.artifact_dir, self.timestamp)
        
        # Ensure the artifact directory exists
        os.makedirs(self.artifact_dir_with_timestamp, exist_ok=True)


# -------- Data Ingestion Config --------------------
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR)
        self.training_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_DIR_NAME, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_DIR_NAME, training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        
        # Ensure the data ingestion directory exists
        os.makedirs(self.data_ingestion_dir, exist_ok=True)

# if __name__ == "__main__":
#     try:
#         # Initialize training pipeline configuration
#         training_pipeline_config = TrainingPipelineConfig()
        
#         # Initialize data ingestion configuration
#         data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        
#     except Exception as e:
#         raise NetworkSecurityException(str(e), sys.exc_info())

# -------- Data Validation Config --------------------
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(self.data_validation_dir, 
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, 
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
            )


# -------- Data Transformation Config --------------------
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,
                                                        training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,
                                                            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,
                                                            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,
                                                              training_pipeline.DATA_TRANSFORMATION_TRASFORMED_OBJECT_DIR,
                                                              training_pipeline.PREPROCESSNG_OBJECT_FILE_NAME)
        

# -------- MODEL TRAINER Config --------------------
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str=os.path.join(training_pipeline_config.artifact_dir,
                                                training_pipeline.MODEL_TRAINER_DIR_NAME)
        
        self.trained_model_file_path:str= os.path.join(self.model_trainer_dir,
                                                       training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                       training_pipeline.MODEL_FILE_NAME)
        
        self.expected_accuracy:float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.over_fitting_under_fitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD