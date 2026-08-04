from utils.log import logger


def is_visible(self, locator_desc, timeout=1000):
    try:
        loc = self.find(locator_desc)
        loc.wait_for(state="visible", timeout=timeout)
        logger.info(f"元素可见: {locator_desc}")
        return True
    except Exception as e:
        logger.warning(f"元素不可见或不存在: {locator_desc}, 错误: {e}")
        return False