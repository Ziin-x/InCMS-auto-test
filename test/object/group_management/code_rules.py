from locator.group_management.code_rules import CodeRulesLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.log import logger

import allure


class CodeRolesPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("进入编号规则界面")
    def enter_code_rules(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.code_rules)
        self.click(InCMSLocator.code_rules)

    @allure.step("设置间隔符号")
    def interval_symbol(self):
        self.click(CodeRulesLocator.interval_symbol_selection)
        self.click(CodeRulesLocator.interval_symbol_line)

    @allure.step("获取预览")
    def get_preview(self):
        value = self.get_text(CodeRulesLocator.preview)
        preview_text = value.split(":",1)[-1].strip()
        logger.info(f"获取的预览文本为：{preview_text}")
        return preview_text

    @allure.step("设置批量编号规则，自定义字符")
    def code_rules_custom_character(self, code_rule_custom):
        if not self.is_visible(CodeRulesLocator.custom_character):
            self.click(CodeRulesLocator.add_field)
            self.click(CodeRulesLocator.custom_character_option)
        self.fill(CodeRulesLocator.custom_character, code_rule_custom)

    @allure.step("保存")
    def save(self):
        self.click(CodeRulesLocator.save)

class RegistrationCodeRulesPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.code_rules_page = CodeRolesPage(page)

    @allure.step("设置注册编号规则，前缀")
    def register_code_rules(self,code_rule_prefix):
        self.fill(CodeRulesLocator.code_rule_prefix, code_rule_prefix)

    @allure.step("设置流水号规则")
    def serial_number_rules(self):
        self.click(CodeRulesLocator.orderly_running_water_number)
        self.click(CodeRulesLocator.serial_number_increases_simultaneously)


class BatchNumberPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.code_rules_page = CodeRolesPage(page)

    @allure.step("进入批号界面")
    def enter_batch_number(self):
        self.click(CodeRulesLocator.batch_number_page)
        try:
            logger.debug("断言是否进入批号界面")
            self.wait_for(CodeRulesLocator.batch_number_page_assert,"visible")
            logger.info("进入批号界面成功")
        except Exception as e:
            logger.error(f"进入批号界面失败，错误：{e}")
            raise

    @allure.step("开启自动生成批号")
    def batch_number_enable(self):
        if not self.is_visible(CodeRulesLocator.auto_generate_batch_number_opened):
            self.click(CodeRulesLocator.auto_generate_batch_number_closed)

    @allure.step("设置批量编号规则，创建日期")
    def code_rules_build_data(self):
        if not self.is_visible(CodeRulesLocator.build_date):
            self.click(CodeRulesLocator.add_field)
            self.click(CodeRulesLocator.build_date_option)


class SampleIDPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.code_rules_page = CodeRolesPage(page)

    @allure.step("进入样品ID界面")
    def enter_sample_id(self):
        self.click(CodeRulesLocator.sample_id_page)
        try:
            logger.debug("断言是否进入样品ID界面")
            self.wait_for(CodeRulesLocator.sample_id_page_assert,"visible")
            logger.info("进入样品ID界面成功")
        except Exception as e:
            logger.error(f"进入样品ID界面失败，错误：{e}")
            raise





