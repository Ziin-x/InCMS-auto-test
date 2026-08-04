import time
from locator.material_view import MaterialViewLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param

import allure


# 物质详情页
class MaterialViewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    # 获取指定模块的指定字段名称所对应的值使用，模块名 -> Locator 的映射
    module_locator_map = {
        '基本信息': MaterialViewLocator.basic_info_module_field,
        '物化信息': MaterialViewLocator.physicochemical_info_module_field,
        # ... 其他模块
    }

    # 获取所有模块的所有字段的值
    modules_fields_map = {
        '基本信息':MaterialViewLocator.basic_info_module_fields,
        '物化信息':MaterialViewLocator.physicochemical_info_module_fields,
        # ... 其他模块
    }

#——————物质详情页——————
    @allure.step("获取物质详情页字段信息")
    def get_material_view_fields_info(self):
        """
        获取物质详情页所有模块的字段信息
        返回: {模块名: {字段名: 字段值, ...}, ...}
        """
        self.wait_for(MaterialViewLocator.loading_ele, 'hidden',timeout=60000)
        frame = self.get_frame(MaterialViewLocator.material_view_frame)
        first_view_locator = frame.frame.locator(MaterialViewLocator.module_title).first
        frame.wait_for(first_view_locator,'visible',timeout=5000)

        material_view_info = {}
        # 1. 获取当前物质详情页的所有模块名称
        module_name_list = frame.find(MaterialViewLocator.module_title).all_inner_texts()
        for module_name in module_name_list:
            with allure.step(f"检查模块: {module_name}"):
                # 获取对应模块的 Locator，找不到则跳过
                locator = self.modules_fields_map.get(module_name)
                if not locator:
                    allure.attach(f"模块 [{module_name}] 未配置对应的 Locator", "警告")
                    continue
                # 2. 获取该模块下所有字段名（非 label 的 td）
                field_name_elements = frame.find(locator)
                field_count = field_name_elements.count()
                module_fields = {}
                for i in range(field_count):
                    field_name = field_name_elements.nth(i).inner_text().strip()
                    # 跳过空字段名
                    if not field_name:
                        continue
                    with allure.step(f"获取字段: {field_name}"):
                        # 3. 获取下一个 td（值所在的 td）
                        value_td_ele = field_name_elements.nth(i).locator('xpath=following-sibling::td[1]')
                        # 如果值 td 不存在，跳过
                        if value_td_ele.count() == 0:
                            allure.attach(f"字段 [{field_name}] 未找到对应的值", "警告")
                            continue
                        # 4. 获取元素
                        field_value = frame.get_text(value_td_ele)
                        module_fields[field_name] = field_value
                        # 附加到 Allure 报告
                        allure.attach(f"值: {field_value}",name=f"{field_name}")
                # 5. 将模块字段存入结果
                material_view_info[module_name] = module_fields
                # 附加模块完整信息到报告
                allure.attach(
                    str(module_fields),
                    name=f"{module_name} 完整字段",
                    attachment_type=allure.attachment_type.JSON
                )
        return material_view_info

    @allure.step("检查物质详情页字段信息")
    def check_material_view_fields_info(self, check_fields_dict):
        """
        检查物质详情页各模块字段信息
        """
        self.wait_for(MaterialViewLocator.loading_ele, 'hidden')
        frame = self.get_frame(MaterialViewLocator.material_view_frame)
        for module_name, fields in check_fields_dict.items():
            with allure.step(f"检查模块: {module_name}"):
                # 获取对应 Locator，找不到则跳过或使用默认
                locator = self.module_locator_map.get(module_name)
                if not locator:
                    allure.attach(f"模块 [{module_name}] 未配置对应的 Locator", "警告")
                    continue
                for field_name, expected_value in fields.items():
                    with allure.step(f"检查字段 [{field_name}]: 期望='{expected_value}'"):
                        # 获取实际值
                        actual_value = frame.get_text(load_ele_param(locator, field_name))
                        # 断言
                        logger.info(f"[{module_name}] [{field_name}] 期望={expected_value}, 实际={actual_value}")
                        assert actual_value == expected_value, (
                            f"[{module_name}] -> [{field_name}] 校验失败!\n"
                            f"  期望: {expected_value}\n"
                            f"  实际: {actual_value}"
                        )


    @allure.step("获取自定义字段值")
    def get_custom_field_value(self, field_name: str) -> str:
        """
        获取自定义字段的值
        :param field_name: 自定义字段名称
        :return: 字段值
        """
        locator = load_ele_param(MaterialViewLocator.custom_field_value, field_name)
        return self.get_text(locator)

#——————数据更新——————
class DataUp(BasePage):
    # 数据更新，获取指定模块的指定字段名称所对应的值使用，模块名 -> Locator 的映射
    module_locator_map = {
        '基本信息': MaterialViewLocator.data_up_basic_info_field,
        '物化信息': MaterialViewLocator.data_up_physicochemical_info_field,
        # ... 其他模块
    }

    def __init__(self, page):
        super().__init__(page)

    @allure.step("化合物单个数据更新")
    def compound_single_data_up(self, modules_info=None, edit_all_batch=False):
        """
        化合物单个数据更新
        :param modules_info: 模块信息，dict格式 {模块名: {字段名: 值, ...}, ...}
        :param edit_all_batch: 有同批次数据，是否更改其他批次，默认不更改其他批次
        """
        self.wait_for(MaterialViewLocator.loading_ele, 'hidden')
        # 1.点击数据更新按钮
        with allure.step("1.点击数据更新按钮"):
            self.click(MaterialViewLocator.data_up_btn)
        # 2.编辑模块信息
        if modules_info is not None:
            with allure.step("2.编辑模块信息"):
                self.modules_info_fill(modules_info)
        # 3.提交更新
        with allure.step("3.提交数据更新"):
            self.click(MaterialViewLocator.submit_data_up_btn)
        # 4.如果有同批次数据，进行数据更新会有批次确认弹层
        if self.is_visible(MaterialViewLocator.data_up_edit_notion):
            if edit_all_batch:
                self.click(load_ele_param(MaterialViewLocator.data_up_edit_notion_label,1))
            else:
                self.click(load_ele_param(MaterialViewLocator.data_up_edit_notion_label,2))
        # 5.等待提交更新按钮消失
        with allure.step("5.等待提交关系按钮消失"):
            #设置的60s的等待，因为数据更新有的时候特别慢
            self.wait_for(MaterialViewLocator.submit_data_up_btn,'hidden',timeout=1200000)
            self.wait_for(MaterialViewLocator.loading_ele,'hidden')

    @allure.step("数据更新填写模块信息")
    def modules_info_fill(self, module_info_dict):
        """
        根据 module_info_dict 填写各模块的指定字段
        :param module_info_dict: {模块名: {字段名: 字段值, ...}, ...}
        """
        # 等待加载元素隐藏
        self.wait_for(MaterialViewLocator.loading_ele, 'hidden')
        # 获取 iframe
        frame = self.get_frame(MaterialViewLocator.data_up_frame)
        for module_name, fields_dict in module_info_dict.items():
            locator = self.module_locator_map.get(module_name)
            # 1. 滑动至模块，确保模块在视图内
            module_name_locator = frame.frame.locator(load_ele_param(MaterialViewLocator.data_up_module_name,module_name)).last
            frame.scroll_to_element(module_name_locator)
            # 2. 遍历该模块下的字段进行填写
            for field_name, field_value in fields_dict.items():
                with allure.step(f"填写{module_name}模块下的字段 [{field_name}]: {field_value}"):
                    # 3. 定位字段输入框（基于之前的 XPath 结构）
                    # 字段名 td + 值 td 里的 input
                    frame.fill(load_ele_param(locator,field_name),field_value)






