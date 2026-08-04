import os
from datetime import datetime
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel, field_validator

yaml_path = os.path.join(YAML_PREFIX_PATH,'data_center','single_register.yml')

class SingleRegisterData(BaseModel):
    add_module_list: list
    batch_number: str = ""
    register_amount: str

    @field_validator("batch_number", mode="before")
    @classmethod
    def fill_batch_number(cls, v):
        if not v or v.strip() == "":
            return f"auto_test_batch_member_{datetime.now().strftime('%Y/%m/%d/%H%M%S')}"
        return v

    @classmethod
    def get_data(cls):
        data = from_yaml(cls,yaml_path)
        return data
