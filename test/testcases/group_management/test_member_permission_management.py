import allure
import pytest

from config.Expection import ElementNotFoundError, TestFailedError
from config.environments_pydantic import Environment
from config.setting import (ConfigRegisterPermissionAPI,
                            SingleRegistrationSubstanceAPI)
from data.pydantic.plug_pydantic import PlugPageData
from locator.material_view import MaterialViewLocator
from object.data_center.data_center import DataCenterPage
from object.data_center.single_register import SingleRegisterPage
from object.data_up.data_up import DataUpPage
from object.fixture_object.login_page_object import LoginPageObject
from object.fixture_object.plug_page_object import PlugPageObject
from object.group_management.member_permission_management import \
    MemberPermissionManagementPage
from utils.auto_generated_data import generate_batch_number
from utils.load_ele_param import load_ele_param
from utils.log import logger

env = Environment.get_data()
plug_data = PlugPageData.get_data()


@allure.epic("群内管理")
@allure.feature("成员权限管理")
class TestMemberPermissionManagement:

    @allure.title("成员权限管理完整流程 [{permission_data}]")
    @pytest.mark.order(15)
    @pytest.mark.parametrize("permission_data", [False, True])
    def test_member_permission_flow(self, InCMS_page, browser, request: pytest.FixtureRequest, permission_data: bool):
        """
        permission_data=False 先执行（关闭权限），permission_data=True 后执行（开启权限）。
        大号设置权限后，通过 sync_playwright 打开独立浏览器登录小号完成效验。
        """
        logger.info(f"==================== test_member_permission_flow [{permission_data}] started ====================")

        # ========== Step 1: 大号设置成员权限 + 首次运行时注册化合物 ==========
        member_management_page = MemberPermissionManagementPage(InCMS_page)
        member_management_page.enter_member_management_page()
        member_management_page.wait_according_to_the_interface(
            ConfigRegisterPermissionAPI,
            lambda: member_management_page.config_normal_member_register_permission(permission=permission_data)
        )
        InCMS_page.wait_for_timeout(3000)

        logger.info(f"cache.get('member_permission_project') 已调用")
        if request.config.cache.get("member_permission_project", None) is None:
            project_name = request.config.cache.get("compound_sequence_project_name", None)
            logger.info(f"cache.get('compound_sequence_project_name') = {project_name}")
            batch_number = generate_batch_number('化合物/序列')
            single_register = SingleRegisterPage(InCMS_page)
            single_register.single_register_ingredients(project_name)
            single_register.single_register_batch_member(batch_number)
            single_register.register_material_amount('100')
            single_register.wait_according_to_the_interface(
                SingleRegistrationSubstanceAPI,
                single_register.confirm_register
            )
            request.config.cache.set("member_permission_project", batch_number)
            logger.info(f"大号注册化合物成功，批号: {batch_number}")

        project_name = request.config.cache.get("compound_sequence_project_name", None)
        logger.info(f"cache.get('compound_sequence_project_name') = {project_name}")
        if project_name is None:
            logger.error("compound_sequence_project_name 缓存为空")
            raise TestFailedError("compound_sequence_project_name 缓存为空")
        else:
            logger.info(f"获取项目名称成功，名称: {project_name}")

        # ========== Step 2 & 3: 打开小号浏览器完成效验 ==========
        member_context = browser.new_context()
        member_page = member_context.new_page()

        # 登录小号
        login_page = LoginPageObject(member_page)
        login_page.login_plug(env, member_login=True)

        # 选择 CMS 产品
        plug_page = PlugPageObject(member_page)
        plug_page.page.wait_for_load_state('networkidle')
        plug_page.choose_product(plug_data.cms)

        # ---- Step 2: 效验可见可注册权限 ----

        dc_page = DataCenterPage(member_page)
        try:
            dc_page.assert_project_visible(project_name=project_name)
            dc_visible = True
        except ElementNotFoundError:
            dc_visible = False

        sr_page = SingleRegisterPage(member_page)
        try:
            sr_page.assert_project_visible(project_name=project_name)
            sr_visible = True
        except ElementNotFoundError:
            sr_visible = False

        if permission_data:
            if not dc_visible:
                logger.error("权限开启，项目在数据中心不可见，测试失败")
                raise TestFailedError("权限开启，项目在数据中心不可见，测试失败")
            if not sr_visible:
                logger.error("权限开启，项目在单个注册不可见，测试失败")
                raise TestFailedError("权限开启，项目在单个注册不可见，测试失败")
            logger.info("权限开启，项目可见性验证通过")
        else:
            if dc_visible:
                logger.error("无权限，项目在数据中心可见，测试失败")
                raise TestFailedError("无权限，项目在数据中心可见，测试失败")
            if sr_visible:
                logger.error("无权限，项目在单个注册可见，测试失败")
                raise TestFailedError("无权限，项目在单个注册可见，测试失败")
            logger.info("无权限，项目不可见验证通过")

        # ---- Step 3: 效验数据更新权限 ----
        # 通过侧边栏导航进入数据更新页面（非新窗口）
        data_up_page = DataUpPage(member_page)
        data_up_page.switch_to_data_up_page()

        project_name_in_data_up = load_ele_param(MaterialViewLocator.data_up_project_name, project_name)
        project_visible_in_data_up = data_up_page.is_visible(project_name_in_data_up, timeout=5000)

        if permission_data:
            if not project_visible_in_data_up:
                logger.error("权限开启，数据更新页面中项目名称不可见，测试失败")
                raise TestFailedError("权限开启，数据更新页面中项目名称不可见，测试失败")
            logger.info("权限开启，数据更新页面项目名称可见，测试通过")
        else:
            if project_visible_in_data_up:
                logger.error("无权限，数据更新页面中项目名称可见，测试失败")
                raise TestFailedError("无权限，数据更新页面中项目名称可见，测试失败")
            logger.info("无权限，数据更新页面中项目名称不可见，测试通过")

        member_context.close()

        logger.info(f"==================== test_member_permission_flow [{permission_data}] over =======================")

    # @allure.story("成员管理")
    # @allure.title("小号登录并调用 assert_project_visible 调试")
    # def test_member_assert_project_visible_debug(self, browser, request: pytest.FixtureRequest):
    #     """独立调试方法：小号登录 CMS，测试 assert_project_visible 是否正常"""
    logger.info(f"cache.get('compound_sequence_project_name') 已调用")
    #     project_name = request.config.cache.get("compound_sequence_project_name", None)
    #     logger.info(f"项目名称: {project_name}")
    #
    #     member_context = browser.new_context()
    #     member_page = member_context.new_page()
    #
    #     login_page = LoginPageObject(member_page)
    #     login_page.login_plug(.env, member_login=True)
    #
    #     plug_page = PlugPageObject(member_page)
    #     plug_page.page.wait_for_load_state('networkidle')
    #     plug_page.choose_product(plug_data.cms)
    #
    #     sr_page = SingleRegisterPage(member_page)
    #     try:
    #         sr_page.assert_project_visible(project_name=project_name)
    #         logger.info("✅ 单个注册: 项目可见")
    #     except ElementNotFoundError:
    #         logger.info("❌ 单个注册: 项目不可见")
    #
    #     member_context.close()


@allure.epic("管理")
@allure.feature("成员权限管理-角色权限")
class TestRolePermission:

    @allure.story("角色权限")
    @allure.title("更改角色出库权限，并读取响应验证")
    @pytest.mark.order(16)
    def test_role_permission(self, InCMS_page):
        logger.info("==================== test_role_permission started ====================")
        member_page = MemberPermissionManagementPage(InCMS_page)
        member_page.enter_role_permission_page()

        # 全部设置为页面不可见（依次：群主/CMS管理员/CMS库管员/普通成员）
        all_invisible = ["页面不可见"] * 4
        member_page.config_role_outbound_permission(all_invisible)
        if member_page.is_save_button_interactive():
            member_page.save_role_permission()
            member_page.verify_role_permissions(all_invisible)

        # 全部设置为可操作
        all_operable = ["可操作"] * 4
        member_page.config_role_outbound_permission(all_operable)
        member_page.save_role_permission()
        member_page.verify_role_permissions(all_operable)

        logger.info("==================== test_role_permission over =======================")



