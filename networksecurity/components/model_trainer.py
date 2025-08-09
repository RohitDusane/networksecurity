import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object, load_numpy_array_data,load_object, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

import pickle

import mlflow   # tracking of experiment locally
mlflow.autolog()
import dagshub  # tracking os million oof experiment virtually via onnecting the github repository
dagshub.init(repo_owner='stat.data247', repo_name='networksecurity', mlflow=True)




class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self, best_model, classification_met):
        try:
            with mlflow.start_run():
                f1_score=classification_met.f1_score
                precision_score=classification_met.precision_score
                recall_score=classification_met.recall_score

                mlflow.log_metric('f1_score', f1_score)
                mlflow.log_metric('precision_score', precision_score)
                mlflow.log_metric('recall_score', recall_score)
                mlflow.log_param('model_name', best_model.__class__.__name__)
                # # ✅ Log model as artifact
                # with open("model_ml.pkl", "wb") as f:
                #     pickle.dump(best_model, f)
                # mlflow.log_artifact("model_ml.pkl")
        except Exception as e:
            logging.error(f"Error while tracking MLflow: {e}")
            raise NetworkSecurityException(f"Tracking Error: {e}", sys)
        
    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            # list all models
            models = {
                    "LogisticRegression": LogisticRegression(verbose=1),
                    "DecisionTree": DecisionTreeClassifier(),
                    "RandomForest": RandomForestClassifier(verbose=1),
                    "GradientBoosting": GradientBoostingClassifier(verbose=1),
                    "SVC": SVC(verbose=True),
                    "KNeighbors": KNeighborsClassifier(),
                    "NaiveBayes": GaussianNB(),
                    "AdaBoost": AdaBoostClassifier()
                }
            # Hyperparameters
            params = {
            "LogisticRegression": {
                "C": [0.01, 0.1, 1, 10],
                "solver": ["liblinear", "lbfgs"]
            },
            "DecisionTree": {
                "max_depth": [3, 5, 10, None],
                "min_samples_split": [2, 5, 10],
                "criterion": ["gini", "entropy"]
            },
            "RandomForest": {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 5, 10, 15],
                "min_samples_split": [2, 5],
                "criterion": ["gini", "entropy"]
            },
            "GradientBoosting": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7]
            },
            "SVC": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf"],
                "gamma": ["scale", "auto"]
            },
            "KNeighbors": {
                "n_neighbors": [3, 5, 7],
                "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan"]
            },
            "AdaBoost": {
                            "n_estimators": [50, 100, 200],
                            "learning_rate": [0.01, 0.1, 0.2]
                },
            }

            model_report, trained_models = evaluate_models(X_train, y_train, X_test, y_test, models, params)

            best_model_name = max(model_report, key=lambda name: model_report[name]["test_score"])
            best_model = trained_models[best_model_name]
            best_model_score = model_report[best_model_name]["test_score"]
            logging.info(f"Best model: {best_model_name} with test score: {best_model_score}")

        
            y_train_pred=best_model.predict(X_train)
            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            y_test_pred=best_model.predict(X_test)
            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            # Track the experiements with mlflow
            logging.info("Tracking Train model - mlflow")
            self.track_mlflow(best_model,classification_train_metric)
            print(f"""Train Dataset score: {classification_train_metric}""")
            logging.info("Tracking Train model - mlflow")
            self.track_mlflow(best_model,classification_test_metric)
            print(f"""TEST Dataset score: {classification_test_metric}""")
           

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
                
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
            
            save_model = save_object('final_models/model.pkl', best_model)
            logging.info(f"Saving the model.pkl.... : {save_model}")
            
            ## Model Trainer Artifact
            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact=classification_train_metric,
                                test_metric_artifact=classification_test_metric
                                )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
                raise NetworkSecurityException(e,sys)


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)