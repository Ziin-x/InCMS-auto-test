import re
from io import BytesIO

from locator.data_up.data_up import DataUpLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure
import openpyxl


class DataUpPage(BasePage):
    """数据更新页"""

    def __init__(self, page):
        super().__init__(page)

    @allure.step("跳转至数据更新页")
    def switch_to_data_up_page(self, tab_name: str = ""):
        """
        导航至数据更新页，可指定tab
        :param tab_name: tab名称（该页有三个tab），为空则不切换
        """
        try:
            self.click(InCMSLocator.data_up, timeout=1000)
            clickable_result = True
        except Exception as e:
            logger.info(f"当前页面未有导航栏元素显示，不可点击，错误原因：{e}")
            clickable_result = False
        if not clickable_result:
            current_url = self.page.url
            base_url = re.match(r'(https?://[^/]+)', current_url).group(1)
            self.page.goto(base_url)
            self.click(InCMSLocator.data_up)
        # 切换tab
        if tab_name:
            self.switch_tab(tab_name)

    @allure.step("切换tab")
    def switch_tab(self, tab_name: str):
        """切换到指定tab"""
        logger.info(f"切换tab：{tab_name}")
        if not self.is_visible(load_ele_param(DataUpLocator.active_tab_with_text,tab_name)):
            self.click(load_ele_param(DataUpLocator.switch_tab, tab_name))
            logger.info(f"切换tab成功：{tab_name}")

    # ---------- 批量更新 ----------

    class BatchUpdate(BasePage):
        """批量数据更新"""

        def __init__(self, page):
            super().__init__(page)

        _INNER_PAGE_MAP = {
            "按模板导入": DataUpLocator.template_import_btn,
            "自定义导入": DataUpLocator.custom_import_btn,
        }

        @allure.step("切换到{page_name}页面")
        def switch_inner_page(self, page_name: str):
            """
            切换内部分页，如果已在目标页面则跳过
            :param page_name: 页面名称（按模板导入 / 自定义导入）
            """
            logger.debug(f"切换到{page_name}页面")
            target_loc = self._INNER_PAGE_MAP.get(page_name)
            if target_loc is None:
                raise ValueError(f"未知的内部分页: {page_name}")
            loc = self.find(target_loc)
            class_attr = loc.get_attribute("class")
            if class_attr and "active" in class_attr.split():
                logger.info(f"已在{page_name}页面")
                return
            logger.debug(f"当前不在{page_name}页面，点击切换")
            self.click(target_loc)
            self.page.wait_for_timeout(3000)
            if not loc.evaluate("el => el.classList.contains('active')"):
                logger.error(f"切换到{page_name}页面失败")
                raise RuntimeError(f"切换到{page_name}页面失败")
            logger.info(f"已切换到{page_name}页面")


        @allure.step("下载批量更新模板")
        def download_batch_update_template(self):
            """在按模板导入页下载批量更新模板，返回 openpyxl Workbook"""
            logger.debug("开始下载批量更新模板")
            with self.page.expect_download() as download_info:
                self.click(DataUpLocator.download_batch_update_template_btn)
            download = download_info.value
            logger.debug(f"模板文件名: {download.suggested_filename}")
            data = download.path().read_bytes()
            logger.debug(f"模板文件大小: {len(data)} bytes")
            assert len(data) > 0, "批量更新模板文件为空"
            wb = openpyxl.load_workbook(BytesIO(data))
            logger.info(f"批量更新模板下载成功，共 {len(wb.sheetnames)} 个 sheet")
            return wb

        # compare_template_to_expected 已提取至 CommonPage
