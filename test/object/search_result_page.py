# 搜索相关
from locator.InCMS import InCMSLocator
from locator.search_result import SearchResultLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param

import allure


class SearchResultPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("搜索批号跳转至物质详情页")
    def jump_to_material_view_page(self,batch_number):
        self.click(InCMSLocator.search_button)
        self.fill(InCMSLocator.quick_search_input,batch_number)
        self.click(InCMSLocator.search_window_search_btn)
        # 需要先点击一下聚焦
        self.click_canvas(SearchResultLocator.search_results_first)
        self.click_canvas(SearchResultLocator.search_results_first)
        # frame = self.get_frame(SearchResultLocator.search_result_iframe)
        # frame.click(load_ele_param(SearchResultLocator.registration_code_column,batch_number))