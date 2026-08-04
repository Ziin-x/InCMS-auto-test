from utils.log import logger

import yaml


def yaml_load(file_path:str,encoding:str = 'utf-8') :
    """
    加载yaml文件
    :param file_path: 文件路径
    :param encoding: 文件编码
    :return:
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"[YAML Loader] 解析失败: {file_path}\n{e}")
        return None
    except Exception as e:
        logger.error(f"[YAML Loader] 读取异常: {file_path}\n{e}")
        return  None
    if isinstance(data, list):
        logger.error(f"[YAML Loader] 顶层必须是列表: {file_path}")
        return  None
    return data

def from_yaml(cls,yaml_path):
    data = yaml_load(yaml_path)
    if data is None:
        return None
    return cls.model_validate(data)
