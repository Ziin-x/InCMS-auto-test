import re
import traceback
from data.pydantic.plug_pydantic import product
from locator.fixture_loactor.plug_page_locator import PlugPageLocator
from object.basepage import BasePage

import allure
import pytest

from utils.load_ele_param import load_ele_param


class PlugPageObject(BasePage):

    def __init__(self, page):
        super().__init__(page)

    @allure.step("plug选择平台进入平台页面")
    def choose_product(self,product_data:product):
        try:
            if product_data == None:
                pytest.exit(f'页面不存在, 停止测试执行', returncode=1)
            for name in product_data.name:
                product_locator = load_ele_param(PlugPageLocator.general_product, product_data.locator_and_url)
                if self.is_visible(product_locator, name):
                    with self.page.expect_popup() as popup_info:
                        self.click(product_locator)
                    new_page = popup_info.value
                    new_page.wait_for_load_state('networkidle')
                    self.page = new_page
                    self.wait_for_url(re.compile(product_data.locator_and_url), timeout=5000)
                    break
            return self.page
        except Exception as e:
            traceback.print_exc()
            pytest.exit(f'plug进入{product_data.locator_and_url}失败, 停止测试执行', returncode=1)

