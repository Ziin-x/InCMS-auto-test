import allure

from config.setting import CompletePickUpAPI, CompleteOutboundAPI
from locator.InCMS import InCMSLocator
from locator.sample_center.outbound import OutboundLocator
from object.basepage import BasePage
from object.sample_center.request_record import RequestRecordPage
from utils.log import logger


class OutboundPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入出库界面")
    def enter_outbound(self):
        self.ensure_dropdown_expanded(InCMSLocator.sample_center, InCMSLocator.outbound)
        self.click(InCMSLocator.outbound)
        self.wait_for(OutboundLocator.assert_outbound, "visible")
        logger.info("已成功进入出库界面")

    # 该方法与申领记录界面通用，内部复用 RequestRecordPage.switch_view，同时有等待作用
    @allure.step("切换界面视图")
    def switch_view(self, view_name: str):
        """切换到指定视图并效验切换成功，复用申领记录界面的通用实现"""
        RequestRecordPage(self.page).switch_view(view_name)

    @allure.step("拣货所有待拣货样品")
    def pick_all_pending_samples(self):
        # 两次点击。第一次聚焦
        self.click_canvas(OutboundLocator.select_all_sample)
        self.page.wait_for_timeout(1000)
        self.click(OutboundLocator.pick_up)
        self.click_canvas(OutboundLocator.select_all_pick_up_order)
        self.click(OutboundLocator.complete_pick_up)
        self.wait_according_to_the_interface(
            CompletePickUpAPI,
            lambda: self.click(OutboundLocator.confirm)
        )
        logger.info("已拣货所有待拣货样品")

    @allure.step("出库所有待出库样品")
    def outbound_all_pending_samples(self):
        self.click_canvas_first(OutboundLocator.select_all_sample)
        self.click(OutboundLocator.outbound)
        self.wait_according_to_the_interface(
            CompleteOutboundAPI,
            lambda: self.click(OutboundLocator.confirm)
        )
        logger.info("已出库所有待出库样品")

    def click_canvas_first(self, canvas_locator, force=False):
        """点击匹配到的第一个canvas元素的相对位置"""
        loc = self.find(canvas_locator[0]).first
        try:
            logger.debug(f"尝试点击元素：{canvas_locator}")
            loc.click(position={'x': canvas_locator[1][0], 'y': canvas_locator[1][1]}, force=force)
            logger.info(f"点击元素成功：{canvas_locator}")
        except Exception as e:
            logger.error(f"点击元素失败：{canvas_locator}，错误：{e}")
            raise


