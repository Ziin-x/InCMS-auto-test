from config.Expection import APIResponseError, ElementNotFoundError
from config.setting import ProjectAPI, ProjectIdAPI
from locator.group_management.template_management import (
    ProjectAndTemplateLocator, RegistrationTemplateLocator,
    TemplateManagementLocator)
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure


class TemplateManagementPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("进入模版管理界面")
    def enter_template_management(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.template_management)
        self.click(InCMSLocator.template_management)

    @allure.step("进入项目和模版界面")
    def enter_project_and_template(self):
        self.ensure_dropdown_expanded(InCMSLocator.group_management, InCMSLocator.template_management)
        self.click(InCMSLocator.template_management)
        self.click(TemplateManagementLocator.project_and_template_button)


class RegistrationTemplatePage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("点击新建，选择类型")
    def enter_new_interface(self,type):
        self.click(RegistrationTemplateLocator.add_template_button)
        template_loc = load_ele_param(RegistrationTemplateLocator.template_type,type)
        self.click(template_loc)

    @allure.step("添加所有模块")
    def add_all_module(self):
        frame = self.get_frame(RegistrationTemplateLocator.template_frame)
        frame.click(RegistrationTemplateLocator.add_module_button)
        frame.click_all(RegistrationTemplateLocator.module)

    @allure.step("重命名模版")
    def rename_template(self,template_name):
        self.click_and_input(RegistrationTemplateLocator.template_name, template_name)

    @allure.step("添加自定义字段")
    def add_custom_field(self, field_name):
        self.click(RegistrationTemplateLocator.field_setting)
        self.wait_for(RegistrationTemplateLocator.component_module_configuration,state="visible")
        element_bool = False
        if self.is_visible(RegistrationTemplateLocator.new_field_1):
            element_bool = True
            self.click(RegistrationTemplateLocator.new_field_1)
            self.fill(RegistrationTemplateLocator.field_title_1,field_name)
            # 有两层弹窗，两次确认
            self.click(RegistrationTemplateLocator.confirm_button_1)
            self.click(RegistrationTemplateLocator.confirm_button)
        elif self.is_visible(RegistrationTemplateLocator.new_field_2):
            element_bool = True
            self.click(RegistrationTemplateLocator.new_field_2)
            self.fill_special(RegistrationTemplateLocator.field_title_2,field_name)
            # 有两层弹窗，两次确认
            self.click(RegistrationTemplateLocator.confirm_button_2)
            self.page.wait_for_timeout(500)
            self.click(RegistrationTemplateLocator.confirm_button)
        if element_bool == False:
            logger.error("未找到新建字段元素")
            raise ElementNotFoundError("未找到新建字段元素")

    @allure.step("添加自定义参数")
    def add_custom_parameter(self, module_name,parameter_name,tip_message,parameter_option):
        frame = self.get_frame(RegistrationTemplateLocator.template_frame)
        setting_loc = load_ele_param(RegistrationTemplateLocator.setting_button,module_name)
        frame.scroll_to_element(setting_loc,block="center")
        frame.click(setting_loc)
        frame.click(RegistrationTemplateLocator.parameter_setting)
        frame.click(RegistrationTemplateLocator.add_button)
        frame.fill(RegistrationTemplateLocator.parameter_name,parameter_name)
        frame.fill(RegistrationTemplateLocator.tip_message,tip_message)
        option_inputs = frame.find(RegistrationTemplateLocator.parameter_option).all()
        logger.info(option_inputs)
        try:
            logger.debug(f"在所有{RegistrationTemplateLocator.parameter_option}元素中输入")
            if len(option_inputs) != len(parameter_option):
                logger.warning(f"选项输入框数量({len(option_inputs)})与数据({len(parameter_option)})不匹配")
                raise ValueError
            for element_loc,option_value in zip(option_inputs, parameter_option):
                self.fill(element_loc,option_value)
            logger.info(f"在所有{RegistrationTemplateLocator.parameter_option}元素输入成功")
        except Exception as e:
            logger.error(f"在所有{RegistrationTemplateLocator.parameter_option}元素中输入失败，错误：{e}")
            raise
        frame.click(RegistrationTemplateLocator.save_custom_parameter_button)

    @allure.step("保存模版")
    def save_template(self):
        self.click(RegistrationTemplateLocator.save_template_button)

    @allure.step("断言模版是否存在")
    def assert_template(self,template_name):
        self.reload()
        assert_loc = load_ele_param(RegistrationTemplateLocator.assert_template_element, template_name)
        try:
            self.wait_for(assert_loc,"visible")
        except Exception as e:
            logger.error(f"断言模版存在失败，错误：{e}")
            raise ElementNotFoundError(
            f"模版 '{template_name}' 在注册模版的模版列表中不可见，等待超时或元素不存在。原始错误：{e}"
        )

    # 对于相同位置因为重复渲染或其他原因出现重复的相同元素，需要使用特殊方法填充
    def fill_special(self,locator_desc,text):
        loc_list = self.find(locator_desc).all()
        if len(loc_list) >= 1:
            self.fill(loc_list[0],text)
        else:
            logger.error(f"未找到元素：{locator_desc}")
            raise ElementNotFoundError(f"未找到元素：{locator_desc}")

class ProjectAndTemplatePage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.TemplateManagementObject = TemplateManagementPage(self.page)

    def new_project(self,project_name,project_code,start_time,end_time):
        self.click(ProjectAndTemplateLocator.add_project_button)
        self.fill(ProjectAndTemplateLocator.project_name,project_name)
        self.fill(ProjectAndTemplateLocator.project_code,project_code)
        self.fill(ProjectAndTemplateLocator.start_time,start_time)
        self.fill(ProjectAndTemplateLocator.end_time,end_time)
        self.click(ProjectAndTemplateLocator.confirm_button)

    # 初步断崖项目与模版界面是否有创建的项目
    def assert_project(self, project_name):
        self.click(TemplateManagementLocator.project_and_template_button)
        assert_loc = load_ele_param(ProjectAndTemplateLocator.project_and_template, project_name)
        try:
            self.wait_for(assert_loc,"visible",timeout=30000)
        except Exception as e:
            logger.error(f"断言项目创建失败，错误：{e}")
            raise ElementNotFoundError(
            f"项目 '{project_name}' 在的项目与模版界面中不可见，等待超时或元素不存在。原始错误：{e}"
        )

    @allure.step("添加关联模版")
    def add_related_template(self,project_name,template_name):
        self.fill(ProjectAndTemplateLocator.search_box,project_name)
        self.click(ProjectAndTemplateLocator.search_button)
        add_related_loc = load_ele_param(ProjectAndTemplateLocator.add_associated_template, project_name)
        self.click(add_related_loc)
        # 在框内输入后
        self.click_and_input(ProjectAndTemplateLocator.associated_template_dropdown,template_name)
        self.page.wait_for_timeout(1000)
        option_loc = load_ele_param(ProjectAndTemplateLocator.template_option, template_name)
        self.click(option_loc)
        self.page.wait_for_timeout(1000)
        # 选择完成后点击下拉框收回
        self.esc()
        self.esc()
        self.click(ProjectAndTemplateLocator.confirm_button)

    @allure.step("调用接口,获取项目id，同时断言项目是否存在inProject的后端中")
    def get_project_id(self,project_name):
        logger.info(f"请求的URL: {ProjectIdAPI}")
        # 等待 SSO token 交换完成，避免因时序问题导致 401
        self.page.wait_for_timeout(2000)
        payload = {}
        response = self.page.request.post(ProjectIdAPI, data=payload)
        if response.status == 200:
            logger.info("响应返回200，获取项目列表成功")
        else:
            logger.error(f"获取项目列表失败，获取到的响应为{response.status}")
            raise APIResponseError(f"获取项目列表失败，获取到的响应为{response.status}")
        data = response.json()['data']
        assert_project = False
        for i in data:
            if i['name'] == project_name:
                logger.info(f"获取项目id为{i}")
                return i['id']
        logger.info(f"项目 '{project_name}' 在项目列表中{'存在' if assert_project else '不存在'}")
        assert assert_project, f"项目 '{project_name}' 在项目列表中不存在"

    @allure.step("调用接口,项目立项")
    def project_apply(self,project_name,project_code,project_id):
        logger.info(f"请求的URL: {ProjectAPI}")
        payload = {
            "project_data": [
                {
                    "project_id": project_id,
                    "reason": "",
                    "approval_node_list": [],
                    "attachment": "",
                    "start_time": "",
                    "end_time": "",
                    "end_type": None,
                    "code": project_code,
                    "name": project_name
                }
            ],
            "operate_type": "project_set"
        }
        response = self.page.request.post(ProjectAPI, data=payload)
        if response.status == 200:
            logger.info("响应返回200，项目立项成功")
        else:
            logger.error(f"项目立项失败，获取到的响应为{response.json()}")
            raise APIResponseError(f"项目立项失败，获取到的响应为{response.json()}")

    @allure.step("调用接口,项目启动")
    def project_start(self,project_name,project_code,project_id):
        logger.info(f"请求的URL: {ProjectAPI}")
        payload = {
            "project_data": [
                {
                    "project_id": project_id,
                    "reason": "",
                    "approval_node_list": [],
                    "attachment": "",
                    "start_time": "",
                    "end_time": "",
                    "end_type": None,
                    "code": project_code,
                    "name": project_name
                }
            ],
            "operate_type": "project_start"
        }
        response = self.page.request.post(ProjectAPI, data=payload)
        if response.status == 200:
            logger.info("响应返回200，项目启动成功")
        else:
            logger.error(f"项目启动失败，获取到的响应为{response.json()}")
            raise APIResponseError(f"项目启动失败，获取到的响应为{response.json()}")









