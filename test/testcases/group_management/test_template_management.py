import re

import allure
import pytest

from config.setting import ProjectCreateAPI, TemplateCreateAPI
from data.pydantic.group_management.template_management import TemplateManagementData
from locator.group_management.template_management import TemplateManagementLocator
from object.data_center.data_center import DataCenterPage
from object.data_center.single_register import SingleRegisterPage
from object.group_management.template_management import (
    ProjectAndTemplatePage, RegistrationTemplatePage, TemplateManagementPage
)
from utils.log import logger


@allure.epic("群内管理")
@allure.feature("模板管理")
class TestTemplateManagement:
    @pytest.fixture(scope="function")
    def load_registration_template_page(self, InCMS_page):
        template_management_page = TemplateManagementPage(InCMS_page)
        template_management_page.enter_template_management()
        # 效验是否进入注册模版界面
        template_management_page.wait_for_url(re.compile("template-manage"), timeout=10000)
        return template_management_page.page

    @pytest.fixture(scope="function")
    def load_project_and_template_page(self, InCMS_page):
        template_management_page = TemplateManagementPage(InCMS_page)
        template_management_page.enter_project_and_template()
        # 效验是否进入项目和模版界面
        template_management_page.wait_for_url(re.compile("template-manage"), timeout=10000)
        template_management_page.wait_for(TemplateManagementLocator.project_and_template_assert, state="visible")
        return template_management_page.page

    @allure.story("注册模版")
    class TestRegistrationTemplate:
        _data = TemplateManagementData.get_data()
        template_name_data = _data.templateName
        field_name = _data.fieldName
        parameter_name = _data.parameter.parameter_name
        tip_message = _data.parameter.tip_message
        parameter_option = _data.parameter.parameter_option

        @allure.title("新建【化合物/序列】注册模板验证")
        @pytest.mark.order(1)
        def test_template_manage01(self, load_registration_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage01 started ====================")
            registration_template_page = RegistrationTemplatePage(load_registration_template_page)
            registration_template_page.enter_new_interface('化合物/序列')
            registration_template_page.page.wait_for_load_state('networkidle')
            registration_template_page.add_all_module()
            registration_template_page.rename_template(self.template_name_data.compound_sequence_name)
            registration_template_page.add_custom_parameter(
                "基本信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "物化信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "体外活性",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "自定义表格",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.wait_according_to_the_interface(TemplateCreateAPI, registration_template_page.save_template)
            # 断言
            registration_template_page.assert_template(self.template_name_data.compound_sequence_name)
            request.config.cache.set("compound_sequence_template_name", self.template_name_data.compound_sequence_name)
            logger.info("==================== test_template_manage01 over =======================")

        @allure.title("新建【混合物/配方】注册模板验证")
        @pytest.mark.order(2)
        def test_template_manage02(self, load_registration_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage02 started ====================")
            registration_template_page = RegistrationTemplatePage(load_registration_template_page)
            registration_template_page.enter_new_interface('混合物/配方')
            registration_template_page.page.wait_for_load_state('networkidle')
            registration_template_page.add_custom_field(self.field_name)
            registration_template_page.add_all_module()
            registration_template_page.rename_template(self.template_name_data.mixture_formula_name)
            registration_template_page.add_custom_parameter(
                "基本信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "物化信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "自定义表格",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.wait_according_to_the_interface(TemplateCreateAPI, registration_template_page.save_template)
            # 断言
            registration_template_page.assert_template(self.template_name_data.mixture_formula_name)
            request.config.cache.set("mixture_formula_template_name", self.template_name_data.mixture_formula_name)
            logger.info("==================== test_template_manage02 over =======================")

        @allure.title("新建【自定义物质】注册模板验证")
        @pytest.mark.order(3)
        def test_template_manage03(self, load_registration_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage03 started ====================")
            registration_template_page = RegistrationTemplatePage(load_registration_template_page)
            registration_template_page.enter_new_interface('自定义物质')
            registration_template_page.page.wait_for_load_state('networkidle')
            registration_template_page.add_custom_field(self.field_name)
            registration_template_page.add_all_module()
            registration_template_page.rename_template(self.template_name_data.custom_compound_name)
            registration_template_page.add_custom_parameter(
                "基本信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "物化信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "自定义表格",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.wait_according_to_the_interface(TemplateCreateAPI, registration_template_page.save_template)
            # 断言
            registration_template_page.assert_template(self.template_name_data.custom_compound_name)
            request.config.cache.set("custom_compound_template_name", self.template_name_data.custom_compound_name)
            logger.info("==================== test_template_manage03 over =======================")

        @allure.title("新建【DNA】注册模板验证")
        @pytest.mark.order(4)
        def test_template_manage04(self, load_registration_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage04 started ====================")
            registration_template_page = RegistrationTemplatePage(load_registration_template_page)
            registration_template_page.enter_new_interface('DNA')
            registration_template_page.page.wait_for_load_state('networkidle')
            registration_template_page.add_all_module()
            registration_template_page.rename_template(self.template_name_data.DNA_name)
            registration_template_page.add_custom_parameter(
                "基本信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "物化信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "自定义表格",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.wait_according_to_the_interface(TemplateCreateAPI, registration_template_page.save_template)
            # 断言
            registration_template_page.assert_template(self.template_name_data.DNA_name)
            request.config.cache.set("DNA_template_name", self.template_name_data.DNA_name)
            logger.info("==================== test_template_manage04 over =======================")

        @allure.title("新建【RNA】注册模板验证")
        @pytest.mark.order(5)
        def test_template_manage05(self, load_registration_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage05 started ====================")
            registration_template_page = RegistrationTemplatePage(load_registration_template_page)
            registration_template_page.enter_new_interface('RNA')
            registration_template_page.page.wait_for_load_state('networkidle')
            registration_template_page.add_all_module()
            registration_template_page.rename_template(self.template_name_data.RNA_name)
            registration_template_page.add_custom_parameter(
                "基本信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "物化信息",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.add_custom_parameter(
                "自定义表格",
                self.parameter_name,
                self.tip_message,
                self.parameter_option
            )
            registration_template_page.page.wait_for_timeout(1000)
            registration_template_page.wait_according_to_the_interface(TemplateCreateAPI, registration_template_page.save_template)
            # 断言
            registration_template_page.assert_template(self.template_name_data.RNA_name)
            request.config.cache.set("RNA_template_name", self.template_name_data.RNA_name)
            logger.info("==================== test_template_manage05 over =======================")

    @allure.story("项目与模板")
    class TestProjectAndTemplate:
        _data = TemplateManagementData.get_data()
        project_data = _data.project
        project_name = _data.project.projectName
        project_code = _data.project.projectCode

        @allure.title("新建项目并关联【化合物/序列】模板")
        @pytest.mark.order(6)
        def test_template_manage06(self, load_project_and_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage06 started ====================")
            project_and_template_page = ProjectAndTemplatePage(load_project_and_template_page)
            # 创建项目，并将new_project方法传入接口等待方法作为action，等待接口返回200后继续下一步
            project_and_template_page.wait_according_to_the_interface(
                ProjectCreateAPI,
                lambda: project_and_template_page.new_project(
                    self.project_name.compound_sequence_name,
                    self.project_code.compound_sequence_code,
                    self.project_data.start_time,
                    self.project_data.end_time
                )
            )
            # 产品特性，数据同步需要较长时间
            project_and_template_page.page.wait_for_timeout(60000)
            # 先断言在项目与模版页面是否出现创建的新项目
            project_and_template_page.reload()
            project_and_template_page.assert_project(self.project_name.compound_sequence_name)
            project_and_template_page.add_related_template(
                self.project_name.compound_sequence_name,
                logger.info(f"cache.get('compound_sequence_template_name') 已调用")
                request.config.cache.get("compound_sequence_template_name", None)
            )
            project_id = project_and_template_page.get_project_id(self.project_name.compound_sequence_name)
            # 调用api调节项目状态
            project_and_template_page.project_apply(
                self.project_name.compound_sequence_name,
                self.project_code.compound_sequence_code,
                project_id
            )
            project_and_template_page.project_start(
                self.project_name.compound_sequence_name,
                self.project_code.compound_sequence_code,
                project_id
            )
            # 产品特性，数据同步需要较长时间
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            data_center_page = DataCenterPage(load_project_and_template_page)
            data_center_page.assert_project_visible(self.project_name.compound_sequence_name)
            single_register_page = SingleRegisterPage(load_project_and_template_page)
            single_register_page.assert_project_visible(self.project_name.compound_sequence_name)
            request.config.cache.set("compound_sequence_project_name", self.project_name.compound_sequence_name)
            request.config.cache.set("compound_sequence_project_code", self.project_code.compound_sequence_code)
            request.config.cache.set("compound_sequence_project_id", project_id)
            logger.info("==================== test_template_manage06 over =======================")

        @allure.title("新建项目并关联【混合物/配方】模板")
        @pytest.mark.order(7)
        def test_template_manage07(self, load_project_and_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage07 started ====================")
            project_and_template_page = ProjectAndTemplatePage(load_project_and_template_page)
            project_and_template_page.wait_according_to_the_interface(
                ProjectCreateAPI,
                lambda: project_and_template_page.new_project(
                    self.project_name.mixture_formula_name,
                    self.project_code.mixture_formula_code,
                    self.project_data.start_time,
                    self.project_data.end_time
                )
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            project_and_template_page.assert_project(self.project_name.mixture_formula_name)
            project_and_template_page.add_related_template(
                self.project_name.mixture_formula_name,
                logger.info(f"cache.get('mixture_formula_template_name') 已调用")
                request.config.cache.get("mixture_formula_template_name", None)
            )
            project_id = project_and_template_page.get_project_id(self.project_name.mixture_formula_name)
            project_and_template_page.project_apply(
                self.project_name.mixture_formula_name,
                self.project_code.mixture_formula_code,
                project_id
            )
            project_and_template_page.project_start(
                self.project_name.mixture_formula_name,
                self.project_code.mixture_formula_code,
                project_id
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            # 替换后的断言：使用数据中心和单注册页面验证项目可见
            data_center_page = DataCenterPage(load_project_and_template_page)
            data_center_page.assert_project_visible(self.project_name.mixture_formula_name)
            single_register_page = SingleRegisterPage(load_project_and_template_page)
            single_register_page.assert_project_visible(self.project_name.mixture_formula_name)
            request.config.cache.set("mixture_formula_project_name", self.project_name.mixture_formula_name)
            request.config.cache.set("mixture_formula_project_code", self.project_code.mixture_formula_code)
            request.config.cache.set("mixture_formula_project_id", project_id)
            logger.info("==================== test_template_manage07 over =======================")

        @allure.title("新建项目并关联【自定义物质】模板")
        @pytest.mark.order(8)
        def test_template_manage08(self, load_project_and_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage08 started ====================")
            project_and_template_page = ProjectAndTemplatePage(load_project_and_template_page)
            project_and_template_page.wait_according_to_the_interface(
                ProjectCreateAPI,
                lambda: project_and_template_page.new_project(
                    self.project_name.custom_compound_name,
                    self.project_code.custom_compound_code,
                    self.project_data.start_time,
                    self.project_data.end_time
                )
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            project_and_template_page.assert_project(self.project_name.custom_compound_name)
            project_and_template_page.add_related_template(
                self.project_name.custom_compound_name,
                logger.info(f"cache.get('custom_compound_template_name') 已调用")
                request.config.cache.get("custom_compound_template_name", None)
            )
            project_id = project_and_template_page.get_project_id(self.project_name.custom_compound_name)
            project_and_template_page.project_apply(
                self.project_name.custom_compound_name,
                self.project_code.custom_compound_code,
                project_id
            )
            project_and_template_page.project_start(
                self.project_name.custom_compound_name,
                self.project_code.custom_compound_code,
                project_id
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            # 替换后的断言
            data_center_page = DataCenterPage(load_project_and_template_page)
            data_center_page.assert_project_visible(self.project_name.custom_compound_name)
            single_register_page = SingleRegisterPage(load_project_and_template_page)
            single_register_page.assert_project_visible(self.project_name.custom_compound_name)
            request.config.cache.set("custom_compound_project_name", self.project_name.custom_compound_name)
            request.config.cache.set("custom_compound_project_code", self.project_code.custom_compound_code)
            request.config.cache.set("custom_compound_project_id", project_id)
            logger.info("==================== test_template_manage08 over =======================")

        @allure.title("新建项目并关联【DNA】模板")
        @pytest.mark.order(9)
        def test_template_manage09(self, load_project_and_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage09 started ====================")
            project_and_template_page = ProjectAndTemplatePage(load_project_and_template_page)
            project_and_template_page.wait_according_to_the_interface(
                ProjectCreateAPI,
                lambda: project_and_template_page.new_project(
                    self.project_name.DNA_name,
                    self.project_code.DNA_code,
                    self.project_data.start_time,
                    self.project_data.end_time
                )
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            project_and_template_page.assert_project(self.project_name.DNA_name)
            project_and_template_page.add_related_template(
                self.project_name.DNA_name,
                logger.info(f"cache.get('DNA_template_name') 已调用")
                request.config.cache.get("DNA_template_name", None)
            )
            project_id = project_and_template_page.get_project_id(self.project_name.DNA_name)
            project_and_template_page.project_apply(
                self.project_name.DNA_name,
                self.project_code.DNA_code,
                project_id
            )
            project_and_template_page.project_start(
                self.project_name.DNA_name,
                self.project_code.DNA_code,
                project_id
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            # 替换后的断言
            data_center_page = DataCenterPage(load_project_and_template_page)
            data_center_page.assert_project_visible(self.project_name.DNA_name)
            single_register_page = SingleRegisterPage(load_project_and_template_page)
            single_register_page.assert_project_visible(self.project_name.DNA_name)
            request.config.cache.set("DNA_project_name", self.project_name.DNA_name)
            request.config.cache.set("DNA_project_code", self.project_code.DNA_code)
            request.config.cache.set("DNA_project_id", project_id)
            logger.info("==================== test_template_manage09 over =======================")

        @allure.title("新建项目并关联【RNA】模板")
        @pytest.mark.order(10)
        def test_template_manage10(self, load_project_and_template_page, request: pytest.FixtureRequest):
            logger.info("==================== test_template_manage10 started ====================")
            project_and_template_page = ProjectAndTemplatePage(load_project_and_template_page)
            project_and_template_page.wait_according_to_the_interface(
                ProjectCreateAPI,
                lambda: project_and_template_page.new_project(
                    self.project_name.RNA_name,
                    self.project_code.RNA_code,
                    self.project_data.start_time,
                    self.project_data.end_time
                )
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            project_and_template_page.assert_project(self.project_name.RNA_name)
            project_and_template_page.add_related_template(
                self.project_name.RNA_name,
                logger.info(f"cache.get('RNA_template_name') 已调用")
                request.config.cache.get("RNA_template_name", None)
            )
            project_id = project_and_template_page.get_project_id(self.project_name.RNA_name)
            project_and_template_page.project_apply(
                self.project_name.RNA_name,
                self.project_code.RNA_code,
                project_id
            )
            project_and_template_page.project_start(
                self.project_name.RNA_name,
                self.project_code.RNA_code,
                project_id
            )
            project_and_template_page.page.wait_for_timeout(60000)
            project_and_template_page.reload()
            # 替换后的断言
            data_center_page = DataCenterPage(load_project_and_template_page)
            data_center_page.assert_project_visible(self.project_name.RNA_name)
            single_register_page = SingleRegisterPage(load_project_and_template_page)
            single_register_page.assert_project_visible(self.project_name.RNA_name)
            request.config.cache.set("RNA_project_name", self.project_name.RNA_name)
            request.config.cache.set("RNA_project_code", self.project_code.RNA_code)
            request.config.cache.set("RNA_project_id", project_id)
            logger.info("==================== test_template_manage10 over =======================")