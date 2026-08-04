import traceback

import allure
import pytest

from config.environments_pydantic import Environment
from config.Expection import EnvironmentConfigError
from locator.fixture_loactor.login_page_loactor import LoginPageLocator
from object.basepage import BasePage


class LoginPageObject(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("登录")
    def login_plug(self,env: Environment,member_login: bool = False):
        """
        :param env:指定运行环境，实际就是控制url和用户信息不同 ，这里以后可能会分化出来user参数，当涉及到角色权限时，现在还没想好怎么管理
        :return:
        """
        # 检查环境是否存在
        if not env:
            raise EnvironmentConfigError(f"环境 '{env}' 未配置")
        # 检查配置是否完整
        if not env.url:
            print(f"错误：环境 '{env}' 的URL未配置")
            return False
        try:
            self.page.goto(env.url)
            if member_login:
                self.fill(LoginPageLocator.account_input,env.member_username)
                self.fill(LoginPageLocator.password_input,env.member_password)
            else:
                self.fill(LoginPageLocator.account_input,env.username)
                self.fill(LoginPageLocator.password_input,env.password)
            self.click(LoginPageLocator.login_button)
            # 等待登录成功,检查登录后的url
            self.page.wait_for_url("**/site/index")
            #检测元素可见
            self.is_visible(LoginPageLocator.check_login_plug)
            print(f"已导航到环境: {env.name}")
            print(f"用户名: {env.username}")
        except Exception :
            traceback.print_exc()
            pytest.exit('登录失败停止测试执行', returncode=1)

