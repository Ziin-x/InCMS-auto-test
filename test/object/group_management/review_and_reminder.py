from locator.group_management.review_and_reminder import \
    ReviewAndReminderLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from typing import Literal

import allure

from utils.log import logger


#审核与提醒页
class ReviewAndReminderPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def enter_review_and_reminder_page(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.review_and_reminder)
        self.click(InCMSLocator.review_and_reminder)

    @allure.step("进入对应的审核设置页面")
    def enter_review_page(self, review_type=None):
        self.enter_review_and_reminder_page()
        if review_type == "注册审核" or review_type is None:
            review_assert_loc = load_ele_param(ReviewAndReminderLocator.registration_review, "注册审核")
        else:
            review_loc = load_ele_param(ReviewAndReminderLocator.registration_review, review_type)
            self.click(review_loc)
            review_assert_loc = load_ele_param(ReviewAndReminderLocator.assert_registration_review, review_type)
        self.wait_for(review_assert_loc, 'visible')

    @allure.step("选择项目")
    def select_project(self, project: str):
        self.click(ReviewAndReminderLocator.select_project)
        self.fill(ReviewAndReminderLocator.search_box,project)
        project_loc = load_ele_param(ReviewAndReminderLocator.project_option, project)
        self.click(project_loc)

    @allure.step("选择审核人")
    def select_reviewer(self, reviewer: str = None):
        self.click(ReviewAndReminderLocator.select_reviewer)
        self.page.wait_for_timeout(1000)
        if reviewer is not None:
            self.fill(ReviewAndReminderLocator.search_box, reviewer)
            reviewer_loc = load_ele_param(ReviewAndReminderLocator.reviewer_option_no_user, reviewer)
            self.click_nth(reviewer_loc, 0)
            self.click(ReviewAndReminderLocator.select_reviewer)
        else:
            # 取消勾选：遍历点击所有已选中的审核人选项
            count = self.find(ReviewAndReminderLocator.any_selected_option).count()
            logger.info(count)
            self.click(ReviewAndReminderLocator.select_reviewer)
            for i in range(count):
                self.click(ReviewAndReminderLocator.select_reviewer)
                self.page.wait_for_timeout(500)
                self.click_nth(ReviewAndReminderLocator.any_selected_option, 0)
                self.click(ReviewAndReminderLocator.select_reviewer)
        self.page.wait_for_timeout(1000)

    @allure.step("保存审核设置")
    def save_review_setting(self):
        self.click(ReviewAndReminderLocator.save)

    def _ensure_approval_tab(self, approval_type):
        """确保当前在正确的审核类型tab下"""
        current_url = self.page.url
        if 'approval-and-remind' not in current_url:
            self.enter_review_page(approval_type)
        else:
            active_tab = self.get_text(ReviewAndReminderLocator.current_active_tab)
            if active_tab != approval_type:
                self.click(load_ele_param(ReviewAndReminderLocator.registration_review, approval_type))
                self.wait_for(load_ele_param(ReviewAndReminderLocator.assert_registration_review, approval_type), 'visible')

    @allure.step("设置项目审核人")
    def set_approval_user(self, project, approval_user, approval_type: Literal[
        "注册审核", "数据更新审核", "样品登记审核", "样品申领审核", "样品报废审核", "样品接收审核", "样品归还审核"
    ]):
        self._ensure_approval_tab(approval_type)
        self.select_project(project)
        self.select_reviewer(reviewer = None)
        self.select_reviewer(approval_user)
        self.click(ReviewAndReminderLocator.save)
        self.wait_for(ReviewAndReminderLocator.save_success_toast, 'visible',timeout=60000)

    @allure.step("清空项目审核设置")
    def clear_approval_setting(self,project,approval_type: Literal[
        "注册审核", "数据更新审核", "样品登记审核", "样品申领审核", "样品报废审核", "样品接收审核", "样品归还审核"
    ]):
        self.set_approval_user(project, None, approval_type)

