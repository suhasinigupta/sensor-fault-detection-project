from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
import sys

class TrainingPipeline:

    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        #self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try :
            logging.info("Starting Data Ingestion")
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed and artifact is {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationConfig:
        try :
            logging.info("Starting data Validation")
            data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()

            logging.info("Data Validation completed")
            return data_validation_config
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try :
            logging.info("Starting Data Transformation")
            data_transformation_entity=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact,data_transformation_entity)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Data Transformation Completed")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_trainer(self):
        try :
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_evaluation(self):
        try :
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_data_pusher(self):
        try :
            pass
        except Exception as e:
            raise SensorException(e,sys)
   
    def run_pipeline(self):
        try :
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
        except Exception as e:
            raise SensorException(e,sys)