from utils.log import logger


def load_ele_param(ele, *param):
    try:
        logger.debug(f'向定位：{ele}中填充参数{param}')
        locator = ele.format(*param)
        logger.info('填充成功')
    except (IndexError, ValueError, AttributeError) as e:
        logger.error(f'填充参数失败：{e}')
        raise e
    except Exception as e:
        logger.error('未知错误')
        raise e
    return locator