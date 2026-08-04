# baseframe.py 或放在 basepage 同文件
import re
from utils.log import logger


class baseframe:
    """iframe 操作封装，使其像 Page 对象一样使用"""
    def __init__(self, frame):
        """frame: Playwright Frame 对象"""
        self.frame = frame

    def find(self, locator_desc):
        """在 frame 内定位元素"""
        if hasattr(locator_desc, 'click') and hasattr(locator_desc, 'fill'):
            return locator_desc
        if isinstance(locator_desc, str):
            return self.frame.locator(locator_desc)
        if isinstance(locator_desc, tuple):
            strategy = locator_desc[0]
            if strategy == "text":
                return self.frame.get_by_text(locator_desc[1])
            elif strategy == "role":
                return self.frame.get_by_role(locator_desc[1], name=re.compile(locator_desc[2]))
            elif strategy == "placeholder":
                return self.frame.get_by_placeholder(locator_desc[1])
            elif strategy == "selector":
                raw_selector = locator_desc[1]
                # 类名自动补点逻辑
                if ' ' in raw_selector and not any(ch in raw_selector for ch in '.#[>+~'):
                    classes = raw_selector.split()
                    css_selector = '.' + '.'.join(classes)
                elif ' ' not in raw_selector and not any(ch in raw_selector for ch in '.#[>+~'):
                    css_selector = '.' + raw_selector
                else:
                    css_selector = raw_selector
                loc = self.frame.locator(css_selector)
                if len(locator_desc) == 3:
                    loc = loc.filter(**locator_desc[2])
                return loc
        raise ValueError(f"不支持的定位描述: {locator_desc}")

    def click(self, locator_desc):
        self.frame.wait_for_timeout(200)
        loc = self.find(locator_desc)
        try:
            logger.debug(f"在 frame 内尝试点击元素：{locator_desc}")
            loc.click()
            logger.info(f"在 frame 内点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"在 frame 内点击元素失败：{locator_desc}，错误：{e}")
            raise

    # 判断元素出现与状态
    def wait_for(self, locator_desc,state,timeout=10000):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"开始等待元素出现：{locator_desc}，状态：{state}")
            loc.wait_for(state=state,timeout=timeout)
            logger.info(f"等待元素出现成功：{locator_desc}，状态：{state}")
        except Exception as e:
            logger.error(f"等待元素出现失败：{locator_desc}，状态：{state}，错误：{e}")
            raise

    # 滚动
    def scroll_to_element(self, locator_desc, block=None):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试滚动到元素：{locator_desc}到窗口内")
            if block is None:
                # 默认行为：滚动到视野内（不保证中央）
                loc.scroll_into_view_if_needed()
                logger.debug(f"滚动到元素（默认视野内）：{locator_desc}")
            else:
                # 精确滚动到指定对齐位置
                loc.evaluate(f"el => el.scrollIntoView({{block: '{block}'}})")
                logger.debug(f"滚动到元素（block={block}）：{locator_desc}")
            logger.info(f"滚动到元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"滚动到元素失败：{locator_desc}，错误：{e}")
            raise

    def click_all(self, locator_desc):
        all_element_loc = self.find(locator_desc).all()
        try:
            logger.debug(f"尝试点击所有可见元素：{locator_desc}")
            for element_loc in all_element_loc:
                if element_loc.is_visible():
                    element_loc.click()
            logger.info(f"点击所有可见元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"点击所有可见元素失败：{locator_desc}，错误：{e}")
            raise

    def fill(self, locator, text):
        self.frame.wait_for_timeout(200)
        loc = self.find(locator)
        try:
            logger.debug(f"在 frame 内的{locator}元素尝试输入内容：{text}")
            loc.fill(text)
            logger.info(f"在 frame 内的{locator}元素输入内容成功：{text}")
        except Exception as e:
            logger.error(f"在 frame 内的{locator}元素输入内容失败：{text}，错误：{e}")
            raise

    def press(self, locator_desc, key):
        """在指定元素上模拟按键（例如 'Enter', 'Tab', 'Escape'）"""
        loc = self.find(locator_desc)
        loc.press(key)

    def get_text(self, locator_desc):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试获取元素：{locator_desc}中的值")
            # 获取元素的标签名（小写）
            tag_name = loc.evaluate("el => el.tagName.toLowerCase()")
            if tag_name in ('input', 'textarea', 'select'):
                # 对于表单控件，获取 value 属性
                value = loc.input_value()
            else:
                # 先检查子元素是否有 input/textarea/select
                # 过滤hidden，只取可见的输入框
                child_input = loc.locator('input:not([type="hidden"]), textarea, select')
                if child_input.count() > 0:
                    value = child_input.first.input_value()
                else:
                    # 普通元素获取 inner_text
                    value = loc.inner_text()
            logger.info(f"获取元素：{locator_desc}中的值成功：{value}")
            return value
        except Exception as e:
            logger.error(f"获取元素：{locator_desc}中的值失败,错误：{e}")
            raise

    def click_right(self, locator_desc):
        self.frame.wait_for_timeout(200)
        loc = self.find(locator_desc)
        try:
            logger.debug(f"在 frame 内尝试右键点击元素：{locator_desc}")
            loc.click(button="right")
            logger.info(f"在 frame 内右键点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"在 frame 内右键点击元素失败：{locator_desc}，错误：{e}")
            raise

    def click_canvas(self, canvas_locator):
        self.frame.wait_for_timeout(200)
        """canvas 相对坐标点击，传入 (locator_desc, (x, y)) 格式"""
        loc = self.find(canvas_locator[0])
        x, y = canvas_locator[1]
        try:
            logger.debug(f"在 frame 内尝试点击 canvas：{canvas_locator}")
            loc.click(position={"x": x, "y": y})
            logger.info(f"在 frame 内点击 canvas 成功：{canvas_locator}")
        except Exception as e:
            logger.error(f"在 frame 内点击 canvas 失败：{canvas_locator}，错误：{e}")
            raise

    def click_canvas_right(self, canvas_locator):
        self.frame.wait_for_timeout(200)
        loc = self.find(canvas_locator[0])
        x, y = canvas_locator[1]
        try:
            logger.debug(f"在 frame 内尝试右键点击 canvas：{canvas_locator}")
            loc.click(button="right", position={"x": x, "y": y})
            logger.info(f"在 frame 内右键点击 canvas 成功：{canvas_locator}")
        except Exception as e:
            logger.error(f"在 frame 内右键点击 canvas 失败：{canvas_locator}，错误：{e}")
            raise

    def input_file(self, locator_desc, file_path):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"在 frame 内尝试对元素：{locator_desc}上传文件：{file_path}")
            loc.set_input_files(file_path)
            logger.info(f"在 frame 内上传文件成功：{file_path}")
        except Exception as e:
            logger.error(f"在 frame 内上传文件失败：{file_path}，错误：{e}")
            raise

    def enter(self):
        try:
            logger.debug("回车")
            self.frame.page.keyboard.press("Enter")
            logger.info("回车成功")
        except Exception as e:
            logger.error(f"回车失败，错误：{e}")
            raise

    def get_frame(self, iframe_selector):
        """
        从当前 frame 继续获取子 iframe（支持嵌套）
        """
        if isinstance(iframe_selector, tuple):
            strategy = iframe_selector[0]
            if strategy == "name":
                frame_name = iframe_selector[1]
                inner_frame = self.frame.frame(name=frame_name)
                if inner_frame is None:
                    raise RuntimeError(f"未找到 name='{frame_name}' 的 frame")
                return baseframe(inner_frame)
            elif strategy == "selector":
                css_selector = iframe_selector[1]
                iframe_loc = self.frame.locator(css_selector)
                iframe_loc.wait_for(state='attached')
                element_handle = iframe_loc.element_handle()
                inner_frame = element_handle.content_frame()
                if inner_frame is None:
                    raise RuntimeError(f"无法获取 iframe 的 content frame，选择器: {css_selector}")
                return baseframe(inner_frame)
            else:
                raise ValueError(f"不支持的 frame 定位策略: {strategy}")
        elif isinstance(iframe_selector, str):
            if iframe_selector.startswith("name="):
                frame_name = iframe_selector[5:]
                inner_frame = self.frame.frame(name=frame_name)
                if inner_frame is None:
                    raise RuntimeError(f"未找到 name='{frame_name}' 的 frame")
                return baseframe(inner_frame)
            else:
                iframe_loc = self.frame.locator(iframe_selector)
                iframe_loc.wait_for(state='attached')
                element_handle = iframe_loc.element_handle()
                inner_frame = element_handle.content_frame()
                if inner_frame is None:
                    raise RuntimeError(f"无法获取 iframe 的 content frame，选择器: {iframe_selector}")
                return baseframe(inner_frame)
        else:
            raise TypeError("iframe_selector 必须是字符串或元组")