import os
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel


yaml_path = os.path.join(YAML_PREFIX_PATH, 'data_center', 'single_register_project.yml')


class CompoundCompositionInfo(BaseModel):
    smiles: str
    isomer_type: str
    sequence_dict: dict


class SingleRegisterProjectData(BaseModel):
    project_name: str
    all_project_template_dict: dict
    compound_composition_info: CompoundCompositionInfo

    @classmethod
    def get_data(cls):
        return from_yaml(cls, yaml_path)
