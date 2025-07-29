



#-------------------Data Ingestion test------------------------------------------------------
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.data_ingestion import DataIngestion
import os
import sys

if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()  # Create an instance
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)  # Pass the instance
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info(f'Initiate Data Ingestion')
        data_ingestion.initiate_data_ingestion()
        print(DataIngestionArtifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


#-------------------Exception Handling test--------------------------------------------------

# # Testing for logger and exception handling
# if __name__ == "__main__":
#     try:
#         logging.info("Starting Exception Handling...")
#         a=2/0
#         print(a)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)

#-------------------Logger testing-----------------------------------------------------------
# Testing of logger.py
# import sys
# from networksecurity.logging.logger import logging
# from networksecurity.exception.exception import NetworkSecurityException

# if __name__=="__main__":
#     logging.info("✅ Starting Logging test...!")
