import pytest

from data.pydantic.enterprise_level_management.storage_and_container import \
    StorageAndContainerData
from object.enterprise_level_management.storage_and_container import \
    StorageAndContainer
from utils.log import logger

import allure


@allure.epic("企业级管理")
@allure.feature("库位与容器")
class TestStorageAndContainer:

    data = StorageAndContainerData.get_data()
    type_name = data.type_name
    abbreviation = data.abbreviation
    field_title = data.field_title

    @allure.title("库位与容器新建位置")
    @pytest.mark.order(11)
    def test_storage_and_container01(self, InCMS_page):
        logger.info("==================== test_storage_and_container01 started ====================")
        storage_and_container_page = StorageAndContainer(InCMS_page)
        # 进入后默认是位置界面，不需要传入界面名称切换界面
        storage_and_container_page.enter_page()
        storage_and_container_page.new_location(self.type_name.location,self.abbreviation.location,self.field_title)
        storage_and_container_page.assert_new_success(self.type_name.location)
        logger.info("==================== test_storage_and_container01 over =======================")

    @allure.title("库位与容器新建盒子")
    @pytest.mark.order(12)
    def test_storage_and_container02(self, InCMS_page):
        logger.info("==================== test_storage_and_container02 started ====================")
        storage_and_container_page = StorageAndContainer(InCMS_page)
        # 切换到盒子界面
        storage_and_container_page.enter_page("盒子")
        storage_and_container_page.new_box(self.type_name.box,self.abbreviation.box,self.field_title)
        storage_and_container_page.assert_new_success(self.type_name.box)
        (logger.info("==================== test_storage_and_container02 over ======================="))

    @allure.title("库位与容器新建孔板")
    @pytest.mark.order(13)
    def test_storage_and_container03(self, InCMS_page):
        logger.info("==================== test_storage_and_container03 started ====================")
        storage_and_container_page = StorageAndContainer(InCMS_page)
        # 切换到孔板界面
        storage_and_container_page.enter_page("孔板")
        storage_and_container_page.new_hole_plate(self.type_name.hole_plate,self.abbreviation.hole_plate,self.field_title)
        storage_and_container_page.assert_new_success(self.type_name.hole_plate)
        (logger.info("==================== test_storage_and_container03 over ======================="))

    @allure.title("库位与容器新建样品管")
    @pytest.mark.order(14)
    def test_storage_and_container04(self, InCMS_page):
        logger.info("==================== test_storage_and_container04 started ====================")
        storage_and_container_page = StorageAndContainer(InCMS_page)
        # 切换到样品管界面
        storage_and_container_page.enter_page("样品管")
        storage_and_container_page.new_sample_tube(self.type_name.sample_tube, self.abbreviation.sample_tube, self.field_title)
        storage_and_container_page.assert_new_success(self.type_name.sample_tube)
        logger.info("==================== test_storage_and_container04 over =======================")