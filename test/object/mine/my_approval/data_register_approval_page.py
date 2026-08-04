import re
from locator.InCMS import InCMSLocator
from locator.mine.my_approval.data_registration_approval import \
    DataRegistrationApprovalLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure


class DataRegisterApprovalPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入我的审核-数据注册审核页")
    def switch_to_data_approval_page(self):
        """导航 我的 → 我的审核 → 数据注册审核"""
        try:
            self.click(InCMSLocator.mine,timeout=1000)
            clickable_result = True
        except Exception as e:
            logger.info(f'当前页面未有导航栏元素显示,不可点击，错误原因{e}')
            clickable_result = False
        if not clickable_result:
            current_url = self.page.url
            #跳转至数据中心
            base_url = re.match(r'(https?://[^/]+)', current_url).group(1)
            self.page.goto(base_url)
            self.click(InCMSLocator.mine)
        self.click(InCMSLocator.my_approval)
        self.click(InCMSLocator.data_register_approval)

    @allure.step("检查审核列表的第x行是否含有字段")
    def check_approval_list(self,row,expected_field):
        try:
            self.wait_for(load_ele_param(DataRegistrationApprovalLocator.table_not_approval_row,row,expected_field),'visible')
        except AssertionError as e:
            logger.error('数据更新审核页，未显示最新的数据')
            raise e

    @allure.step("单行数据注册审批")
    def single_row_approval(self,row,approval_result:bool,reject_reason=None):
        """
        :param row:指定当前页面的第几行的勾选框
        :param approval_result: 审核结果，布尔值，通过与不通过
        :param reject_reason: 数据注册审核拒绝原因
        :return:
        """
        self.click(load_ele_param(DataRegistrationApprovalLocator.table_not_approval_checkbox,row))
        if approval_result:
            self.click(DataRegistrationApprovalLocator.approval_btn)
        else:
            self.click(DataRegistrationApprovalLocator.reject_btn)
            if reject_reason is None:
                self.fill(DataRegistrationApprovalLocator.reject_reason_input,'（默认）拒绝数据注册审核')
            else:
                self.fill(DataRegistrationApprovalLocator.reject_reason_input,reject_reason)
        #二次弹层确认
        self.click(DataRegistrationApprovalLocator.confirm_btn)

