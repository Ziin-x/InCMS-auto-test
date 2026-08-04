import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel

yaml_path = os.path.join(YAML_PREFIX_PATH, "group_management","code_rules.yml")

class CodeRulesData(BaseModel):
    code_rule_prefix: str
    code_rule_custom: str

    @classmethod
    def get_data(cls):
        data = from_yaml(cls,yaml_path)
        return data