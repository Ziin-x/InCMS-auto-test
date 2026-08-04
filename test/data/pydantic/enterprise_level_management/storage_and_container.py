import os
from datetime import datetime
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel, Field

yaml_path = os.path.join(YAML_PREFIX_PATH,"enterprise_level_management","storage_and_container.yml")


def _ts():
    return datetime.now().strftime('%Y/%m/%d/%H%M%S')


class TypeName(BaseModel):
    location: str = Field(default_factory=lambda: f"自动化测试位置_{_ts()}")
    box: str = Field(default_factory=lambda: f"自动化测试盒子_{_ts()}")
    hole_plate: str = Field(default_factory=lambda: f"自动化测试孔板_{_ts()}")
    sample_tube: str = Field(default_factory=lambda: f"自动化测试样本管_{_ts()}")


class Abbreviation(BaseModel):
    location: str = Field(default_factory=lambda: f"auto_test_location_{_ts()}")
    box: str = Field(default_factory=lambda: f"auto_test_box_{_ts()}")
    hole_plate: str = Field(default_factory=lambda: f"auto_test_hole_plate_{_ts()}")
    sample_tube: str = Field(default_factory=lambda: f"auto_test_sample_tube_{_ts()}")


class StorageAndContainerData(BaseModel):
    type_name: TypeName
    abbreviation: Abbreviation
    field_title: str = Field(default_factory=lambda: f"自动化测试字段标题_{_ts()}")

    @classmethod
    def get_data(cls):
        data = from_yaml(cls, yaml_path)
        return data
