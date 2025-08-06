
#-------------------Data Validation test------------------------------------------------------
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
import os
import sys

if __name__ == '__main__':
    try:
        logging.info("Starting Network Security Training Pipeline")
        # Set up the overall training pipeline config
        training_pipeline_config = TrainingPipelineConfig()
        
        # Data Ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)  # Pass the instance
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info(f'Initiating data ingestion')
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully")
        logging.info(f"Data ingestion artifact details: {data_ingestion_artifact}")
        print(data_ingestion_artifact)

        
        # Data Validation
        data_validation_config =DataValidationConfig(training_pipeline_config)
        # Initialise Data Validation
        data_validation= DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info(f"Initiating data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data validation completed successfully")
        logging.info(f"Data validation artifact details: {data_validation_artifact}")
        print(data_validation_artifact)


        logging.info("Pipeline execution(Data ingestion & validation) completed successfully")

    except Exception as e:
        logging.exception("An error occurred during pipeline execution.")
        raise NetworkSecurityException(e,sys)




#-------------------Data Ingestion test------------------------------------------------------
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
# from networksecurity.entity.artifact_entity import DataIngestionArtifact
# from networksecurity.components.data_ingestion import DataIngestion
# import os
# import sys
# from networksecurity.components.data_validation import DataValidation
# from networksecurity.entity.config_entity import DataValidationConfig



# if __name__=='__main__':
#     try:
#         training_pipeline_config = TrainingPipelineConfig()  # Create an instance
#         data_ingestion_config = DataIngestionConfig(training_pipeline_config)  # Pass the instance
#         data_ingestion = DataIngestion(data_ingestion_config)
#         logging.info(f'Initiate Data Ingestion')
#         data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
#         print(data_ingestion_artifact)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)


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
