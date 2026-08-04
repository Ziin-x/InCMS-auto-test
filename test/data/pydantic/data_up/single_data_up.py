import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel


yaml_path = os.path.join(YAML_PREFIX_PATH, 'data_up', 'single_data_up.yml')


class SingleDataUpData(BaseModel):
    batch_number: str
    project_name: str
    modules_info: dict

    @classmethod
    def get_data(cls):
        return from_yaml(cls, yaml_path)
