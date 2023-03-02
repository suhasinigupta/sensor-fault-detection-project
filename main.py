from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

if __name__=='__main__' :
   trainin_pip_config= TrainingPipelineConfig()
   data_ingestion_config= DataIngestionConfig(trainin_pip_config)
   print(data_ingestion_config.__dict__)
