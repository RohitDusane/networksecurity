# End-To-End-Netowrk-Security-ETL-Pipeline-Deployment-Project

<!--
# Step by step process
# Data Validation

The data validation (DV) checks if the data is consistent with the expected schema, ensuring no discrepancies in columns, data drift, or missing numerical columns. The purpose is to identify and raise an error if there are any issues with the incoming data.

## Artifacts Directory:
The data is input from the artifacts\data_ingestion folder. After validation, it will be output to the artifacts\data_validation folder.

## Key Checks to Implement:

* **Schema Validation**: Ensure the data matches the expected schema (columns, data types, etc.).
* **Data Drift**: Detect if the data distribution has shifted significantly.

* **Columns Check**: Verify if the number of columns and the presence of expected numerical columns are as expected.

* **Error Handling**:
If any of the checks fail, an error must be raised to ensure the pipeline doesn’t proceed with invalid data.

##  Step-by-Step Implementation:

1. Update Constants in the `__init__.py` file
In the `constants\training_pipeline\__init__.py` file, we’ll add the expected schema, required columns, and other constants related to the data validation.

For example:  
```
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalidated'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml' 
SCHEMA_FILE_PATH = os.path.join('data_schema','schema.yaml')
```

2. Update `config.entity` file in the entity folder. 
Create a `class DataValdiationConfig` and write the configurations.

3. Create a new file in `components\data_validation.py` filepath. This is where we create `class DataValidation`. It takes the data ingestion artifact and data validation config as inputs. The class is responsible for:

- Reading the train and test CSV files from the ingested data.
- Validating the number of columns.
- Checking for the existence of numerical columns.
- Detecting data drift.
- Generating validation reports and artifacts.

4. **Defining Data Validation Artifact**
A `DataValidationArtifact` data class is defined to encapsulate the output of the data validation process. It includes:

- validation_status: a boolean indicating if validation passed.
- Paths for validated train and test files.
- Paths for invalid train and test files.
- Path for the data drift report.
This artifact is returned after the validation process completes.

5. **Schema Definition and Usage**
A schema YAML file is created under a `data_schema directory`. This file defines:

* The expected columns and their data types.
* The list of numerical columns.
This schema is used to validate incoming data against expected structure and types. The schema file is read during data validation to ensure consistency.

6. **Reading the Schema YAML File**
A utility function `read_yaml_file` is implemented in the utils module to read YAML files and return their contents as dictionaries. This function is used to read the schema YAML file during data validation.

7.1 **Initiate Data Validation Function**
We will create a function inside the class named `initiate_data_validation`. This function will take self as input and return a `DataValidationArtifact`, which we have already imported.


7.2 **Accessing Train and Test File Paths**
Inside the initiate_data_validation function, we first retrieve the train and test file paths from the data ingestion artifact, which is part of the data ingestion component. These paths are stored in self.data_ingestion_artifact.train_file_path and self.data_ingestion_artifact.test_file_path respectively.

7.3 **Reading Train and Test Data**
We will create a static method named `read_data` to read CSV files into pandas DataFrames. This method will take a file path as input and return the corresponding DataFrame. Using a **`static method`** avoids the need to instantiate the class just to read data.

7.4 **Loading Train and Test DataFrames**
Using the read_data static method, we load the train and test datasets into DataFrames named train_data_frame and test_data_frame respectively.

7.5 **Validating Number of Columns**
Implement validate_number_of_columns(data_frame) to check if a DataFrame has the expected number of columns, based on your schema. It should return True/False.

7.6 **Applying Column Validation** to Both Datasets
Execute the column-number check for both train and test data. If either check fails, log or raise an error with an explanatory message.

7.7 **Detecting Dataset Drift**
Create detect_data_set_drift(base_df, current_df) to compare distributions of matching features between two DataFrames:

Use SciPy’s ks_2samp for continuous features.
If p-value < 0.05 → raise flag for data drift.

7.8 **Writing YAML File Utility**
Build write_yaml_file(content, file_path), which:
Ensures the target directory exists (create it if needed).
Writes content to the specified YAML file.

7.9 **Integrating Drift Detection**  
Inside initiate_data_validation:
After column validation passes, compare train vs. test data for drift.
If no drift, save both validated datasets to designated file paths.
Otherwise, record drift findings.

7.10 **Returning Data Validation Artifact**  
Return a DataValidationArtifact that includes:
validation_status (e.g., passed or failed),
paths to validated train/test data, and
path to the drift report.

7.11 **Running the Data Validation Pipeline**  
In your **`main.py`** driver script:
- Import DataValidation.
- Initialize it with the ingestion artifact and validation config.
- Call initiate_data_validation().
- Log the outcome and artifact details.
- Troubleshoot errors proactively—such as missing imports or incorrect os.makedirs usage.


-->
