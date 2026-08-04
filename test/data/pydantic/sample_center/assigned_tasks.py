import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel

yaml_path = os.path.join(YAML_PREFIX_PATH, "sample_center", "assigned_tasks.yml")


class AssignedTasksData(BaseModel):
    project_name: str

    @classmethod
    def get_data(cls):
        return from_yaml(cls, yaml_path)
