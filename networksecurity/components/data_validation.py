from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  # ADD to constant folder
        except  Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f'Required number of columns: {number_of_columns}')
            logging.info(f'Dataframe has columns : {len(dataframe.columns)}')

            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    # def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
    #     try:
    #         # Initialize drift status to True (no drift detected)
    #         status = True
    #         report = {}

    #         logging.info("Starting dataset drift detection...")

    #         for column in base_df.columns:
    #             if column not in current_df.columns:
    #                 logging.warning(f"Column {column} is missing in the current dataset.")
    #                 continue
                
    #             d1 = base_df[column]
    #             d2 = current_df[column]

    #             logging.info(f"Checking drift for column: {column}...")

    #             # Perform Kolmogorov-Smirnov test
    #             ks_test = ks_2samp(d1, d2)
    #             p_value = ks_test.pvalue
    #             logging.info(f"Column: {column}, p-value: {p_value}")

    #             if p_value <= threshold:
    #                 # Drift detected: p-value <= threshold
    #                 is_found = True
    #                 status = False
    #             else:
    #                 # No drift detected: p-value > threshold
    #                 is_found = False

    #             # Add result to the drift report
    #             report[column] = {
    #                 "p_value": float(p_value),
    #                 "drift_status": is_found
    #             }

    #         # File path for the drift report
    #         drift_report_file_path = self.data_validation_config.drift_report_file_path
    #         logging.info(f"Saving drift report to {drift_report_file_path}")

    #         # Create directory if it doesn't exist
    #         os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

    #         # Write the drift report to a YAML file
    #         write_yaml_file(file_path=drift_report_file_path, content=report)

    #         logging.info(f"Drift report saved to {drift_report_file_path}")
    #         return status

    #     except Exception as e:
    #         logging.error(f"Error during dataset drift detection: {e}")
    #         raise NetworkSecurityException(e, sys)
    
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            status = True
            report = {}
            logging.info("Starting dataset drift detection...")

            for column in base_df.columns:
                if column not in current_df.columns:
                    logging.warning(f"Column {column} is missing in the current dataset.")
                    continue

                d1 = base_df[column]
                d2 = current_df[column]

                if not pd.api.types.is_numeric_dtype(d1):
                    logging.warning(f"Skipping non-numeric column: {column}")
                    continue

                ks_test = ks_2samp(d1, d2)
                p_value = ks_test.pvalue

                drift_detected = p_value <= threshold
                if drift_detected:
                    status = False

                report[column] = {
                    "p_value": float(p_value),
                    "drift_status": drift_detected
                }

            # Add summary
            total_columns = len(report)
            drifted_columns = sum(1 for col in report.values() if col["drift_status"])
            summary = {
                "total_columns": total_columns,
                "drifted_columns": drifted_columns,
                "drift_percentage": round((drifted_columns / total_columns) * 100, 2)
            }
            report["summary"] = summary

            # Paths
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            csv_report_path = drift_report_file_path.replace(".yaml", ".csv")
            html_report_path = drift_report_file_path.replace(".yaml", ".html")

            # Save YAML
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            # Save CSV & HTML
            report_df = pd.DataFrame([
                {"column": col, **details}
                for col, details in report.items()
                if col != "summary"
            ])
            report_df.to_csv(csv_report_path, index=False)
            report_df.to_html(html_report_path, index=False)

            # Visualize drifted columns
            import matplotlib.pyplot as plt
            import seaborn as sns

            #drifted_columns_list = [col for col, val in report.items() if isinstance(val, dict) and val["drift_status"]]
            drifted_columns_list = [col for col, val in report.items() if isinstance(val, dict) and val.get("drift_status") is True]
            visualization_dir = os.path.join(os.path.dirname(drift_report_file_path), "drift_visualizations")
            os.makedirs(visualization_dir, exist_ok=True)

            for col in drifted_columns_list:
                plt.figure(figsize=(10, 6))
                sns.kdeplot(base_df[col], label='Train', fill=True)
                sns.kdeplot(current_df[col], label='Test', fill=True)
                plt.title(f'Distribution Comparison - {col}')
                plt.xlabel(col)
                plt.ylabel('Density')
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(visualization_dir, f'{col}_drift.png'))
                plt.close()

            logging.info(f"Drift report saved to {drift_report_file_path}, CSV: {csv_report_path}, HTML: {html_report_path}")
            return status

        except Exception as e:
            logging.error(f"Error during dataset drift detection: {e}")
            raise NetworkSecurityException(e, sys)



    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            # read file path
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validate number of columns
            train_status = self.validate_number_of_columns(dataframe=train_df)
            test_status = self.validate_number_of_columns(dataframe=test_df)

            if not train_status:
                error_message = f"Train Dataframe does not contain all columns. Expected {len(self._schema_config['columns'])} columns."
                logging.error(error_message)
                raise NetworkSecurityException(error_message, sys.exc_info())

            if not test_status:
                error_message = f"Test Dataframe does not contain all columns. Expected {len(self._schema_config['columns'])} columns."
                logging.error(error_message)
                raise NetworkSecurityException(error_message, sys.exc_info())

            
            # Check data drift 
            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            
            # Save the validated data files
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False, header=True)

            # Prepare the DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=self.data_ingestion_artifact.trained_file_path,
                invalid_train_file_path=self.data_ingestion_artifact.test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


