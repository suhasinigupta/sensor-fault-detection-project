from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact, ClassificationMetricArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
import sys

class TrainingPipeline:

    def __init__(self):
        try:
            self.training_pipeline_config=TrainingPipelineConfig()
        #self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try :
            logging.info("Starting Data Ingestion")
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
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
        
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try :
            logging.info("Starting model trainer")
            model_trainer_config= ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer= ModelTrainer(model_trainer_config,data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Model Training Completed")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_evaluation(self,  data_validation_artifact:DataValidationConfig, 
                               model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluation:
        try :
            logging.info("Starting model evaluation")
            model_evaluation_config=ModelEvaluationConfig(self.training_pipeline_config)
            model_evaluation=ModelEvaluation(model_evaluation_config,data_validation_artifact=data_validation_artifact,
                                             model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            logging.info("ModelEvaluation Completed")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try :
           logging.info("Starting Model Pusher")
           model_pusher_config=ModelPusherConfig(self.training_pipeline_config)
           model_pusher=ModelPusher(model_pusher_config=model_pusher_config,
                                              model_evaluation_artifact=model_evaluation_artifact)
           model_pusher_artifact=model_pusher.initiate_model_pusher()
           logging.info("Model Pusher Completed")
           return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)
   
    def run_pipeline(self):
        try :
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(model_trainer_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact)
        except Exception as e:
            raise SensorException(e,sys)