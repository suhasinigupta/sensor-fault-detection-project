from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact

if __name__=='__main__' :
  trainin_pip_config= TrainingPipelineConfig()
  data_ingestion_config= DataIngestionConfig(trainin_pip_config)
  train_obj= TrainingPipeline()
  train_obj.run_pipeline()