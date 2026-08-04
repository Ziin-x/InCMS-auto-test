import json
import os
from datetime import datetime
from utils.log import logger

_RECORD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "record_test_data", "test_record")


def _ensure_dir():
    os.makedirs(_RECORD_DIR, exist_ok=True)


def _file_path():
    """按天隔离，每天一个文件"""
    _ensure_dir()
    date_str = datetime.now().strftime("%Y%m%d")
    return os.path.join(_RECORD_DIR, f"runtime_{date_str}.json")


def set_to_test_record(key: str, value):
    """
    写入运行时数据到 JSON 文件
    用于在模板创建、项目-模板关联时保存数据，供后续用例读取

    :param key:   数据键名，如 "compound_sequence_project_name"
    :param value: 数据值，支持 str / dict / list
    """
    file_path = _file_path()
    data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    data[key] = value
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"记录运行时数据: {key}={value}")


def get_from_test_record(key: str, default=None):
    """
    从 JSON 文件读取运行时数据
    单条执行时也能读到之前创建的数据

    :param key:     数据键名
    :param default: 未找到时的默认值
    """
    file_path = _file_path()
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default


def get_all_from_test_record():
    """获取当天所有运行时数据"""
    file_path = _file_path()
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def clear_test_record():
    """清空当天的运行时数据"""
    file_path = _file_path()
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"已清空运行时数据: {file_path}")
