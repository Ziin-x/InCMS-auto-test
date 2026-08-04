from locator.data_center.single_register import SingleRegisterLocator
from locator.eln.eln import ELNLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure


class ELNPage(BasePage):
    """ELN 页面"""

    def __init__(self, page):
        super().__init__(page)

    @allure.step("新建ELN记录")
    def create_record(self, notebook_name, group_name, project_name):
        """
        新建 ELN 记录
        :param notebook_name: 记录本名称
        :param group_name: 鹰群名称
        :param project_name: 所属项目名称
        """
        logger.debug("开始新建ELN记录")
        self.click(ELNLocator.create_record_btn)
        self.page.wait_for_timeout(1000)
        logger.debug("已打开新建记录弹窗")

        # 选择记录本，如果没有就新建
        self._select_or_create_notebook(notebook_name, group_name, project_name)
        # 选择空白模板
        self.click(ELNLocator.template_select)
        self.click(ELNLocator.blank_template_option)
        logger.debug("已选择空白模板")
        # 点击确定
        self.click(ELNLocator.confirm_btn)
        logger.info("新建ELN记录完成")

    def _select_or_create_notebook(self, notebook_name, group_name, project_name):
        # 点击记录本选择框，输入名称过滤，检查是否存在记录本
        self.click(ELNLocator.notebook_select)
        self.page.wait_for_timeout(300)
        self.fill(ELNLocator.notebook_select, notebook_name)
        self.page.wait_for_timeout(500)

        notebook_option = load_ele_param(ELNLocator.notebook_option, notebook_name)
        if self.is_visible(notebook_option):
            self.click(notebook_option)
            logger.info(f"已选择记录本: {notebook_name}")
            return

        # 记录本不存在，点击新建
        logger.debug("记录本不存在，点击新建记录本")
        self.click(ELNLocator.create_notebook_link)
        self.page.wait_for_timeout(500)

        # 在新建记录本弹窗中：鹰群 → 记录本名称 → 所属项目 → 确定
        logger.debug(f"选择鹰群: {group_name}")
        self.click(ELNLocator.group_select)
        self.click(load_ele_param(ELNLocator.group_option, group_name))

        logger.debug(f"填写记录本名称: {notebook_name}")
        self.fill(ELNLocator.form_item_input, notebook_name)

        logger.debug(f"选择所属项目: {project_name}")
        self.click(ELNLocator.project_select)
        self.click(load_ele_param(ELNLocator.project_tree_option, project_name))

        # 两个弹窗叠在一起，取最后一个（新建记录本弹窗在上面）
        self.click_nth(ELNLocator.confirm_btn, -1)
        logger.info("新建记录本完成")

    @allure.step("添加InDraw模块")
    def add_indraw_module(self):
        logger.debug("添加 InDraw 模块")
        self.click(ELNLocator.add_module_btn)
        self.click(ELNLocator.indraw_module)
        self.click(ELNLocator.panel_close_btn)
        logger.info("已添加 InDraw 模块")

    @allure.step("添加产物")
    def add_product(self, product_name="苯"):
        """搜索并添加产物，默认添加苯"""
        logger.debug(f"添加产物: {product_name}")
        self.click(ELNLocator.add_product_btn)
        self.page.wait_for_timeout(500)
        self.fill(ELNLocator.product_search_input, product_name)
        self.page.wait_for_timeout(1000)
        self.click_nth(ELNLocator.product_suggestion, 0)
        self.click(ELNLocator.confirm_btn)
        logger.info(f"已添加产物: {product_name}")

    @allure.step("注册产物到CMS")
    def register_to_cms(self, group_name):
        """点击产物 → 注册到CMS → 选择鹰群 → 确定 → 切换CMS页面 → 确定"""
        logger.debug("点击产物P1")
        self.click(ELNLocator.product_badge)
        logger.debug("点击注册到CMS")
        self.click(ELNLocator.register_to_cms_btn)

        logger.debug(f"选择鹰群: {group_name}")
        self.click(ELNLocator.group_select)
        self.click(load_ele_param(ELNLocator.group_option, group_name))

        logger.debug("点击确认")
        with self.page.expect_popup() as popup_info:
            self.click(ELNLocator.Confirm_btn)
        self.page = popup_info.value
        self.page.wait_for_load_state('networkidle')
        logger.info(f"CMS页面已打开: {self.page.url}")

        # 在CMS页面点击确定
        self.click(ELNLocator.confirm_btn)
        logger.info("注册到CMS完成")
