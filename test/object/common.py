from object.basepage import BasePage
from utils.log import logger

import allure

class CommonPage():
    """通用页面操作，所有用例可直接实例化调用"""

    def __init__(self, page):
        super().__init__(page)

    # 删除排序规则
    delete_sort_rule_btn = ("selector", ".iconfont.icon-Delete.default.square.delete-btn")
    # 排序按键
    sort_btn = ("selector", ".tool-item-button", {"has_text": "排序"})
    # 新增排序规则
    add_sort_rule_btn = ("role", "button", "新增排序规则")
    # 申领时间字段
    request_time_field = ("selector", ".field-label-box", {"has_text": "申领时间"})
    # 倒序
    desc_order = ("selector", ".el-segmented__item-label", {"has_text": "倒序"})

    @staticmethod
    @allure.step("按申领时间倒序排序")
    def sort_by_request_time_desc(page_obj):
        """点击排序 → 新增排序规则 → 选择申领时间 → 倒序"""
        page_obj.click(CommonPage.sort_btn)
        while page_obj.is_visible(CommonPage.delete_sort_rule_btn):
            page_obj.click(CommonPage.delete_sort_rule_btn)
        page_obj.click(CommonPage.add_sort_rule_btn)
        # 精准匹配"申领时间"，排除"取消申领时间"的干扰
        loc = page_obj.page.locator(".field-label-box").filter(has_text="申领时间").filter(has_not_text="取消")
        try:
            logger.debug("尝试点击元素：申领时间")
            loc.click()
            logger.info("点击元素成功：申领时间")
        except Exception as e:
            logger.error(f"点击元素失败：申领时间，错误：{e}")
            raise
        page_obj.click(CommonPage.desc_order)
        logger.info("已设置按申领时间倒序排序")

    @staticmethod
    @allure.step("比对模板与预期字典")
    def compare_template_to_expected(wb, expected_headers, expected_fields):
        """
        将下载的模板 Excel 与预期字典比对
        :param wb: openpyxl Workbook
        :param expected_headers: 预期第1行字段ID列表
        :param expected_fields: 预期第2行字段名列表
        :return: 差异列表
        """
        logger.debug("开始比对模板与预期字典")
        diffs = []
        ws = wb.active

        actual_headers = [ws.cell(row=1, column=c + 1).value for c in range(ws.max_column)]
        while actual_headers and actual_headers[-1] is None:
            actual_headers.pop()
        if actual_headers != expected_headers:
            diffs.append({"row": 1, "expected": expected_headers, "actual": actual_headers})
            logger.error(f"第1行字段ID不一致")

        actual_fields = [ws.cell(row=2, column=c + 1).value for c in range(ws.max_column)]
        while actual_fields and actual_fields[-1] is None:
            actual_fields.pop()
        if actual_fields != expected_fields:
            diffs.append({"row": 2, "expected": expected_fields, "actual": actual_fields})
            logger.error(f"第2行字段名不一致")

        if diffs:
            logger.error(f"模板比对不一致，共 {len(diffs)} 处差异")
        else:
            logger.info("模板与预期字典完全一致")
        return diffs

