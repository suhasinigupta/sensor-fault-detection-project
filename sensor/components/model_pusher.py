import os,sys
from sensor.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_object
import shutil

class ModelPusher:
     def __init__(self, model_pusher_config:ModelPusherConfig, model_evaluation_artifact:ModelEvaluationArtifact):
          try:
              self.model_pusher_config=model_pusher_config
              self.model_evaluation_artifact=model_evaluation_artifact

          except Exception as e:
               raise SensorException(e,sys)
          
     def initiate_model_pusher(self)->ModelPusherArtifact:
          try:
               trained_model_path=self.model_evaluation_artifact.trained_model_path
               model_file_path=self.model_pusher_config.model_file_path

               os.makedirs(self.model_pusher_config.model_pusher_dir, exists_ok=True)
               shutil.copy(src=trained_model_path, dst=model_file_path)

               saved_model_path=self.model_pusher_config.saved_model_file_path
               os.makedirs(os.path.dirname(self.model_pusher_config.saved_model_file_path), exists_ok=True)
               shutil.copy(src=trained_model_path, dest=saved_model_path)

               model_pusher_artifact=ModelPusherArtifact(saved_model_path=saved_model_path,model_file_path=model_file_path)
               logging.info("Model pusher artifact: [{model_pusher_artifact}]")
               return model_pusher_artifact
          except Exception as e:
               raise SensorException(e,sys)