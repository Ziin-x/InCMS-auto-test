import os
from datetime import datetime

from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel, field_validator

yaml_path = os.path.join(YAML_PREFIX_PATH, "eln", "eln.yml")


class ELNData(BaseModel):
    notebook_name: str = ""

    @field_validator("notebook_name", mode="before")
    @classmethod
    def fill_notebook_name(cls, v):
        if not v or v.strip() == "":
            return f"auto_test{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return v

    @classmethod
    def get_data(cls):
        data = from_yaml(cls, yaml_path)
        return data
