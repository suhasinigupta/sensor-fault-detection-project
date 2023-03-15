from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
import pandas as pd
import sys, os
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
           self.data_ingestion_artifact=data_ingestion_artifact
           self.data_validation_config=data_validation_config
           self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self, dataframe=pd.DataFrame)->bool:
        try:
            length_of_cols=len(self._schema_config["columns"])
            logging.info(f"Length of columns should be : [{length_of_cols}] ")
            if len(dataframe.columns)==length_of_cols :
                return True
            return False

        except Exception as e:
            raise SensorException(e,sys)
        
    def is_numerical_columns_exists(self, dataframe:pd.DataFrame)->bool:
        try:
            num_cols_status= True
            numerical_columns=self._schema_config["numerical_columns"]

    
            df_cols= dataframe.columns

            missing_num_cols=[]
            for num_cols in numerical_columns:
                if num_cols not in df_cols:
                    num_cols_status=False
                    missing_num_cols.append(num_cols)
                logging.info(f"Missing numerical columns are [{missing_num_cols}]")
                return num_cols_status
        except Exception as e:
            raise SensorException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
        
    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df=pd.DataFrame, threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if is_same_dist.pvalue>=threshold :
                    is_found=False
                    status=False
                else :
                    is_found=True
                report.update({column:{"pvalue":float(is_same_dist.pvalue),"drift_status":is_found}})

            drift_rep_file_path=self.data_validation_config.drift_report_file_path

            os.makedirs(os.path.dirname(drift_rep_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_rep_file_path,content=report,replace=True)

            return status
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message=""
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            # Reading data from train and test file location
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            # Validate number of columns
            status= self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns"
            status= self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns"

            # validate numerical columns
            status= self.is_numerical_columns_exists(train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all numerical columns"
            status= self.is_numerical_columns_exists(test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all numerical columns"

            if len(error_message)>0:
                raise Exception(error_message)
            
            # finding drift report
            status=self.detect_dataset_drift(train_dataframe, test_dataframe)
            data_validation_artifact=DataValidationArtifact(validation_status=status,
                                                            valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                                                            valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                                                            invalid_test_file_path=None,
                                                            invalid_train_file_path=None,
                                                            drift_report_file_path=self.data_validation_config.drift_report_file_path)
            logging.info(f"Data validation artifact is [{data_validation_artifact}]")
            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
