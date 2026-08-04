from config.Expection import ElementNotFoundError
from locator.data_center.single_register import SingleRegisterLocator
from locator.InCMS import InCMSLocator
from object.basepage import BasePage
from utils.indraw import IndrawLocator
from utils.load_ele_param import load_ele_param
from utils.log import logger
from typing import Literal

import allure
import pyperclip


class SingleRegisterPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("选择项目与模块")
    def choose_project_and_module(self, project_name, template_name):
        self.click(InCMSLocator.register_button)
        self.click(InCMSLocator.single_register)
        # 选择项目
        self.click_and_input(SingleRegisterLocator.select_project, project_name)
        self.click(load_ele_param(SingleRegisterLocator.project_option, project_name))
        # 选择模板
        self.fill(SingleRegisterLocator.select_template, template_name)
        self.click(load_ele_param(SingleRegisterLocator.template_option, template_name))
        # 点击确认
        self.click(SingleRegisterLocator.confirm)

    def register_info_fill(self,register_type,comp_info,module_filed_dict,statu):
        self.click(InCMSLocator.register_button)

    @allure.step("化合物成分信息填写")
    def compound_composition_info_fill(self, smiles="", isomer_type="", sequence_dict: dict = None):
        """
        化合物成分信息填写
        :param smiles:       SMILES结构式（可选）
        :param isomer_type:  异构体类型（可选）
        :param sequence_dict: 序列字典 {名称: 序列, ...}（可选，smiles和sequence至少有一个）
        """
        # 校验：smiles和sequence至少有一个
        if not smiles and not sequence_dict:
            raise ValueError("smiles和sequence_dict至少需要提供一个")
        # 1. 填写smiles
        if smiles:
            indraw_frame = self.get_frame(SingleRegisterLocator.indraw_frame)
            indraw_frame.frame.page.wait_for_timeout(500)
            pyperclip.copy(smiles)
            indraw_frame.click(SingleRegisterLocator.indraw_canvas)
            indraw_frame.press(SingleRegisterLocator.indraw_canvas, "Control+v")
            indraw_frame.frame.page.wait_for_timeout(500)
        # 2. 异构体类型填写（el-select，需要输入后点选选项）
        if isomer_type:
            self.fill(SingleRegisterLocator.isomer_type, isomer_type)
            self.click(load_ele_param(SingleRegisterLocator.isomer_type_option, isomer_type))
        # 3. 序列填写（如有多个序列，点击"+"添加）
        if sequence_dict:
            sequence_items = list(sequence_dict.items())
            for i, (seq_name, seq_value) in enumerate(sequence_items):
                if i > 0:
                    # 第二个及以上序列，点击"+"添加新行
                    self.click(SingleRegisterLocator.add_sequence_btn)
                index = int(i)+1
                # 填写序列
                self.click(load_ele_param(SingleRegisterLocator.sequence_name_with_index,index))
                self.fill(load_ele_param(SingleRegisterLocator.sequence_name_with_index,index),seq_name)
                self.click(load_ele_param(SingleRegisterLocator.sequence_with_index,index))
                self.fill(load_ele_param(SingleRegisterLocator.sequence_with_index,index),seq_value)
        self.click(SingleRegisterLocator.next_step)
        

    @allure.step("DNA与RNA成分信息填写")
    def dna_and_rna_composition_info_fill(self,sequence_type:Literal['DNA','RNA'],sequence):
        frame = self.get_frame(SingleRegisterLocator.frame)
        sequence_frame = frame.get_frame(SingleRegisterLocator.sequence_iframe)
        # frame.wait_for(SingleRegisterLocator.new_sequence,state='visible')
        sequence_frame.click(SingleRegisterLocator.new_sequence)
        current_type = sequence_frame.get_text(SingleRegisterLocator.sequence_type_selected)
        if current_type != sequence_type:
            sequence_frame.click(load_ele_param(SingleRegisterLocator.sequence_type,sequence_type))
        sequence_frame.fill(SingleRegisterLocator.sequence_input,sequence)
        sequence_frame.click(SingleRegisterLocator.sequence_confirm_btn)
        #等待生成sequence图后点击下一步进入step2
        self.wait_for(SingleRegisterLocator.loading_ele, 'hidden')
        sequence_frame.wait_for(SingleRegisterLocator.draw_sequence,'visible')
        self.click(SingleRegisterLocator.next_step)

    @allure.step("自定义物质成分信息填写")
    def custom_substance_composition_info_fill(self, field_info):
        # field_info限制是一个字典，key为字段名称，value是另一个字典，包含字段类型，字段填写值
        # 先适配文本、数值，单选、多选。
        # 日期以后再说
        for field_name in field_info:
            field_config = field_info[field_name]
            field_type = field_config.get("field_type", "text")  # 字段类型：text/number/select/radio/checkbox
            fill_value = field_config.get("fill_value", "")  # 要填写的值
            # 根据字段类型选择不同的定位器和填写方式
            if field_type in ["text", "number"]:
                # 文本框/数值输入框 - 通过字段名称定位,直接填写
                self.fill(load_ele_param(SingleRegisterLocator.custom_filed,field_name),fill_value)
            elif field_type == "select":
                # 单选下拉框
                locator = (SingleRegisterLocator.custom_field_select[0],
                           SingleRegisterLocator.custom_field_select[1].format(field_name=field_name))
                self.click(locator)
                # 选择对应选项
                option_locator = (SingleRegisterLocator.custom_field_option[0],
                                  SingleRegisterLocator.custom_field_option[1].format(option_value=fill_value))
                self.click(option_locator)

            elif field_type == "checkbox":
                # 多选框 - fill_value 应为列表
                if isinstance(fill_value, list):
                    for option in fill_value:
                        locator = (SingleRegisterLocator.custom_field_checkbox[0],
                                   SingleRegisterLocator.custom_field_checkbox[1].format(field_name=field_name,
                                                                                         option_value=option))
                        self.click(locator)
                else:
                    locator = (SingleRegisterLocator.custom_field_checkbox[0],
                               SingleRegisterLocator.custom_field_checkbox[1].format(field_name=field_name,
                                                                                     option_value=fill_value))
                    self.click(locator)



    @allure.step("物质step2填写模块信息后提交")
    def modules_info_fill(self,module_info_dict,register_statu:Literal['保存为草稿','提交注册']):
        #等待加载元素隐藏
        self.wait_for(SingleRegisterLocator.loading_ele,'hidden')
        #先只填写注册的量和批号字段,如果覆盖模板的所有可填写的字段，需要拿到模板\模块\字段的匹配关系以及字段的类型
        frame = self.get_frame(SingleRegisterLocator.frame)
        for field in module_info_dict:
            frame.fill(load_ele_param(SingleRegisterLocator.basic_module_filed,field),module_info_dict[field])
        self.click(load_ele_param(SingleRegisterLocator.step2_button,register_statu))
        if register_statu == '提交注册':
            self.click(SingleRegisterLocator.confirm)
            #toast等待
            self.wait_for(SingleRegisterLocator.success_toast,'visible')
        else:
            #toast等待
            self.wait_for(SingleRegisterLocator.success_toast,'visible')
        #返回注册状态，可以判断我的这里是否是草稿or注册中（注册中包含注册成功或者注册审核中）
        return register_statu

    # def check_register_statu(self,register_statu):
    #     #1.注册会跳转至我的页面，如果更改设置也有可能不跳转，


    @allure.step("断言项目在单个注册可见")
    def assert_project_visible(self,project_name):
        self.click(InCMSLocator.register_button)
        self.click(InCMSLocator.single_register)
        self.click_and_input(SingleRegisterLocator.select_project, project_name)
        project_loc = load_ele_param(SingleRegisterLocator.project_option, project_name)
        try:
            self.wait_for(project_loc,"visible")
        except Exception as e:
            logger.error(f"断言项目在单个注册不可见，错误：{e}")
            raise ElementNotFoundError(
            f"项目 '{project_name}' 在单个注册的项目列表中不可见，等待超时或元素不存在。原始错误：{e}"
        )

    @allure.step("化合物单个注册物质，填写成分信息")
    def single_register_ingredients(self, project_name):
        self.click(InCMSLocator.register_button)
        self.click(InCMSLocator.single_register)
        self.click_and_input(SingleRegisterLocator.select_project, project_name)
        project_loc = load_ele_param(SingleRegisterLocator.project_option, project_name)
        self.click(project_loc)
        self.click(SingleRegisterLocator.confirm)
        self.indraw()
        self.click(SingleRegisterLocator.next_step)

    @allure.step("indraw编辑")
    def indraw(self):
        # get_frame返回的是baseframe实例
        frame = self.get_frame(IndrawLocator.indraw_iframe)
        frame.frame.page.wait_for_timeout(1000)
        frame.click(IndrawLocator.benzene_class)
        frame.click(IndrawLocator.benzene)
        frame.click_canvas(IndrawLocator.draw_benzene)

    @allure.step("单个注册物质，填写批号，当存在预设批号时，不填写")
    def single_register_batch_member(self, batch_member):
        frame = self.get_frame(SingleRegisterLocator.frame)
        batch_member_value = frame.get_text(SingleRegisterLocator.batch_number)
        if not batch_member_value:
            frame.fill(SingleRegisterLocator.batch_number, batch_member)
            # 如果没有预设批号，批号为空，填入并返回yaml记录的数据
            return batch_member
        # 如果有预设批号，不作调整，读取后直接返回
        return batch_member_value

    @allure.step("单个注册物质，填写注册的量")
    def register_material_amount(self,register_amount):
        frame = self.get_frame(SingleRegisterLocator.frame)
        frame.fill(SingleRegisterLocator.register_amount, register_amount)


    @allure.step("确认注册")
    def confirm_register(self):
        self.click(SingleRegisterLocator.submit_register)
        self.click(SingleRegisterLocator.confirm)

    @allure.step("断言CMS注册的SMILES是否正确")
    def assert_cms_smiles(self, expected_smiles="C1C=CC=CC=1"):
        """点击下一步，读取SMILES值，断言与预期一致"""
        self.wait_for(SingleRegisterLocator.loading_ele, 'hidden')
        self.click(SingleRegisterLocator.next_step)
        self.wait_for(SingleRegisterLocator.loading_ele, 'hidden')
        actual = self.get_text(SingleRegisterLocator.smiles_value)
        assert actual == expected_smiles, f"SMILES不匹配，期望={expected_smiles}，实际={actual}"
        logger.info(f"SMILES验证通过: {actual}")

    @allure.step("断言注册物质时的模块与模板是否一致")
    def assert_register_material_module(self, add_module_list: list):
        frame = self.get_frame(SingleRegisterLocator.frame)
        try:
            logger.info("开始检查页面中的模块是否与模板一致")
            for i in add_module_list:
                add_module_loc = load_ele_param(SingleRegisterLocator.module, i)
                frame.wait_for(add_module_loc,"visible")
                logger.info(f"检查添加的模块：{i}存在")
            logger.info("检查页面中的模块是否与模板一致完成")
        except Exception as e:
            logger.error(f"页面中的模块与模板不一致，请检查，错误：{e}")
            raise

    @allure.step("断言注册物质时模块的参数是否与模版一致")
    def assert_register_material_parameter(self,parameter: str):
        frame = self.get_frame(SingleRegisterLocator.frame)
        try:
            logger.info("开始检查页面中的参数是否与模板一致")
            parameter_loc = load_ele_param(SingleRegisterLocator.parameter, parameter)
            frame.wait_for(parameter_loc,"visible")
            logger.info(f"检查添加的参数：{parameter}存在")
        except Exception as e:
            logger.error(f"页面中的参数与模板不一致，请检查，错误：{e}")
            raise


