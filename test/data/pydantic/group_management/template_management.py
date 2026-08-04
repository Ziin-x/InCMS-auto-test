import os
from datetime import datetime
from config.setting import YAML_PREFIX_PATH
from utils.load_yaml import from_yaml

from pydantic import BaseModel, Field

yaml_path = os.path.join(YAML_PREFIX_PATH, "group_management","template_management.yml")


def _ts():
    return datetime.now().strftime('%Y/%m/%d/%H%M%S')


class TemplateName(BaseModel):
    compound_sequence_name: str = Field(default_factory=lambda: f"化合物/序列自动化测试模板类型_{_ts()}")
    mixture_formula_name: str = Field(default_factory=lambda: f"混合物/配方自动化测试模板类型_{_ts()}")
    custom_compound_name: str = Field(default_factory=lambda: f"自定义物质自动化测试模板类型_{_ts()}")
    DNA_name: str = Field(default_factory=lambda: f"DNA自动化测试模板类型_{_ts()}")
    RNA_name: str = Field(default_factory=lambda: f"RNA自动化测试模板类型_{_ts()}")


class Parameter(BaseModel):
    parameter_name: str
    tip_message: str
    parameter_option: list


class ProjectName(BaseModel):
    compound_sequence_name: str = Field(default_factory=lambda: f"化合物/序列自动化测试项目类型_{_ts()}")
    mixture_formula_name: str = Field(default_factory=lambda: f"混合物/配方自动化测试项目类型_{_ts()}")
    custom_compound_name: str = Field(default_factory=lambda: f"自定义物质自动化测试项目类型_{_ts()}")
    DNA_name: str = Field(default_factory=lambda: f"DNA自动化测试项目类型_{_ts()}")
    RNA_name: str = Field(default_factory=lambda: f"RNA自动化测试项目类型_{_ts()}")


class ProjectCode(BaseModel):
    compound_sequence_code: str = Field(default_factory=lambda: f"compound_sequence_auto_test_code_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}")
    mixture_formula_code: str = Field(default_factory=lambda: f"mixture_formula_auto_test_code_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}")
    custom_compound_code: str = Field(default_factory=lambda: f"custom_compound_auto_test_code_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}")
    DNA_code: str = Field(default_factory=lambda: f"DNA_auto_test_code_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}")
    RNA_code: str = Field(default_factory=lambda: f"RNA_auto_test_code_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}")


class Project(BaseModel):
    projectName: ProjectName = Field(default_factory=ProjectName)
    projectCode: ProjectCode = Field(default_factory=ProjectCode)
    start_time: str
    end_time: str


class TemplateManagementData(BaseModel):
    templateName: TemplateName = Field(default_factory=TemplateName)
    fieldName: str
    parameter: Parameter
    project: Project

    @classmethod
    def get_data(cls):
        data = from_yaml(cls, yaml_path)
        return data
