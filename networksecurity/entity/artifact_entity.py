"""
Data Ingestion Artifact
The output of the `data ingestion component` is **encapsulated** in a `data ingestion artifact`,
which contains the train and test file paths. This is implemented as a data class.
"""

from dataclasses import dataclass

@dataclass      # acts as decorator for empty class variable
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str