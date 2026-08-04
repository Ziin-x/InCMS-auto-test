import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel

yaml_path = os.path.join(YAML_PREFIX_PATH, "plug.yaml")

class product(BaseModel):
    locator_and_url: str
    name: list

class PlugPageData(BaseModel):
    eln: product
    cms: product

    @classmethod
    def get_data(cls):
        data = from_yaml(cls, yaml_path)
        return data
