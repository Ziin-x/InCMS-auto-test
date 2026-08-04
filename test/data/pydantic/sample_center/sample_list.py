import os
from datetime import datetime
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel, field_validator

yaml_path = os.path.join(YAML_PREFIX_PATH,'sample_center','sample_list.yml')

class SampleListData(BaseModel):
    current_amount: str
    sample_name: str = ""
    sample_form: str
    batch_current_amount: str
    sample_tube_type: str

    @field_validator("sample_name", mode="before")
    @classmethod
    def fill_sample_name(cls, v):
        if not v or v.strip() == "":
            return f"autotest_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return v

    @classmethod
    def get_data(cls):
        data = from_yaml(cls, yaml_path)
        return data
