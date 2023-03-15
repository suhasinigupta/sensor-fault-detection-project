from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact ,ModelEvaluationArtifact, ClassificationMetricArtifact, DataValidationArtifact
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.ML.metric.classification_metric import get_classification_score
from sensor.utils.main_utils import save_object, load_object, write_yaml_file
from sensor.ML.model.estimator import ModelResolver , TargetValueMapping
import os, sys
import pandas as pd
from sensor.constant.training_pipeline import TARGET_COLUMN

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig, model_trainer_artifact:ModelTrainerArtifact, 
                 data_validation_artifact:DataValidationArtifact):
      try :
        logging.info("9")
        self.model_evaluation_config=model_evaluation_config
        self.model_trainer_artifact=model_trainer_artifact
        self.data_validation_artifact=data_validation_artifact
      except Exception as e:
         raise SensorException(e,sys)
      
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
       try :
        
          valid_train_file_path=self.data_validation_artifact.valid_train_file_path
          valid_test_file_path=self.data_validation_artifact.valid_test_file_path
        
          train_df=pd.read_csv(valid_train_file_path)
          test_df=pd.read_csv(valid_test_file_path)
     
          df=pd.concat([train_df,test_df])
          y_true=df[TARGET_COLUMN]
          y_true=y_true.replace(TargetValueMapping().to_dict())
          
          df=df.drop(columns=[TARGET_COLUMN], axis=1)
          train_model_file_path=self.model_trainer_artifact.trained_model_file_path
 
          model_resolver=ModelResolver()
          
          is_model_accepted=True

          if not model_resolver.is_model_exists():
               
               model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=is_model_accepted,
                                                               improved_accuracy=None,
                                                               best_model_path=None,
                                                               trained_model_path=train_model_file_path,
                                                               train_model_metric_artifact=self.model_trainer_artifact.test_model_metric_artifact,
                                                               best_model_metric_artifact=None)
                                                               
               logging.info(f"Model Evaluation Artifact: [{model_evaluation_artifact}]")
               return model_evaluation_artifact
          
          latest_model_path=model_resolver.get_best_model_path()
        
          latest_model=load_object(latest_model_path)
          train_model=load_object(train_model_file_path)
         
          y_train_pred=train_model.predict(df.drop(columns=TARGET_COLUMN))
          y_latest_pred=latest_model.predict(df.drop(columns=TARGET_COLUMN))
         
          trained_metric=get_classification_score(y_true, y_train_pred)
          latest_metric=get_classification_score(y_true, y_latest_pred)

          improved_accuracy=trained_metric.f1_score -latest_metric.f1_score
          if improved_accuracy> self.model_evaluation_config.change_threshold:
             is_model_accepted=True

          else:
              is_model_accepted=False

          model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=is_model_accepted,
                                                               improved_accuracy=improved_accuracy,
                                                               best_model_path=latest_model_path,
                                                               trained_model_path=train_model_file_path,
                                                               train_model_metric_artifact=trained_metric,
                                                               best_model_metric_artifact=latest_metric)
                                                               
          model_eval_report=model_evaluation_artifact.__dict__()
          write_yaml_file(self.model_evaluation_config.report_file_path,model_eval_report)
          logging.info(f"Model Evaluation Artifact: [{model_evaluation_artifact}]")
          return model_evaluation_artifact

       except Exception as e:
          raise SensorException(e,sys)
      
      