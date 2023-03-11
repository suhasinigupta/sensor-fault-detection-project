import numpy as np

from sensor.logger import logging
from sensor.exception import SensorException
from sensor.configuration.mongodb_connection import MongoDBClient
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
import os

filepath=f"D:\\sensor-fault-detection-project\\aps_failure_training_set1.csv"
if __name__=='__main__':
    
    sd = SensorData()
    if DATA_INGESTION_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[DATA_INGESTION_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=filepath,collection_name=DATA_INGESTION_COLLECTION_NAME)