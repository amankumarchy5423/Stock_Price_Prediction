from dataclasses import dataclass



@dataclass
class DataIngestionArtifact:
    data_dir : str

@dataclass
class DataValidationArtifact:
    data_dir : str