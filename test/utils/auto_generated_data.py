import random
from datetime import datetime
from typing import Literal


def generate_dna() -> str:
    """生成随机DNA序列（A/T/C/G）"""
    bases = "ATCG"
    length = random.randint(3, 1000)
    return "".join(random.choices(bases, k=length))

def generate_rna() -> str:
    """生成随机RNA序列（A/U/C/G）"""
    bases = "AUCG"
    length = random.randint(3, 1000)
    return "".join(random.choices(bases, k=length))

def generate_batch_number(register_type: Literal['DNA', 'RNA', '化合物/序列', '混合物/配方', '自定义物质']) -> str:
    """
    自动生成批号
    格式: 注册类型缩写_月日时分秒
    示例: dna_0618105530
    """
    # 注册类型映射
    type_map = {
        'DNA': 'dna',
        'RNA': 'rna',
        '化合物/序列': 'hhw',  # 自定义
        '混合物/配方': 'pf',  # 配方
        '自定义物质': 'zdy'  # 化合物/混合物
    }
    # 获取缩写
    prefix = type_map.get(register_type)
    if not prefix:
        raise ValueError(f"不支持的注册类型: {register_type}")
    # 获取当前时间: 月日时分秒 (6位或8位)
    now = datetime.now()
    time_str = now.strftime("%m%d_%H%M%S")  # 月日时分秒，如 0618_105530
    return f"{prefix}_{time_str}"

def generate_register_amount(max_value:int = 1000):
    # 支持的单位列表
    units = ['ug', 'mg', 'g', 'kg', 't', 'uL', 'mL', 'l', 'pcs']
    # 随机选择一个单位
    unit = random.choice(units)
    value = random.randint(1, int(max_value))
    return value,unit

def generate_register_template_name(register_type):
    #生成测试的模板名称
    current_date = datetime.now().strftime("%m%d")
    return f'auto_test_{register_type}模板（{current_date}）'

def generate_project_name(register_type: str = ""):
    """自动生成项目名称
    格式: auto_test项目（月日）
    示例: auto_test项目（0629）
    """
    current_date = datetime.now().strftime("%m%d")
    if register_type:
        return f'auto_test_{register_type}项目（{current_date}）'
    return f'auto_test项目（{current_date}）'






