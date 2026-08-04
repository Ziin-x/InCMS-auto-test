from config.Expection import TestFailedError
from config.environments_pydantic import Environment
from data.pydantic.data_up.single_data_up import SingleDataUpData
from object.data_center.data_center import DataCenterPage
from object.group_management.review_and_reminder import \
    ReviewAndReminderPage
from object.material_view_page import DataUp, MaterialViewPage
from object.mine.my_approval.data_up_approval_page import \
    DataUpApprovalPage
from object.search_result_page import SearchResultPage
from utils.log import logger

import allure
import pytest


@allure.epic("物质详情页")
@allure.feature("单个更新")
class TestSingleDataUp:
    data = SingleDataUpData.get_data()

    batch_number = data.batch_number
    project_name = data.project_name
    modules_info = data.modules_info

    review_type = "数据更新审核"
    approval_user = Environment.get_data().username

    @allure.title("化合物类型，单个数据更新无审核")
    @pytest.mark.order(29)
    def test_single_data_up01(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_single_data_up01 started ====================")
        # 1.检查物质所属项目是否有数据更新审核，如果有审核，则取消审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.review_type
        )
        # 2.搜索物质批号，跳转至物质详情页
        with InCMS_page.expect_popup() as popup_info:
            data_center_page = DataCenterPage(InCMS_page)
            data_center_page.enter_all_project()
            search_result_page = SearchResultPage(InCMS_page)
            search_result_page.jump_to_material_view_page(
                logger.info(f"cache.get('compound_sequence_batch_number') 已调用")
                request.config.cache.get("compound_sequence_batch_number", None))
        new_page = popup_info.value
        # 3.物质详情页点击数据更新按钮，开始进行数据更新
        data_up_window =  DataUp(new_page)
        data_up_window.compound_single_data_up(modules_info=self.modules_info)
        # 4.刷新页面，检查数据是否更新
        new_page.reload()
        material_view_page = MaterialViewPage(new_page)
        material_view_page.check_material_view_fields_info(self.modules_info)
        logger.info("==================== test_single_data_up01 over =======================")

    @allure.title("数据更新有审核，审核拒绝")
    @pytest.mark.order(30)
    def test_single_data_up02(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_single_data_up02 started ====================")
        # 1.设置项目数据更新审核，审核节点只有一个人
        set_approval_page = ReviewAndReminderPage(InCMS_page)
        set_approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None), self.approval_user, self.review_type)
        # 2.搜索物质批号，进入物质详情页
        with InCMS_page.expect_popup() as popup_info:
            data_center_page = DataCenterPage(InCMS_page)
            data_center_page.enter_all_project()
            search_result_page = SearchResultPage(InCMS_page)
            search_result_page.jump_to_material_view_page(
                logger.info(f"cache.get('compound_sequence_batch_number') 已调用")
                request.config.cache.get("compound_sequence_batch_number", None))
        new_page = popup_info.value
        material_view_page = MaterialViewPage(new_page)
        # 3.获取物质详情页的模块字段信息
        init_material_view_info = material_view_page.get_material_view_fields_info()
        # 4.数据更新
        data_up_window = DataUp(new_page)
        data_up_window.compound_single_data_up(modules_info=self.modules_info)
        # 5.刷新页面，获取当前的物质详情页的模块字段信息
        new_page.reload()
        data_up_without_approval_material_view_info = material_view_page.get_material_view_fields_info()
        # 检查点1：未审核时，提交数据更新后物质详情页数据应与原始数据一致
        if init_material_view_info != data_up_without_approval_material_view_info:
            logger.error("数据更新审核未通过时，物质详情页数据与原始数据不一致")
            raise TestFailedError("数据更新审核未通过时，物质详情页数据与原始数据不一致")
        # 6.跳转至我的-我的审核-数据更新审核，检查待审核中有此条数据
        InCMS_page.bring_to_front()
        my_approval_data_up_page = DataUpApprovalPage(InCMS_page)
        my_approval_data_up_page.switch_to_data_approval_page()
        logger.info(f"cache.get('compound_sequence_batch_number') 已调用")
        my_approval_data_up_page.check_approval_list(1, request.config.cache.get("compound_sequence_batch_number", None))
        # 7.审核拒绝
        my_approval_data_up_page.single_row_approval(1, False)
        # 8.再次进入该物质的物质详情页，检查数据更新后的数据
        new_page.bring_to_front()
        new_page.reload()
        # 检查点2:拒绝数据更新审核后，物质详情页仍显示原始字段
        after_approval_material_view_info = material_view_page.get_material_view_fields_info()
        if init_material_view_info != after_approval_material_view_info:
            logger.error("拒绝数据更新审核后，物质详情页未显示原始字段")
            raise TestFailedError("拒绝数据更新审核后，物质详情页未显示原始字段")
        logger.info("==================== test_single_data_up02 over =======================")

    @allure.title("数据更新有审核，审核通过")
    @pytest.mark.order(31)
    def test_single_data_up03(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_single_data_up03 started ====================")
        # 1.设置项目数据更新审核，审核节点只有一个人
        set_approval_page = ReviewAndReminderPage(InCMS_page)
        set_approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None), self.approval_user, self.review_type)
        # 2.搜索物质批号，进入物质详情页
        with InCMS_page.expect_popup() as popup_info:
            data_center_page = DataCenterPage(InCMS_page)
            data_center_page.enter_all_project()
            search_result_page = SearchResultPage(InCMS_page)
            search_result_page.jump_to_material_view_page(
                logger.info(f"cache.get('compound_sequence_batch_number') 已调用")
                request.config.cache.get("compound_sequence_batch_number", None))
        new_page = popup_info.value
        material_view_page = MaterialViewPage(new_page)
        # 3.获取物质详情页的模块字段信息
        init_material_view_info = material_view_page.get_material_view_fields_info()
        # 4.数据更新
        data_up_window = DataUp(new_page)
        data_up_window.compound_single_data_up(modules_info=self.modules_info)
        # 5.刷新页面，获取当前的物质详情页的模块字段信息
        new_page.reload()
        data_up_without_approval_material_view_info  = material_view_page.get_material_view_fields_info()
        #检查点1：未审核时，提交数据更新后物质详情页数据应与原始数据一致
        if init_material_view_info != data_up_without_approval_material_view_info:
            logger.error("数据更新审核未通过时，物质详情页数据与原始数据不一致")
            raise TestFailedError("数据更新审核未通过时，物质详情页数据与原始数据不一致")
        # 6.跳转至我的-我的审核-数据更新审核，检查待审核中有此条数据
        InCMS_page.bring_to_front()
        my_approval_data_up_page = DataUpApprovalPage(InCMS_page)
        my_approval_data_up_page.switch_to_data_approval_page()
        logger.info(f"cache.get('compound_sequence_batch_number') 已调用")
        my_approval_data_up_page.check_approval_list(1, request.config.cache.get("compound_sequence_batch_number", None))
        # 7.审核同意
        my_approval_data_up_page.single_row_approval(1,True)
        # 8.再次查看该物质的物质详情页，审核检查为数据更新后的数据
        new_page.bring_to_front()
        new_page.reload()
        material_view_page.check_material_view_fields_info(self.modules_info)
        logger.info("==================== test_single_data_up03 over =======================")


