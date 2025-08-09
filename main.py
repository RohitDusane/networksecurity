#-------------------Data TRANSFORMATION test------------------------------------------------------
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
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

        logging.info(f'Initiating Data Ingestion')
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed successfully")
        logging.info(f"Data Ingestion Artifact details: {data_ingestion_artifact}")
        print(data_ingestion_artifact)

        
        # Data Validation
        data_validation_config =DataValidationConfig(training_pipeline_config)
        # Initialise Data Validation
        data_validation= DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info(f"Initiating Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation completed successfully")
        logging.info(f"Data Validation Artifact details: {data_validation_artifact}")
        print(data_validation_artifact)

        # Data Transformation
        data_trasformation_config =DataTransformationConfig(training_pipeline_config)
        
        # Initialise Data Validation
        data_transformation= DataTransformation(data_validation_artifact, data_trasformation_config)
        
        logging.info(f"Initiating Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data Transformation completed successfully")
        logging.info(f"Data Transformation Artifact details: {data_transformation_artifact}")
        print(data_transformation_artifact)

        # Model Trainer
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        
        # Initialise Data Validation
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)

        logging.info(f"Initiating Model Trainer")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info(f"Model Trained Successfully")
        logging.info(f"Model Trainer Artifact details: {model_trainer_artifact}")
        print(model_trainer_artifact)

        logging.info("Pipeline execution(Data ingestion & validation) completed successfully")

    except Exception as e:
        logging.exception("An error occurred during pipeline execution.")
        raise NetworkSecurityException(e,sys)









#-------------------Data Validation test------------------------------------------------------
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
# from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
# from networksecurity.components.data_ingestion import DataIngestion
# from networksecurity.components.data_validation import DataValidation
# import os
# import sys

# if __name__ == '__main__':
#     try:
#         logging.info("Starting Network Security Training Pipeline")
#         # Set up the overall training pipeline config
#         training_pipeline_config = TrainingPipelineConfig()
        
#         # Data Ingestion
#         data_ingestion_config = DataIngestionConfig(training_pipeline_config)  # Pass the instance
#         data_ingestion = DataIngestion(data_ingestion_config)

#         logging.info(f'Initiating data ingestion')
#         data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
#         logging.info("Data ingestion completed successfully")
#         logging.info(f"Data ingestion artifact details: {data_ingestion_artifact}")
#         print(data_ingestion_artifact)

        
#         # Data Validation
#         data_validation_config =DataValidationConfig(training_pipeline_config)
#         # Initialise Data Validation
#         data_validation= DataValidation(data_ingestion_artifact, data_validation_config)
        
#         logging.info(f"Initiating data validation")
#         data_validation_artifact = data_validation.initiate_data_validation()
#         logging.info(f"Data validation completed successfully")
#         logging.info(f"Data validation artifact details: {data_validation_artifact}")
#         print(data_validation_artifact)


#         logging.info("Pipeline execution(Data ingestion & validation) completed successfully")

#     except Exception as e:
#         logging.exception("An error occurred during pipeline execution.")
#         raise NetworkSecurityException(e,sys)




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
