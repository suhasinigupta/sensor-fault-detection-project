import yaml
from sensor.exception import SensorException
import sys, os
import numpy as np
import pickle, dill

def read_yaml_file(file_path:str)->dict:
    try :
      with open(file_path, "rb") as obj :
        return yaml.safe_load(obj)
    except Exception as e:
       raise SensorException(e,sys)
    
def write_yaml_file(file_path:str, content:object, replace:bool=False)->None:
   try:
        if replace:
           if os.path.exists(file_path):
               os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exists_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content,file)
   except Exception as e:
      raise SensorException(e, sys)
   
def save_numpy_array_data(filepath:str, arr=np.array):
   try:
      dir_path=os.path.dirname(filepath)
      os.makedirs(dir_path,exists_ok=True)
      with open(filepath, "wb") as file_obj:
         np.save(file_obj, arr)
   except Exception as e:
      raise SensorException(e,sys)
   
def load_numpy_array_data(filepath:str)->np.array:
   try:
      with open(filepath,"rb") as obj:
         return np.load(obj)
   except Exception as e:
      raise SensorException(e,sys)
   
def save_object(filepath:str, obj:object):
   try:
      os.makedirs(os.path.dirname(filepath), exist_ok=True)
      with open(filepath,"wb") as file_obj:
         dill.dump(obj,file_obj)
   except Exception as e:
      raise SensorException(e,sys)
   
def load_object(filepath:str)->object:
   try:
      if not os.path.exists(filepath):
        raise Exception(f"filepath {filepath} doen not exists")
      with open(filepath,"rb") as file_obj:
         dill.load(file_obj)
         return dill
   except Exception as e:
      raise SensorException(e,sys)