from object.baseframe import baseframe
from utils.log import logger


class BasePage:
    def __init__(self, page):
        self.page = page


    # 把定位描述的解析逻辑抽离成独立方法,将（" "," "," "）的格式转变为Playwright 的 Locator 对象
    def find(self, locator_desc):
        """把定位描述翻译成 Playwright Locator"""
        if hasattr(locator_desc, 'click') and hasattr(locator_desc, 'fill'):
            return locator_desc
        if isinstance(locator_desc, str):
            return self.page.locator(locator_desc)
        if isinstance(locator_desc, tuple):
            strategy = locator_desc[0]

            if strategy == "text":
                return self.page.get_by_text(locator_desc[1])
            elif strategy == "role":
                # 使用exact=True精确匹配，避免文本中的/被Playwright内部当作正则分隔符解析
                return self.page.get_by_role(locator_desc[1], name=locator_desc[2], exact=True)
            elif strategy == "placeholder":
                return self.page.get_by_placeholder(locator_desc[1])
            elif strategy == "selector":
                raw_selector = locator_desc[1]
                loc = self.page.locator(raw_selector)
                if len(locator_desc) == 3:  # 带过滤条件
                    #将"has_text" : "string"解包为 has_text = "string"
                    loc = loc.filter(**locator_desc[2])
                return loc
        raise ValueError(f"不支持的定位描述: {locator_desc}")

    # 获取frame对象
    def get_frame(self, iframe_selector):
        if isinstance(iframe_selector, tuple):
            strategy = iframe_selector[0]
            if strategy == "name":
                frame_name = iframe_selector[1]
                frame = self.page.frame(name=frame_name)
                if frame is None:
                    raise RuntimeError(f"未找到 name='{frame_name}' 的 frame")
                return baseframe(frame)
            elif strategy == "selector":
                css_selector = iframe_selector[1]
                # 使用 CSS 选择器逻辑
                iframe_loc = self.page.locator(css_selector)
                iframe_loc.wait_for(state='attached')
                element_handle = iframe_loc.element_handle()
                frame = element_handle.content_frame()
                if frame is None:
                    raise RuntimeError(f"无法获取 iframe 的 content frame，选择器: {css_selector}")
                return baseframe(frame)
            else:
                raise ValueError(f"不支持的 frame 定位策略: {strategy}")
        elif isinstance(iframe_selector, str):
            if iframe_selector.startswith("name="):
                frame_name = iframe_selector[5:]  # 去掉 'name='
                frame = self.page.frame(name=frame_name)
                if frame is None:
                    raise RuntimeError(f"未找到 name='{frame_name}' 的 frame")
                return baseframe(frame)
            else:
                # 当作 CSS 选择器处理
                iframe_loc = self.page.locator(iframe_selector)
                iframe_loc.wait_for(state='attached')
                element_handle = iframe_loc.element_handle()
                frame = element_handle.content_frame()
                if frame is None:
                    raise RuntimeError(f"无法获取 iframe 的 content frame，选择器: {iframe_selector}")
                return baseframe(frame)
        else:
            raise TypeError("iframe_selector 必须是字符串或元组")


    # 点击元素
    def click(self, locator_desc,timeout=30000):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试点击元素：{locator_desc}")
            loc.click(timeout=timeout)
            logger.info(f"点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"点击元素失败：{locator_desc}，错误：{e}")
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


    # 滚动界面
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


    def reload(self):
        self.page.reload()
        logger.info("页面刷新完成")


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
                # 普通元素获取 inner_text
                value = loc.inner_text()
            logger.info(f"获取元素：{locator_desc}中的值成功：{value}")
            return value
        except Exception as e:
            logger.error(f"获取元素：{locator_desc}中的值失败,错误：{e}")
            raise


    # 根据接口响应等待
    def wait_according_to_the_interface(self,url,action,timeout=30000):
        logger.debug(f"开始监听 {url}，等待动作执行...")
        try:
            with self.page.expect_response(lambda response: response.url == url,timeout=timeout) as response_info:
                action()
        except TimeoutError:
            raise RuntimeError("接口响应超时，或其他原因导致的接口未响应")
        response = response_info.value
        logger.info(f"接口响应：{response.status}，判断等待是否结束")
        if response.status == 200:
            logger.info("接口响应为200，等待结束")
            return True
        else:
            raise RuntimeError(f"接口响应为 {response.status}，动作执行失效")


    def wait_for_url(self, url, timeout=10000):
        """
        等待页面 URL 匹配预期值。

        :param url: 预期 URL，支持：
                                - 完整 URL 字符串
                                - 正则表达式对象（re.compile()）
        """
        try:
            logger.debug(f"等待页面跳转：{url}")
            self.page.wait_for_url(url, timeout=timeout)
            # 等待成功后打印新 URL
            current_after = self.page.url
            logger.info(f"等待成功，当前 URL: {current_after}")
            logger.info(f"等待页面跳转成功：{url}")
        except Exception as e:
            # 超时或失败时打印当时的 URL
            current_on_error = self.page.url
            logger.error(f"等待页面跳转失败：{url}，错误：{e}")
            logger.error(f"失败时的 URL: {current_on_error}")
            raise


    # 强制点击
    def click_force(self, locator_desc):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试点击元素：{locator_desc}")
            loc.click(force=True)
            logger.info(f"点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"点击元素失败：{locator_desc}，错误：{e}")
            raise


    # 按序号点击：index=0 点击第一个，index=-1 点击最后一个，index=n 点击第n个
    def click_nth(self, locator_desc, index):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试点击元素：{locator_desc}，序号：{index}")
            loc.nth(index).click()
            logger.info(f"点击元素成功：{locator_desc}，序号：{index}")
        except Exception as e:
            logger.error(f"点击元素失败：{locator_desc}，序号：{index}，错误：{e}")
            raise

    # 右键点击
    def click_right(self, locator_desc):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试点击元素：{locator_desc}")
            loc.click(button = "right")
            logger.info(f"点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"点击元素失败：{locator_desc}，错误：{e}")
            raise


    # canvas相对坐标点击
    def click_canvas(self, canvas_locator,force=False):
        #  获取canvas元素
        loc = self.find(canvas_locator[0])
        # 获取canvas内元素的相对坐标
        try:
            logger.debug(f"尝试点击元素：{canvas_locator}")
            loc.click(position = {'x':canvas_locator[1][0],'y':canvas_locator[1][1]},force = force)
            logger.info(f"点击元素成功：{canvas_locator}")
        except Exception as e:
            logger.error(f"点击元素失败：{canvas_locator}，错误：{e}")
            raise

    # canvas相对坐标右键点击
    def click_canvas_right(self, canvas_locator):
        #  获取canvas元素
        loc = self.find(canvas_locator[0])
        # 获取canvas内元素的相对坐标
        try:
            logger.debug(f"尝试点击元素：{ canvas_locator}")
            loc.click(position = {'x': canvas_locator[1][0],'y': canvas_locator[1][1]},button = 'right')
            logger.info(f"点击元素成功：{ canvas_locator}")
        except Exception as e:
            logger.error(f"点击元素失败：{ canvas_locator}，错误：{e}")
            raise


    def click_all(self, locator_desc):
        all_element_loc = self.find(locator_desc).all()
        try:
            logger.debug(f"尝试点击所有元素：{locator_desc}")
            for element_loc in all_element_loc:
                element_loc.click()
            logger.info(f"点击元素成功：{locator_desc}")
        except Exception as e:
            logger.error(f"点击元素失败：{locator_desc}，错误：{e}")
            raise


    # 输入内容
    def fill(self, locator, text):
        loc = self.find(locator)
        try:
            logger.debug(f"尝试在{locator}输入内容：{text}")
            loc.fill(text)
            logger.info(f"在{locator}输入内容成功：{text}")
        except Exception as e:
            logger.error(f"在{locator}输入内容失败：{text}，错误：{e}")
            raise

    # 下拉选择
    def select_option(self, locator_desc, value):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试选择下拉选项：{locator_desc}，值：{value}")
            loc.select_option(value)
            logger.info(f"选择下拉选项成功：{locator_desc}，值：{value}")
        except Exception as e:
            logger.error(f"选择下拉选项失败：{locator_desc}，值：{value}，错误：{e}")
            raise


    # 对非输入框元素输入内容
    def click_and_input(self, locator_decs, text):
        loc = self.find(locator_decs)
        try:
            logger.debug(f"尝试点击元素：{locator_decs}")
            loc.click()
            logger.debug(f"尝试输入内容：{text}")
            self.page.keyboard.type(text)
            logger.info(f"输入内容成功：{text}")
        except Exception as e:
            logger.error(f"输入内容失败：{text}，错误：{e}")
            raise


    # 双击录入
    def dblclick_and_input_for_canvas(self, canvas_locator, text):
        loc = self.find(canvas_locator[0])
        try:
            logger.debug(f"尝试双击元素：{canvas_locator}")
            loc.dblclick(position = {'x':canvas_locator[1][0],'y':canvas_locator[1][1]})
            logger.debug(f"尝试输入内容：{text}")
            self.page.keyboard.type(text)
            logger.info(f"输入内容成功：{text}")
        except Exception as e:
            logger.error(f"输入内容失败：{text}，错误：{e}")
            raise


    def dblclick_and_type(self, locator_decs, text):
        loc = self.find(locator_decs)
        try:
            logger.debug(f"尝试双击元素：{locator_decs}")
            loc.dblclick()
            logger.debug(f"尝试输入内容：{text}")
            self.page.keyboard.type(text)
            logger.info(f"输入内容成功：{text}")
        except Exception as e:
            logger.error(f"输入内容失败：{text}，错误：{e}")
            raise


    # 输入文件
    def input_file(self, locator_desc, file_path):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试对元素：{locator_desc}上传文件：{file_path}")
            loc.set_input_files(file_path)
            logger.info(f"上传文件成功：{file_path}")
        except Exception as e:
            logger.error(f"上传文件失败：{file_path}，错误：{e}")
            raise


    # 回车
    def enter(self):
        try:
            logger.debug("回车")
            self.page.keyboard.press("Enter")
            logger.info("回车成功")
        except Exception as e:
            logger.error(f"回车失败，错误：{e}")
            raise


    def esc(self):
        try:
            logger.debug("esc")
            self.page.keyboard.press("Escape")
            logger.info("esc成功")
        except Exception as e:
            logger.error(f"esc失败，错误：{e}")
            raise


    def click_slider(self, runway_locator_desc, percent):
        runway = self.find(runway_locator_desc)
        box = runway.bounding_box()
        if not box:
            logger.error("无法获取滑轨的边界信息")
            raise RuntimeError("滑轨不可见或不存在")
        if percent == 100:
            self.page.keyboard.press("End")
        else:
        # 计算点击的绝对坐标：轨道左边缘 + 宽度 * 百分比，垂直居中
            click_x = box['x'] + box['width'] * percent / 100
            click_y = box['y'] + box['height'] / 2
            try:
                logger.debug(f"点击滑轨坐标 ({click_x}, {click_y})，设置百分比 {percent}%")
                self.page.mouse.click(click_x, click_y)
                logger.info(f"已通过点击滑轨设置值为 {percent}%")
            except Exception as e:
                logger.error(f"点击滑轨失败: {e}")
                raise


    def click_js(self, locator_desc):
        loc = self.find(locator_desc)
        try:
            logger.debug(f"尝试通过 JS 点击元素：{locator_desc}")
            self.page.evaluate("el => el.click()", loc.element_handle())
            logger.info(f"JS 点击成功：{locator_desc}")
        except Exception as e:
            logger.error(f"JS 点击失败：{locator_desc}，错误：{e}")
            raise


    def is_visible(self, locator_desc,timeout=10000):
        loc = self.find(locator_desc)
        try:
            boolean = loc.is_visible(timeout=timeout)
            if boolean:
                logger.info(f"检查元素可见：{locator_desc}")
            else:
                logger.error(f"检查元素不可见：{locator_desc}")
            return boolean
        except Exception as e:
            logger.error(f"检查元素可见性异常：{locator_desc}, 错误：{e}")
            return False

    def ensure_dropdown_expanded(self, parent_locator, child_locator):
        """
        确保侧边栏下拉菜单已展开，用于导航前检测。
        先等待父级菜单项可见，再判断子项是否已展示：
        - 子项已可见 → 下拉框已展开，跳过点击父级
        - 子项不可见 → 点击父级展开下拉框
        """
        self.wait_for(parent_locator, "visible")
        if not self.is_visible(child_locator):
            self.click(parent_locator)
            logger.info("下拉框已展开")




