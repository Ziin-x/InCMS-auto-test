import re
from config.setting import (AutoBatchMemberSaveAPI, NumberRuleSaveAPI,
                                 SampleIDSaveAPI)
from data.pydantic.data_center.single_register import SingleRegisterData
from data.pydantic.group_management.code_rules import CodeRulesData
from data.pydantic.group_management.template_management import \
    TemplateManagementData
from data.pydantic.sample_center.sample_list import SampleListData
from object.group_management.code_rules import (BatchNumberPage,
                                                     CodeRolesPage,
                                                     RegistrationCodeRulesPage,
                                                     SampleIDPage)
from utils.log import logger  # 新增导入

import allure
import pytest


@allure.epic("群内管理")
@allure.feature("编号规则")
class TestCodeRules:
    @pytest.fixture(scope="function")
    def load_code_rules_page(self, InCMS_page):
        code_rules_page = CodeRolesPage(InCMS_page)
        code_rules_page.enter_code_rules()
        code_rules_page.wait_for_url(re.compile("code-rule"), timeout=10000)
        return code_rules_page.page

    @allure.story("注册编号")
    class TestRegistrationCode:
        code_rules_data = CodeRulesData.get_data()
        add_module_list = SingleRegisterData.get_data().add_module_list
        parameter_name = TemplateManagementData.get_data().parameter.parameter_name
        register_amount = SingleRegisterData.get_data().register_amount
        batch_number = SingleRegisterData.get_data().batch_number
        current_amount = SampleListData.get_data().current_amount

        @allure.title("设置注册编号自动生成规则")
        @pytest.mark.order(17)
        def test_code_rule01(self, load_code_rules_page, request: pytest.FixtureRequest):
            logger.info("==================== test_code_rule01 started ====================")
            registration_code_rules_page = RegistrationCodeRulesPage(load_code_rules_page)
            registration_code_rules_page.code_rules_page.code_rules_custom_character(self.code_rules_data.code_rule_custom)
            registration_code_rules_page.register_code_rules(self.code_rules_data.code_rule_prefix)
            registration_code_rules_page.code_rules_page.interval_symbol()
            # 记录注册编号预览，以便断言
            code_preview_text = registration_code_rules_page.code_rules_page.get_preview()
            request.config.cache.set("code_preview_text", code_preview_text)
            registration_code_rules_page.serial_number_rules()
            registration_code_rules_page.wait_according_to_the_interface(
                NumberRuleSaveAPI,
                registration_code_rules_page.code_rules_page.save
            )
            logger.info("==================== test_code_rule01 over =======================")

        @allure.title("设置批号自动生成规则")
        @pytest.mark.order(18)
        def test_code_rule02(self, load_code_rules_page, request: pytest.FixtureRequest):
            logger.info("==================== test_code_rule02 started ====================")
            batch_code_page = BatchNumberPage(load_code_rules_page)
            batch_code_page.enter_batch_number()
            batch_code_page.batch_number_enable()
            batch_code_page.code_rules_page.code_rules_custom_character(self.code_rules_data.code_rule_custom)
            batch_code_page.code_rules_build_data()
            batch_code_page.code_rules_page.interval_symbol()
            # 记录自动生成批号预览，以便断言
            batch_preview_text = batch_code_page.code_rules_page.get_preview()
            request.config.cache.set("batch_preview_text", batch_preview_text)
            batch_code_page.wait_according_to_the_interface(
                AutoBatchMemberSaveAPI,
                batch_code_page.code_rules_page.save
            )
            logger.info("==================== test_code_rule02 over =======================")

        @allure.title("设置样品ID自动生成规则")
        @pytest.mark.order(19)
        def test_code_rules03(self, load_code_rules_page, request: pytest.FixtureRequest):
            logger.info("==================== test_code_rules03 started ====================")
            sample_id_page = SampleIDPage(load_code_rules_page)
            sample_id_page.enter_sample_id()
            sample_id_page.code_rules_page.code_rules_custom_character(self.code_rules_data.code_rule_custom)
            sample_id_page.code_rules_page.interval_symbol()
            id_preview_text = sample_id_page.code_rules_page.get_preview()
            request.config.cache.set("id_preview_text", id_preview_text)
            sample_id_page.wait_according_to_the_interface(
                SampleIDSaveAPI,
                sample_id_page.code_rules_page.save
            )
            logger.info("==================== test_code_rules03 over =======================")