# Testing of logger.py
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

if __name__=="__main__":
    logging.info("✅ Starting Logging test...!")

if __name__ == "__main__":
    try:
        logging.info("Starting Exception Handling...")
        a=2/0
        print(a)
    except Exception as e:
        raise CustomException(e,sys)