import allure

from config.setting import ReturnSampleAPI, RequestReceiveAPI
from locator.sample_center.request_record import RequestRecordLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from object.common import CommonPage
from utils.load_ele_param import load_ele_param
from utils.log import logger


class RequestRecordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入申领记录界面")
    def enter_request_record(self):
        self.ensure_dropdown_expanded(InCMSLocator.sample_center, RequestRecordLocator.request_record_nav)
        self.click(RequestRecordLocator.request_record_nav)
        self.wait_for(RequestRecordLocator.assert_request_record, "visible")
        logger.info("已成功进入申领记录界面")

    # 该方法与出库界面通用
    @allure.step("切换界面视图")
    def switch_view(self, view_name: str):
        """切换到指定视图并效验切换成功，已接收视图默认按申领时间倒序"""
        view_btn = load_ele_param(RequestRecordLocator.view_btn, view_name)
        view_btn_active = load_ele_param(RequestRecordLocator.view_btn_active, view_name)
        self.click(view_btn)
        self.wait_for(view_btn_active, "visible")
        if view_name == "已接收":
            CommonPage.sort_by_request_time_desc(self)
        logger.info(f"已成功进入{view_name}界面")

    @allure.step("归还申领的物品")
    def return_sample(self):
        # 双击，第一次模拟悬停
        self.click_canvas(RequestRecordLocator.check_first_received)
        self.click_canvas(RequestRecordLocator.check_first_received)
        self.click(RequestRecordLocator.return_btn)
        self.click_canvas(RequestRecordLocator.check_all_return)
        self.wait_according_to_the_interface(
            ReturnSampleAPI,
            lambda: self.click(RequestRecordLocator.confirm_btn)
        )
        logger.info("样品归还请求发送完成")

    @allure.step("接收申领的物品")
    def receive_sample(self):
        self.click_canvas(RequestRecordLocator.check_all_request)
        self.click(RequestRecordLocator.receive_btn)
        self.wait_according_to_the_interface(
            RequestReceiveAPI,
            lambda: self.click(RequestRecordLocator.confirm_btn)
        )
        logger.info("样品接收完成")

    @allure.step("为申领物品分配任务")
    def assign_task(self, member: str):
        """选中物品并分配给指定成员"""
        self.click_canvas(RequestRecordLocator.check_first_received)
        self.click(RequestRecordLocator.assign_btn)
        self.click(RequestRecordLocator.select_member)
        member_loc = load_ele_param(RequestRecordLocator.member_option, member)
        self.click(member_loc)
        self.click(RequestRecordLocator.confirm_btn)
        logger.info(f"已为申领物品分配任务给: {member}")

