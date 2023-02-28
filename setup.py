from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str] :
    '''
    This function returns list of requirements which will used by setup method
    '''
    req_list:List[str]=[]
    with open("requirements.txt") as obj:
        req_list= obj.readlines().remove("-e.")

    return req_list


  
  
setup(
     name= "setup file",
     author="suhasini",
     version="0.0.1",
     packages=find_packages(),
     install_requires=get_requirements()
     )