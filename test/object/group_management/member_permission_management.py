import allure

from config.setting import GetRolePermissionAPI
from locator.group_management.member_permission_management import \
    MemberPermissionManagementLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.log import logger


class MemberPermissionManagementPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    def enter_member_permission_management_page(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.member_permissions_management)
        self.click(InCMSLocator.member_permissions_management)

    @allure.step("进入成员权限管理-成员管理界面")
    def enter_member_management_page(self):
        self.enter_member_permission_management_page()

    @allure.step("进入成员权限管理-角色权限界面")
    def enter_role_permission_page(self):
        self.enter_member_permission_management_page()
        self.click(MemberPermissionManagementLocator.role_permission)
        self.wait_for(MemberPermissionManagementLocator.assert_role_permission, "visible")
        logger.info("已成功进入角色权限界面")

    @allure.step("配置普通成员注册权限")
    def config_normal_member_register_permission(self,permission:bool = True):
        # 需要两次点击，第一次模拟鼠标悬浮元素激活点击
        self.click_canvas(MemberPermissionManagementLocator.configure_registration_permissions)
        self.click_canvas(MemberPermissionManagementLocator.configure_registration_permissions)
        self.page.wait_for_timeout(3000)
        # 选中全部项目
        # permission为Ture，开启权限
        if permission:
            if not self.is_visible(MemberPermissionManagementLocator.all_projects_checkbox_checked):
                self.click(MemberPermissionManagementLocator.all_projects_checkbox)
            if not self.is_visible(MemberPermissionManagementLocator.visible_register_checked):
                self.click(MemberPermissionManagementLocator.visible_register)
                self.page.wait_for_timeout(1000)
            if not self.is_visible(MemberPermissionManagementLocator.update_data_checked):
                self.click(MemberPermissionManagementLocator.update_data)
        # permission为False，关闭权限
        if not permission:
            while (self.is_visible(MemberPermissionManagementLocator.all_projects_checkbox_checked)
                   or self.is_visible(MemberPermissionManagementLocator.all_projects_checkbox_indeterminate)):
                self.click(MemberPermissionManagementLocator.all_projects_checkbox)
        self.click(MemberPermissionManagementLocator.submit)

    # ---- 角色权限 ----

    _PERMISSION_OPTIONS = {
        "可操作": MemberPermissionManagementLocator.operable_option,
        "页面不可见": MemberPermissionManagementLocator.page_invisible_option,
    }

    @allure.step("配置角色出库权限")
    def config_role_outbound_permission(self, permissions: list):
        """
        依次为群主/CMS管理员/CMS库管员/普通成员设置出库权限
        :param permissions: ["可操作", "页面不可见", "可操作", "页面不可见"]
        """
        for i, perm in enumerate(permissions):
            self.click_nth(MemberPermissionManagementLocator.outbound_select, i)
            self.page.wait_for_timeout(500)
            self.click_nth(self._PERMISSION_OPTIONS[perm], 0)
            logger.info(f"已设置第{i+1}个角色出库权限为: {perm}")

    @allure.step("检查保存按钮是否可点击交互")
    def is_save_button_interactive(self):
        """
        通过检查元素 is_enabled 状态及 aria-disabled 属性判断保存按钮是否可交互
        配置完页面不可见后需等待 UI 刷新再调用
        :return: True=可交互（权限已变更需保存），False=不可交互（权限未变更）
        """
        self.page.wait_for_timeout(500)
        save_loc = self.find(MemberPermissionManagementLocator.save)
        aria_disabled = save_loc.get_attribute("aria-disabled")
        enabled = save_loc.is_enabled()
        interactive = enabled and aria_disabled != "true"
        if interactive:
            logger.info("保存按钮可交互，权限已变更")
        else:
            logger.info("保存按钮不可交互，权限未变更，原本已是页面不可见")
        return interactive

    @allure.step("保存角色权限")
    def save_role_permission(self):
        """点击保存并等待接口响应"""
        self.wait_according_to_the_interface(
            GetRolePermissionAPI,
            lambda: self.click(MemberPermissionManagementLocator.save)
        )

    _OUTBOUND_VALUE_MAP = {
        "可操作": 2,
        "页面不可见": 0,
    }

    _ROLE_NAMES = ["群主", "CMS管理员", "CMS库管员", "普通成员"]

    @allure.step("获取并验证角色权限")
    def verify_role_permissions(self, expected: list):
        """
        调用接口获取角色权限并验证各角色的出库权限
        :param expected: ["可操作", "页面不可见", "可操作", "页面不可见"]
        """
        self.page.wait_for_timeout(3000)
        response = self.page.request.get(GetRolePermissionAPI)
        if response.status != 200:
            raise RuntimeError(f"获取角色权限失败，状态码: {response.status}")
        data = response.json()
        roles = data['data']['data']
        for i, perm in enumerate(expected):
            role_name = self._ROLE_NAMES[i]
            expected_value = self._OUTBOUND_VALUE_MAP[perm]
            actual_value = None
            for item in roles:
                if item['roleName'] == role_name:
                    actual_value = item['authData'].get('outbound')
                    break
            logger.info(f"验证 {role_name} 出库权限: 期望={perm}({expected_value}), 实际={actual_value}")
            assert actual_value == expected_value, \
                f"{role_name} 出库权限不匹配，期望={perm}({expected_value})，实际={actual_value}"
        logger.info("角色权限验证通过")




