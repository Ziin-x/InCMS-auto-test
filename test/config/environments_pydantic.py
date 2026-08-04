import os
from utils.load_yaml import from_yaml

from pydantic import BaseModel

yaml_path = os.path.join(os.path.dirname(__file__), "environment.yaml")

class Environment(BaseModel):
    name: str
    url:str
    username:str
    password:str
    member_username: str
    member_password: str
    group_name: str

    @classmethod
    def get_data(cls):
        return from_yaml(cls, yaml_path)


