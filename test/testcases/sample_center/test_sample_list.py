from config.environments_pydantic import Environment
from data.pydantic.sample_center.sample_list import SampleListData
from object.group_management.review_and_reminder import ReviewAndReminderPage
from object.group_management.sample_management import GeneralConfigurationPage
from object.mine.my_approval.sample_approval_page import \
    SampleApprovalPage
from object.sample_center.outbound import OutboundPage
from object.sample_center.batch_import import BatchImportPage
from object.sample_center.request_record import RequestRecordPage
from object.sample_center.sample_list import SampleListPage

import allure
import pytest

from utils.log import logger


@allure.epic("样品中心")
@allure.feature("样品管理")
class TestSampleList:

    data = SampleListData.get_data()
    approval_user = Environment.get_data().username

    @allure.title("样品单个登记，无审核")
    @pytest.mark.order(32)
    def test_sample_list01(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list01 started ====================")
        # 检查物质所属项目是否有样品登记审核，如果有审核，则取消审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品登记审核"
        )
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_name = self.data.sample_name
        sample_list_page.wait_loading()
        sample_list_page.register_sample(
            sample_name,
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.data.current_amount
        )
        request.config.cache.set("sample_name", sample_name)
        # 无审核：注册后样品应为在库状态
        status = sample_list_page.get_sample_status(sample_name)
        logger.info(f"样品 [{sample_name}] 状态: sampleStatus={status}")
        assert status == "2", \
            f"无审核登记后样品 [{sample_name}] 应为在库状态(sampleStatus=2)"
        logger.info("==================== test_sample_list01 over =======================")

    # 必须先完成上面用例注册样品
    # 顺便分配任务，为分配的任务模块用例作准备
    @allure.title("获取样品ID，效验群内管理-样品ID模块设置的自动生成规则")
    @pytest.mark.order(33)
    def test_assert_code_rules03(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_assert_code_rules03 started ====================")
        sample_list_page = SampleListPage(InCMS_page)
        sample_id = sample_list_page.get_sample_id(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None)
        )
        sample_list_page.assert_sample_id(
            sample_id,
            logger.info(f"cache.get('id_preview_text') 已调用")
            request.config.cache.get("id_preview_text", None)
        )
        logger.info("==================== test_assert_code_rules03 over =======================")

    @allure.title("全部审核关闭，申领-归还")
    @pytest.mark.order(34)
    def test_sample_list02(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list02 started ====================")
        # 关闭所有审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        for approval_type in ("样品申领审核", "样品接收审核", "样品归还审核"):
            approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            approval_type
        )
        general_configuration_page = GeneralConfigurationPage(InCMS_page)
        general_configuration_page.enter_general_configuration()
        general_configuration_page.page.wait_for_timeout(3000)
        general_configuration_page.auto_outbound_switch(True)
        general_configuration_page.auto_receive_switch(True)
        # 申领
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_request()
        sample_list_page.page.wait_for_timeout(3000)
        # 全部关闭：申领后自动接收，应为已接收
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 归还
        request_record_page = RequestRecordPage(InCMS_page)
        request_record_page.enter_request_record()
        request_record_page.switch_view("已接收")
        request_record_page.assign_task(self.approval_user)
        request_record_page.return_sample()
        # 全部关闭：归还后应为已归还
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "7"
        )
        logger.info("==================== test_sample_list02 over =======================")

    @allure.title("仅开启申领审核，申领-归还")
    @pytest.mark.order(35)
    def test_sample_list03(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list03 started ====================")
        # 仅开启样品申领审核，关闭其余
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.approval_user,
            "样品申领审核"
        )
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品接收审核"
        )
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品归还审核"
        )
        general_configuration_page = GeneralConfigurationPage(InCMS_page)
        general_configuration_page.enter_general_configuration()
        general_configuration_page.page.wait_for_timeout(3000)
        general_configuration_page.auto_outbound_switch(True)
        general_configuration_page.auto_receive_switch(True)
        # 申领
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_request()
        sample_list_page.page.wait_for_timeout(3000)
        # 申领审核中
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "9"
        )
        # 审批通过
        sample_approval_page = SampleApprovalPage(InCMS_page)
        sample_approval_page.switch_to_sample_approval_page()
        sample_approval_page.sample_approval(True)
        # 审批通过后自动接收，应为已接收
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 归还
        request_record_page = RequestRecordPage(InCMS_page)
        request_record_page.enter_request_record()
        request_record_page.switch_view("已接收")
        request_record_page.return_sample()
        # 归还审核关闭，归还后应为已归还
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "7"
        )
        logger.info("==================== test_sample_list03 over =======================")

    # 由于必须手动接收才能触发接收审核，所以自动接收用例与接收审核用例合并执行
    @allure.title("开启接收审核，同时关闭自动接收")
    @pytest.mark.order(36)
    def test_sample_list04(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list04 started ====================")
        # 仅开启样品接收审核，关闭其余
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品申领审核"
        )
        approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.approval_user,
            "样品接收审核"
        )
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品归还审核"
        )
        general_configuration_page = GeneralConfigurationPage(InCMS_page)
        general_configuration_page.enter_general_configuration()
        general_configuration_page.page.wait_for_timeout(3000)
        # 关闭自动接收
        general_configuration_page.auto_outbound_switch(True)
        general_configuration_page.auto_receive_switch(False)
        # 申领
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_request()
        sample_list_page.page.wait_for_timeout(3000)
        # 申请接收
        request_record_page = RequestRecordPage(InCMS_page)
        request_record_page.enter_request_record()
        request_record_page.switch_view("待接收")
        request_record_page.receive_sample()
        # 接收审核中
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "11"
        )
        # 审批通过
        sample_approval_page = SampleApprovalPage(InCMS_page)
        sample_approval_page.switch_to_sample_approval_page()
        sample_approval_page.sample_approval(True)
        # 审批通过后自动接收，应为已接收
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 归还
        request_record_page = RequestRecordPage(InCMS_page)
        request_record_page.enter_request_record()
        request_record_page.switch_view("已接收")
        request_record_page.return_sample()
        # 归还审核关闭，归还后应为已归还
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "7"
        )
        logger.info("==================== test_sample_list04 over =======================")

    # 两个用例流程无冲突，为了与test_sample_list04统一格式，并且从精简角度出发，自动出库用例与归还审核用例也合并
    @allure.title("开启归还审核，同时关闭自动出库")
    @pytest.mark.order(37)
    def test_sample_list05(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list05 started ====================")
        # 仅开启样品归还审核，关闭其余
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品申领审核"
        )
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品接收审核"
        )
        approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.approval_user,
            "样品归还审核"
        )
        general_configuration_page = GeneralConfigurationPage(InCMS_page)
        general_configuration_page.enter_general_configuration()
        general_configuration_page.page.wait_for_timeout(3000)
        # 关闭自动出库
        general_configuration_page.auto_outbound_switch(False)
        general_configuration_page.auto_receive_switch(True)
        # 申领
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_request()
        sample_list_page.page.wait_for_timeout(3000)
        # 状态为待拣货
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "0"
        )
        # 手动拣货
        out_bound_page = OutboundPage(InCMS_page)
        out_bound_page.enter_outbound()
        out_bound_page.switch_view("待拣货")
        out_bound_page.pick_all_pending_samples()
        # 状态为待出库
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "3"
        )
        # 手动出库
        out_bound_page.switch_view("待出库")
        out_bound_page.outbound_all_pending_samples()
        # 申领、接收审核关闭，出库后自动接收，应为已接收
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 归还
        request_record_page = RequestRecordPage(InCMS_page)
        request_record_page.enter_request_record()
        request_record_page.switch_view("已接收")
        request_record_page.return_sample()
        # 归还审核中
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "12"
        )
        # 审批通过
        sample_approval_page = SampleApprovalPage(InCMS_page)
        sample_approval_page.switch_to_sample_approval_page()
        sample_approval_page.sample_approval(True)
        # 审批通过后应为已归还
        sample_list_page.assert_sample_request_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "7"
        )
        logger.info("==================== test_sample_list05 over =======================")

    @allure.title("无审批，样品报废")
    @pytest.mark.order(38)
    def test_sample_list06(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list06 started ====================")
        # 关闭样品报废审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            "样品报废审核"
        )
        # 进入样品列表，报废
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_scrap()
        sample_list_page.page.wait_for_timeout(3000)
        # 无审批：报废后样品应为已报废状态
        sample_list_page.assert_sample_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 样品已报废，清除缓存中的样品名称
        request.config.cache.set("sample_name", None)
        logger.info("==================== test_sample_list06 over =======================")

    @allure.title("样品单个登记，有审核")
    @pytest.mark.order(39)
    def test_sample_list07(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list07 started ====================")
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.approval_user,
            "样品登记审核"
        )
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_name = self.data.sample_name
        sample_list_page.register_sample(
            sample_name,
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.data.current_amount
        )
        request.config.cache.set("sample_name", sample_name)
        # 审核未通过：样品应为待审批状态
        status = sample_list_page.get_sample_status(sample_name)
        logger.info(f"审核前样品 [{sample_name}] 状态: sampleStatus={status}")
        assert status == "7", \
            f"审核未通过时样品 [{sample_name}] 应为待审批状态(sampleStatus=7)"
        # 跳转至我的-我的审核-样品相关审核，审核通过
        sample_approval_page = SampleApprovalPage(InCMS_page)
        sample_approval_page.switch_to_sample_approval_page()
        sample_approval_page.sample_approval(True)
        # 审核通过后：样品应为在库状态
        status = SampleListPage(InCMS_page).get_sample_status(sample_name)
        logger.info(f"审核后样品 [{sample_name}] 状态: sampleStatus={status}")
        assert status == "2", \
            f"审核通过后样品 [{sample_name}] 应为在库状态(sampleStatus=2)，或审核失效"
        logger.info("==================== test_sample_list07 over =======================")

    @allure.title("有审批，样品报废")
    @pytest.mark.order(40)
    def test_sample_list08(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_list08 started ====================")
        # 开启样品报废审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None),
            self.approval_user,
            "样品报废审核"
        )
        # 进入样品列表，报废
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_scrap()
        sample_list_page.page.wait_for_timeout(3000)
        # 有审批：报废后样品应为报废审批中状态
        sample_list_page.assert_sample_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "8"
        )
        # 跳转至我的-我的审核-样品相关审核，审核通过
        sample_approval_page = SampleApprovalPage(InCMS_page)
        sample_approval_page.switch_to_sample_approval_page()
        sample_approval_page.sample_approval(True)
        # 审核通过后样品应为已报废状态
        SampleListPage(InCMS_page).assert_sample_status(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None), "5"
        )
        # 样品已报废，清除缓存中的样品名称
        request.config.cache.set("sample_name", None)
        logger.info("==================== test_sample_list08 over =======================")

    @allure.title("批量登记样品")
    @pytest.mark.order(41)
    def test_batch_register_sample(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_batch_register_sample started ====================")
        data = SampleListData.get_data()
        project_name = request.config.cache.get("compound_sequence_project_name", None)
        logger.info(f"cache.get('compound_sequence_project_name') = {project_name}")

        sample_page = SampleListPage(InCMS_page)
        sample_page.enter_sample_list_page()
        sample_page.wait_loading()

        batch_import_page = BatchImportPage(InCMS_page)
        file_path = batch_import_page.generate_sample_excel(
            project_name, data.sample_name, data.sample_form, data.batch_current_amount, data.sample_tube_type
        )
        batch_import_page.register_samples(file_path)
        sample_id = batch_import_page.assert_sample_exists(data.sample_name)
        logger.info(f"样品已登记成功，样品ID: {sample_id}")
        logger.info("==================== test_batch_register_sample passed ====================")




