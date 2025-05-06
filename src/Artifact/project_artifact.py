from dataclasses import dataclass



@dataclass
class DataIngestionArtifact:
    data_dir : str

@dataclass
class DataValidationArtifact:
    data_dir : str

@dataclass
class DataTransformationArtifact:
    train_file : str
    test_file : str
    preprocessor_path : str

@dataclass
class ModelTrainerArtifact:
    model_file : str
    preprocessor_file : str

@dataclass
class ModelEvaluatorArtifact:
    report : bool
    bucket_name : str
    ml_model_key : str
    pre_model_key : str