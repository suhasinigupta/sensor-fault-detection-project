from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact ,ModelEvaluationArtifact, ClassificationMetricArtifact
from sensor.logger import logging
from sensor.exception import SensorException

from sensor.utils.main_utils import read_yaml_file, write_yaml_file
import os, sys

class ModelPusher:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig, model_trainer_artifact:ModelTrainerArtifact):
      try :
        self.model_evaluation_config=model_evaluation_config
        self.model_trainer_artifact=model_trainer_artifact
      except Exception as e:
         raise SensorException(e,sys)
      
      