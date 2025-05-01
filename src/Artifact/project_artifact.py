from dataclasses import dataclass



@dataclass
class DataIngestionArtifact:
    data_dir : str

@dataclass
class DataValidationArtifact:
    train_df : str
    test_df : str