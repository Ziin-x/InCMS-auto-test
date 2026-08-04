import allure

from config.setting import SaveGeneralConfigurationAPI
from locator.InCMS import InCMSLocator
from locator.group_management.sample_management import GeneralConfigurationLocator
from object.basepage import BasePage
from utils.log import logger


class GeneralConfigurationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入通用配置界面")
    def enter_general_configuration(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.sample_management)
        self.click(InCMSLocator.sample_management)
        self.wait_for(GeneralConfigurationLocator.general_config_tab, "visible")

    def _toggle_switch(self, label_locator, switch_locator, switch: bool):
        """通过label的class判断当前开关状态，需要切换时点击switch"""
        label = self.find(label_locator)
        class_attr = label.get_attribute("class") or ""
        is_on = "disabled" not in class_attr
        logger.info(f"开关当前状态: {'开启' if is_on else '关闭'}, 目标状态: {'开启' if switch else '关闭'}")
        if switch == is_on:
            logger.info("开关已是目标状态，跳过操作")
            return
        logger.info("开关状态不一致，执行切换")
        self.wait_according_to_the_interface(
            SaveGeneralConfigurationAPI,
            lambda: self.click(switch_locator)
        )

    @allure.step("自动出库开关控制")
    def auto_outbound_switch(self, switch: bool):
        self._toggle_switch(
            GeneralConfigurationLocator.auto_outbound_label,
            GeneralConfigurationLocator.auto_outbound_switch,
            switch
        )

    @allure.step("自动接收开关控制")
    def auto_receive_switch(self, switch: bool):
        self._toggle_switch(
            GeneralConfigurationLocator.auto_receive_label,
            GeneralConfigurationLocator.auto_receive_switch,
            switch
        )
