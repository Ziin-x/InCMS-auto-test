import allure

from config.setting import DeleteSampleCartItemAPI
from locator.InCMS import InCMSLocator
from locator.sample_center.sample_cart import SampleCartLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger


class SampleCartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入领样车界面")
    def enter_sample_cart(self):
        self.ensure_dropdown_expanded(InCMSLocator.sample_center, InCMSLocator.sample_cart)
        self.click(InCMSLocator.sample_cart)
        self.wait_for(SampleCartLocator.assert_sample_cart, "visible")
        logger.info("已成功进入领样车界面")

    @allure.step("切换到按量界面")
    def switch_to_quantity_tab(self):
        """点击按量tab并等待is-active出现，完成切换"""
        self.click(SampleCartLocator.quantity_tab)
        self.wait_for(SampleCartLocator.quantity_tab_active, "visible")
        logger.info("已成功切换到按量界面")

    @allure.step("删除所有领样车样品")
    def delete_all_sample(self):
        """删除所有领样车样品"""
        self.click(SampleCartLocator.check_all_sample)
        if self.is_visible(SampleCartLocator.delete_btn):
            self.wait_according_to_the_interface(
                DeleteSampleCartItemAPI,
                lambda: self.click(SampleCartLocator.delete_btn)
            )
        logger.info("领样车中已经没有样品")

    def _click_canvas_and_input(self, canvas_locator, value: str):
        """点击canvas激活输入框并填入值"""
        self.click_canvas(canvas_locator)
        self.page.keyboard.type(value)
        logger.info(f"已填入申领量: {value}")

    @allure.step("为第一个样品填入申领的量")
    def check_and_fill_claim_amount(self, claim_amount: str):
        """选中第一个样品，并为其填入申领的量"""
        self._click_canvas_and_input(SampleCartLocator.claim_amount, claim_amount)
        logger.info("已为第一个样品填写申领量")
        self.click(SampleCartLocator.claim_amount_unit)
        self.click(SampleCartLocator.claim_amount_unit_volume)
        self.click(SampleCartLocator.claim_amount_unit_volume_μg)

    @allure.step("选中第一个样品申领")
    def check_and_claim_sample(self):
        """选中第一个样品，并填写申领的量"""
        self.click_canvas(SampleCartLocator.check_newest_sample)
        self.click(SampleCartLocator.claim_now)

    @allure.step("选择接收人")
    def choose_receiver(self, receiver: str):
        """选择接收人"""
        self.click(SampleCartLocator.receiver_btn)
        receiver_loc = load_ele_param(SampleCartLocator.receiver_option, receiver)
        self.page.wait_for_timeout(3000)
        if self.is_visible(receiver_loc):
            self.click(receiver_loc)
            logger.info(f"已选择接收人: {receiver}")
        else:
            logger.error(f"接收人 [{receiver}] 在列表中不可见")
            raise RuntimeError(f"接收人 [{receiver}] 在列表中不可见，无法选择")



