from config.setting import SingleRegistrationSubstanceAPI
from data.pydantic.data_center.single_register import SingleRegisterData
from data.pydantic.data_center.single_register_project import \
    SingleRegisterProjectData
from data.pydantic.group_management.template_management import \
    TemplateManagementData
from object.data_center.single_register import SingleRegisterPage
from object.group_management.review_and_reminder import \
    ReviewAndReminderPage
from object.mine.mine_registration import MineRegistrationPage
from object.mine.my_approval.data_register_approval_page import \
    DataRegisterApprovalPage
from utils.auto_generated_data import (generate_batch_number,
                                            generate_dna, generate_rna)
from utils.log import logger

import allure
import pytest


@allure.epic("数据中心")
@allure.feature("单个注册")
class TestSingleRegister:

    single_register_data = SingleRegisterData.get_data()
    single_register_project_data = SingleRegisterProjectData.get_data()
    parameter_name = TemplateManagementData.get_data().parameter.parameter_name

    all_project_template_dict = single_register_project_data.all_project_template_dict
    compound_composition_info = single_register_project_data.compound_composition_info.model_dump()

    project_name = single_register_project_data.project_name
    project_template_dict = all_project_template_dict[project_name]

    review_type = single_register_project_data.review_type
    approval_user = single_register_project_data.approval_user



    @allure.story("无审批状态")
    @allure.title("注册化合物/序列")
    @pytest.mark.order(28)
    def test_single_register01(self, InCMS_page, request:pytest.FixtureRequest):
        logger.info("==================== test_single_register01 started ====================")
        # 注册物质
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.single_register_ingredients(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None))
        # 断言实际创建时的模块是否与case1创建的模板中添加的模块一致
        single_register_page.assert_register_material_module(self.single_register_data.add_module_list)
        single_register_page.assert_register_material_parameter(self.parameter_name)
        single_register_page.single_register_batch_member(self.single_register_data.batch_number)
        single_register_page.register_material_amount(self.single_register_data.register_amount)
        single_register_page.page.wait_for_timeout(5000)
        single_register_page.wait_according_to_the_interface(
            SingleRegistrationSubstanceAPI,
            single_register_page.confirm_register
        )

    @allure.story("无审批状态")
    @allure.title("注册DNA物质")
    @pytest.mark.order(29)
    def test_single_register02(self, InCMS_page):
        logger.info("==================== test_single_register02 started ====================")
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name,self.project_template_dict['DNA'][0])
        rna_sequence = generate_dna()
        single_register_page.dna_and_rna_composition_info_fill('DNA',rna_sequence)
        #自动生成批号&注册的量
        batch_number = generate_batch_number('DNA')
        module_info = {
            '批号':batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info,'提交注册')
        mine_register_page = MineRegistrationPage(InCMS_page)
        mine_register_page.check_mine_register_new_data(batch_number)

    @allure.story("无审批状态")
    @allure.title("注册RNA物质")
    @pytest.mark.order(30)
    def test_single_register03(self, InCMS_page):
        logger.info("==================== test_single_register03 started ====================")
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name,self.project_template_dict['RNA'][0])
        rna_sequence = generate_rna()
        single_register_page.dna_and_rna_composition_info_fill('RNA', rna_sequence)
        # 自动生成批号&注册的量
        batch_number = generate_batch_number('RNA')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '提交注册')
        mine_register_page = MineRegistrationPage(InCMS_page)
        mine_register_page.check_mine_register_new_data(batch_number)

    @allure.story("无审批状态")
    @allure.title("注册自定义物质")
    @pytest.mark.order(31)
    def test_single_register04(self, InCMS_page):
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name,self.project_template_dict['自定义物质'][0])
        # 自动生成批号&注册的量
        batch_number = generate_batch_number('RNA')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '提交注册')
        mine_register_page = MineRegistrationPage(InCMS_page)
        mine_register_page.check_mine_register_new_data(batch_number)

    @allure.title("注册混合物/配方")
    @pytest.mark.order(32)
    def test_single_register05(self, InCMS_page, request: pytest.FixtureRequest):
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name,self.project_template_dict['混合物/配方'][0])
        # 自动生成批号&注册的量
        batch_number = generate_batch_number('混合物/配方')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '提交注册')
        mine_register_page = MineRegistrationPage(InCMS_page)
        mine_register_page.check_mine_register_new_data(batch_number)

    @allure.title("保存为草稿状态检查")
    @pytest.mark.order(33)
    def test_single_register06(self, InCMS_page, request: pytest.FixtureRequest):
        # 1.检查物质所属项目是否有数据更新审核，如果有审核，则取消审核
        approval_page = ReviewAndReminderPage(InCMS_page)
        approval_page.clear_approval_setting(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None), self.review_type)
        # 2.注册化合物/序列物质
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name,self.project_template_dict['化合物/序列'][0])
        #3.化合物填写成分信息
        single_register_page.compound_composition_info_fill(**self.compound_composition_info)
        #4.化合物填写其他模块
        batch_number = generate_batch_number('化合物/序列')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '保存为草稿')
        #和设置有关，默认设置会自动跳转到我的
        #5.我的
        mine_register_page = MineRegistrationPage(InCMS_page)
        table_head_dict = mine_register_page.get_table_header_index()
        mine_register_page.check_row_info_assert(1,table_head_dict['注册编号(批号)'],batch_number)
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], '暂无注册编号')
        mine_register_page.check_row_info_assert(1,table_head_dict['状态'],'草稿')

    @allure.title("数据注册有审核，审核拒绝")
    @pytest.mark.order(38)
    def test_single_register_with_approval_01(self, InCMS_page, request: pytest.FixtureRequest):
        # 1.设置项目数据注册审核，审核节点只有一个人
        set_approval_page = ReviewAndReminderPage(InCMS_page)
        set_approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None), self.approval_user, self.review_type)
        # 2.进行化合物注册
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name, self.project_template_dict['化合物/序列'][0])
        # 3.化合物填写成分信息
        single_register_page.compound_composition_info_fill(**self.compound_composition_info)
        # 4.化合物填写其他模块
        batch_number = generate_batch_number('化合物/序列')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '提交注册')
        # 5.检查我的-此物质为待审核状态
        mine_register_page = MineRegistrationPage(InCMS_page)
        table_head_dict = mine_register_page.get_table_header_index()
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], batch_number)
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], '暂无注册编号')
        mine_register_page.check_row_info_assert(1, table_head_dict['状态'], '已注册待审核')
        # 6.我的审核-数据注册审核，审核人有此条数据
        my_approval_register_page = DataRegisterApprovalPage(InCMS_page)
        my_approval_register_page.switch_to_data_approval_page()
        my_approval_register_page.check_approval_list(1, batch_number)
        # 7.拒绝审核
        my_approval_register_page.single_row_approval(1, False)
        # 8.切换至我的-此物质为审批拒绝状态，无注册编号
        mine_register_page.enter_mine_registration_page()
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], batch_number)
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], '暂无注册编号')
        mine_register_page.check_row_info_assert(1, table_head_dict['状态'], '审核未通过')



    @allure.title("数据注册有审核，审核通过")
    @pytest.mark.order(39)
    def test_single_register_with_approval_02(self, InCMS_page, request: pytest.FixtureRequest):
        # 1.设置项目数据注册审核，审核节点只有一个人
        set_approval_page = ReviewAndReminderPage(InCMS_page)
        set_approval_page.set_approval_user(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None), self.approval_user, self.review_type)
        # 2.进行化合物注册
        single_register_page = SingleRegisterPage(InCMS_page)
        single_register_page.choose_project_and_module(self.project_name, self.project_template_dict['化合物/序列'][0])
        # 3.化合物填写成分信息
        single_register_page.compound_composition_info_fill(**self.compound_composition_info)
        # 4.化合物填写其他模块
        batch_number = generate_batch_number('化合物/序列')
        module_info = {
            '批号': batch_number,
            '注册的量': '100'
        }
        single_register_page.modules_info_fill(module_info, '提交注册')
        # 5.检查我的-此物质为待审核状态
        mine_register_page = MineRegistrationPage(InCMS_page)
        table_head_dict = mine_register_page.get_table_header_index()
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], batch_number)
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], '暂无注册编号')
        mine_register_page.check_row_info_assert(1, table_head_dict['状态'], '已注册待审核')
        # 6.我的审核-数据注册审核，审核人有此条数据
        my_approval_register_page = DataRegisterApprovalPage(InCMS_page)
        my_approval_register_page.switch_to_data_approval_page()
        my_approval_register_page.check_approval_list(1, batch_number)
        # 7.通过审核
        my_approval_register_page.single_row_approval(1, True)
        # 8.切换至我的-此物质为审批状态，有注册编号
        mine_register_page.enter_mine_registration_page()
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], batch_number)
        mine_register_page.check_row_info_assert(1, table_head_dict['注册编号(批号)'], '暂无注册编号',is_contain=False)
        mine_register_page.check_row_info_assert(1, table_head_dict['状态'], '审核通过')



    @allure.title("进入我的注册界面，获取注册编号和批号，断言群内管理-编号规则模块")
    @pytest.mark.order(40)
    def test_assert_code_rule0102(self, InCMS_page, request:pytest.FixtureRequest):
        # 进入我的注册界面
        mine_registration_page = MineRegistrationPage(InCMS_page)
        mine_registration_page.enter_mine_registration_page()
        # 根据项目名称获取注册编号和批号
        registration_code = mine_registration_page.get_registration_number(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None))
        batch_number = mine_registration_page.get_batch_number(
            logger.info(f"cache.get('compound_sequence_project_name') 已调用")
            request.config.cache.get("compound_sequence_project_name", None))
        # 断言断言注册编号和批号是否与设置一致
        assert mine_registration_page.assert_registration_code_and_batch_number(
            registration_code,
            logger.info(f"cache.get('code_preview_text') 已调用")
            request.config.cache.get("code_preview_text", None),
            batch_number,
            logger.info(f"cache.get('batch_preview_text') 已调用")
            request.config.cache.get("batch_preview_text", None)
        ), (f"注册编号或批号与设置不一致。注册编号: {registration_code}, 批号: {batch_number}, "
            logger.info(f"cache.get('code_preview_text') 已调用")
            f"预设编号: {request.config.cache.get('code_preview_text', None)}, "
            logger.info(f"cache.get('batch_preview_text') 已调用")
            f"预设批号: {request.config.cache.get('batch_preview_text', None)}")



