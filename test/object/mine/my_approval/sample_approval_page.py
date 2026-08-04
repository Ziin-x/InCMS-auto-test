import re

from config.setting import RejectSampleApprovalAPI, ApprovalSampleApprovalAPI
from locator.InCMS import InCMSLocator
from locator.mine.my_approval.sample_approval import \
    SampleApprovalLocator
from object.basepage import BasePage
from utils.log import logger

import allure


class SampleApprovalPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入我的审核-样品相关审核页")
    def switch_to_sample_approval_page(self):
        """导航 我的 → 我的审核 → 样品相关审核"""
        try:
            self.click(InCMSLocator.mine, timeout=1000)
            clickable_result = True
        except Exception as e:
            logger.info(f'当前页面未有导航栏元素显示,不可点击，错误原因{e}')
            clickable_result = False
        if not clickable_result:
            current_url = self.page.url
            base_url = re.match(r'(https?://[^/]+)', current_url).group(1)
            self.page.goto(base_url)
            self.click(InCMSLocator.mine)
        self.click(InCMSLocator.my_approval)
        self.click(InCMSLocator.sample_approval)

    @allure.step("样品审批")
    def sample_approval(self, is_approval: bool, reject_reason: str = None):
        """点击全选后审批"""
        self.click_canvas(SampleApprovalLocator.check_all)
        if is_approval:
            self.click(SampleApprovalLocator.approval_btn)
            self.wait_according_to_the_interface(
                ApprovalSampleApprovalAPI,
                lambda: self.click(SampleApprovalLocator.confirm_btn)
            )
        else:
            self.click(SampleApprovalLocator.reject_btn)
            if reject_reason is None:
                self.fill(SampleApprovalLocator.reject_reason_input, '（默认）拒绝样品登记审核')
            else:
                self.fill(SampleApprovalLocator.reject_reason_input, reject_reason)
            self.wait_according_to_the_interface(
                RejectSampleApprovalAPI,
                lambda: self.click(SampleApprovalLocator.confirm_btn)
            )


