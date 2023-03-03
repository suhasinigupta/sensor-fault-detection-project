import yaml
from sensor.exception import SensorException
import sys, os

def read_yaml_file(file_path:str)->dict:
    try :
      with open(file_path, "rb") as obj :
        return yaml.safe_load(obj)
    except Exception as e:
       raise SensorException(e,sys)
    
def write_yaml_file(file_path:str, content:object, repalce:bool=False)->None:
   try:
        if repalce:
           if os.path.exists(file_path):
               os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exists_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content,file)
   except Exception as e:
      raise SensorException(e, sys)
   