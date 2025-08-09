from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model= model
            logging.info("NetworkModel initialized with preprocessor and model.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self, X):
        try:
            logging.info("Starting prediction in NetworkModel.")
            x_transform = self.preprocessor.transform(X)
            y_hat = self.model.predict(x_transform)
            logging.info("Prediction completed.")
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)