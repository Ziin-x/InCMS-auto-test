import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel


yaml_path = os.path.join(YAML_PREFIX_PATH, 'visualization', 'visualization.yml')


class VisualizationData(BaseModel):
    chart_type: str
    project_name: str
    template_name: str
    x_field: str
    y_field: str

    @classmethod
    def get_data(cls):
        return from_yaml(cls, yaml_path)
