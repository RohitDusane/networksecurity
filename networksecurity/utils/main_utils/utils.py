import yaml                   # Add to requirements.txt
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        logging.info(f"Entered the read_yaml_file method from mainutils")
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        logging.info(f"Exited the read_yaml_file method from mainutils")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        logging.info(f"Entered the write_yaml_file method from mainutils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
        logging.info(f"Exited the write_yaml_file method from mainutils")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    # try:
    #     if replace:
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #         os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #         with open(file_path, 'w') as file:
    #             yaml.dump(content, file)
    # except Exception as e:
    #     raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path:str, array:np.array):
    try:
        logging.info(f"Entered the save_numpy_array_data method from mainutils")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
        logging.info(f"Exited the save_numpy_array_data method from mainutils")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info(f"Entered the save_object method from mainutils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Exited the save_object method from mainutils")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception (f"File not Found: {file_path}")
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def load_numpy_array_data(file_path: str) -> np.ndarray:
    try:
        logging.info(f"Loading numpy array from file: {file_path}")
        with open(file_path, 'rb') as file:
            array = np.load(file)
        logging.info(f"Loaded numpy array shape: {array.shape}")
        return array
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# from sklearn.metrics import r2_score
# from sklearn.model_selection import GridSearchCV

# def evaluate_models(X_train, y_train,X_test,y_test,models,param):
#     try:
#         report = {}

#         for i in range(len(list(models))):
#             model = list(models.values())[i]
#             para=param[list(models.keys())[i]]

#             gs = GridSearchCV(model,para,cv=3)
#             gs.fit(X_train,y_train)

#             model.set_params(**gs.best_params_)
#             model.fit(X_train,y_train)

#             #model.fit(X_train, y_train)  # Train model

#             y_train_pred = model.predict(X_train)

#             y_test_pred = model.predict(X_test)

#             train_model_score = r2_score(y_train, y_train_pred)

#             test_model_score = r2_score(y_test, y_test_pred)

#             report[list(models.keys())[i]] = test_model_score

#         return report

#     except Exception as e:
#         raise NetworkSecurityException(e, sys)

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def evaluate_models(X_train, y_train, X_test, y_test, models: dict, param: dict) -> tuple[dict, dict]:
    try:
        report = {}
        best_models = {}

        for model_name, model in models.items():
            logging.info(f"Evaluating model: {model_name}")
            
            model_params = param.get(model_name, {})

            gs = GridSearchCV(model, model_params, cv=3, n_jobs=-1, verbose=0)
            gs.fit(X_train, y_train)

            best_model = gs.best_estimator_  # ✅ Fitted model
            best_models[model_name] = best_model

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = {
                "train_score": train_model_score,
                "test_score": test_model_score,
                "best_params": gs.best_params_
            }

            logging.info(f"{model_name} R2 train: {train_model_score}, test: {test_model_score}")

        return report, best_models

    except Exception as e:
        raise NetworkSecurityException(e, sys)