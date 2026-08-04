from locator.enterprise_level_management.storage_and_container import \
    StorageAndContainerLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure
from playwright.sync_api import Locator


class StorageAndContainer(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("进入库位与容器界面")
    def enter_storage_and_container(self):
        self.ensure_dropdown_expanded(InCMSLocator.enterprise_management, InCMSLocator.storage_and_container)
        self.click(InCMSLocator.storage_and_container)

    # 通用新建步骤
    def general_new_step(self,new_loc: Locator,type_name: str,abbreviation: str,field_title: str):
        self.click(new_loc)
        self.fill(StorageAndContainerLocator.type_name,type_name)
        self.fill(StorageAndContainerLocator.abbreviation,abbreviation)
        self.click(StorageAndContainerLocator.new_attribute_field)
        self.fill(StorageAndContainerLocator.field_title,field_title)
        self.click(StorageAndContainerLocator.confirm_button)

    def confirm_new(self):
        self.click(StorageAndContainerLocator.create_button)

    @allure.step("断言{type_name}是否成功创建")
    def assert_new_success(self,type_name: str):
        assert_loc = load_ele_param(StorageAndContainerLocator.assert_type_name,type_name)
        try:
            logger.debug(f"断言{type_name}是否成功创建存在")
            self.wait_for(assert_loc,"visible")
            logger.info(f"{type_name}创建成功")
        except Exception as e:
            logger.error(f"{type_name}创建失败，错误：{e}")
            raise

    @allure.step("进入{page_name}页面")
    def enter_page(self,page_name=None):
        self.enter_storage_and_container()
        if page_name is not None:
            page_button_loc = load_ele_param(StorageAndContainerLocator.switch_button, page_name)
            self.click(page_button_loc)

    @allure.step("新建位置")
    def new_location(self,type_name: str,abbreviation: str,field_title: str):
        new_loc = load_ele_param(StorageAndContainerLocator.new_button,"位置")
        self.general_new_step(new_loc,type_name,abbreviation,field_title)
        self.confirm_new()

    @allure.step("新建盒子")
    def new_box(self,type_name: str,abbreviation: str,field_title: str):
        new_loc = load_ele_param(StorageAndContainerLocator.new_button,"盒子")
        self.general_new_step(new_loc,type_name,abbreviation,field_title)
        self.click(StorageAndContainerLocator.store_sample_container_type)
        self.click(StorageAndContainerLocator.common_sample_container_option)
        self.confirm_new()

    @allure.step("新建孔板")
    def new_hole_plate(self,type_name: str,abbreviation: str,field_title: str):
        new_loc = load_ele_param(StorageAndContainerLocator.new_button,"孔板")
        self.general_new_step(new_loc,type_name,abbreviation,field_title)
        self.click(StorageAndContainerLocator.specification)
        self.click(StorageAndContainerLocator.hole_plate_option)
        self.confirm_new()

    @allure.step("新建样品管")
    def new_sample_tube(self, type_name: str, abbreviation: str, field_title: str):
        new_loc = load_ele_param(StorageAndContainerLocator.new_button,"样品管")
        self.general_new_step(new_loc,type_name,abbreviation,field_title)
        self.confirm_new()
