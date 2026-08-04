from config.setting import SampleListAPI, SampleRegisterAPI, SampleRequestAPI, SampleRequestDataAPI
from locator.InCMS import InCMSLocator
from locator.sample_center.sample_list import SampleListLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure


class SampleListPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("进入样本列表页面")
    def enter_sample_list_page(self):
        self.ensure_dropdown_expanded(InCMSLocator.sample_center, InCMSLocator.sample_list)
        self.click(InCMSLocator.sample_list)

    def wait_loading(self):
        self.wait_for(SampleListLocator.wait_loading, "visible",timeout=20000)
        self.page.wait_for_timeout(2000)

    @allure.step("单个登记样品")
    def register_sample(self, sample_name, project_name, current_amount):
        self.click(SampleListLocator.sample_register)
        self.fill(SampleListLocator.sample_name, sample_name)
        self.click(SampleListLocator.project)
        project_option_loc = load_ele_param(SampleListLocator.project_option, project_name)
        self.click(project_option_loc)
        self.fill(SampleListLocator.current_amount, current_amount)
        self.wait_according_to_the_interface(
            SampleRegisterAPI,
            lambda: self.click(SampleListLocator.submit_register)
        )

    @allure.step("进入申领弹窗")
    def enter_request_dialog(self):
        """选中最新样品并点击申领按钮，打开申领弹窗"""
        self.click_canvas(SampleListLocator.check_newest_sample)
        self.click_canvas(SampleListLocator.check_newest_sample)
        self.page.wait_for_timeout(500)
        if not self.is_visible(SampleListLocator.sample_request):
            logger.error("样品状态异常，无法申领：申领按钮不可见")
            raise RuntimeError("样品状态异常，无法申领：申领按钮不可见")
        self.click(SampleListLocator.sample_request)

    @allure.step("选择领样方式-立即领用")
    def select_immediate_request(self):
        """在申领弹窗中点击立即领用"""
        self.click(SampleListLocator.sample_request_immediately)

    @allure.step("选择领样方式-按量")
    def select_quantity_request(self):
        """在申领弹窗中点击按量，切换为加入领样车模式"""
        self.click(SampleListLocator.quantity_method_btn)

    @allure.step("确认立即申领")
    def confirm_immediate_request(self):
        """勾选全部样品并点击立即申领，等待接口返回"""
        self.click_canvas(SampleListLocator.check_all_sample)
        self.wait_according_to_the_interface(
            SampleRequestAPI,
            lambda: self.click(SampleListLocator.sample_request_now)
        )

    @allure.step("加入领样车")
    def add_to_cart(self):
        """点击加入领样车按钮，将样品加入领样车"""
        self.click(SampleListLocator.add_to_cart_btn)
        logger.info("已将样品加入领样车")

    @allure.step("样品加入领样车")
    def sample_add_to_cart(self):
        """完整流程：选中样品 → 打开申领弹窗 → 选择按量 → 加入领样车"""
        self.enter_request_dialog()
        self.select_quantity_request()
        self.add_to_cart()

    @allure.step("样品申领")
    def sample_request(self):
        self.enter_request_dialog()
        self.select_immediate_request()
        self.page.wait_for_timeout(5000)
        self.confirm_immediate_request()

    @allure.step("样品报废")
    def sample_scrap(self):
        # 需要先点一下聚焦canvas
        self.click_canvas(SampleListLocator.check_newest_sample)
        self.click_canvas(SampleListLocator.check_newest_sample)
        self.page.wait_for_timeout(500)
        if not self.is_visible(SampleListLocator.sample_scrap):
            logger.error("样品状态异常，无法报废：报废按钮不可见")
            raise RuntimeError("样品状态异常，无法报废：报废按钮不可见")
        self.click(SampleListLocator.sample_scrap)
        self.fill(SampleListLocator.reason_input, "auto_test")
        self.click(SampleListLocator.confirm_btn)

    def _get_sample_list(self):
        """调用样品列表接口，返回 dataList"""
        self.page.wait_for_timeout(3000)
        logger.debug(f"调用接口{SampleListAPI}返回样本列表")
        payload = {}
        response = self.page.request.get(SampleListAPI, params=payload)
        if response.status != 200:
            logger.error(f"获取样本列表失败，响应状态码：{response.status}，响应内容：{response.text()}")
            raise RuntimeError(f"获取样本列表失败，响应状态码：{response.status}，响应内容：{response.text()}")
        try:
            return response.json()['data']['data']['dataList']
        except (KeyError, TypeError) as e:
            logger.error(f"解析样本列表响应失败。原始错误：{e}，响应内容：{response.text()}")
            raise RuntimeError(f"解析样本列表响应失败。原始错误：{e}，响应内容：{response.text()}")

    @allure.step("通过样品名称获取样品ID")
    def get_sample_id(self, sample_name: str):
        data_list = self._get_sample_list()
        for item in data_list:
            if item['sampleName'] == sample_name:
                return item['sampleBarcode']
        raise RuntimeError(f"样品 [{sample_name}] 在样品列表中不存在")

    @allure.step("根据样品名称获取样品状态")
    def get_sample_status(self, sample_name: str) -> str:
        """
        调用样品列表接口，按 sampleName 查找样品状态
        :param sample_name: 样品名称
        :return: sampleStatus 值（2=在库, 5=已报废, 8=报废审批中），未找到返回 None
        """
        data_list = self._get_sample_list()
        for item in data_list:
            if item['sampleName'] == sample_name:
                status = item['sampleStatus']
                logger.info(f"样品 [{sample_name}] 状态为 sampleStatus={status}")
                return status
        logger.warning(f"样品 [{sample_name}] 不存在于样品列表中")
        return None

    @allure.step("断言样品状态")
    def assert_sample_status(self, sample_name: str, expected_status: str):
        """
        :param sample_name: 样品名称
        :param expected_status: 期望的 sampleStatus 值，传 None 表示样品应从列表中移除
        """
        status = self.get_sample_status(sample_name)
        logger.info(f"样品 [{sample_name}] 状态: sampleStatus={status}, 期望={expected_status}")
        assert status == expected_status, \
            f"样品 [{sample_name}] 状态不匹配，期望={expected_status}，实际={status}"

    def _get_sample_request_list(self):
        """调用申领记录接口，返回 dataList"""
        self.page.wait_for_timeout(3000)
        logger.debug(f"调用接口{SampleRequestDataAPI}获取申领记录")
        payload = {"range": "about_me"}
        response = self.page.request.post(SampleRequestDataAPI, multipart=payload)
        if response.status != 200:
            logger.error(f"获取申领记录失败，响应状态码：{response.status}，响应内容：{response.text()}")
            raise RuntimeError(f"获取申领记录失败，响应状态码：{response.status}，响应内容：{response.text()}")
        try:
            return response.json()['data']['data']['dataList']
        except (KeyError, TypeError) as e:
            logger.error(f"解析申领记录响应失败。原始错误：{e}，响应内容：{response.text()}")
            raise RuntimeError(f"解析申领记录响应失败。原始错误：{e}，响应内容：{response.text()}")

    @allure.step("根据样品名称获取申领状态")
    def get_sample_request_status(self, sample_name: str) -> str:
        """
        调用申领记录接口，按样品名称查找申领状态
        :param sample_name: 样品名称（对应接口返回的 sampleName 字段）
        :return: requisitionStatus 值（5=已接收），未找到返回 None
        """
        data_list = self._get_sample_request_list()
        sorted_list = sorted(data_list, key=lambda x: int(x['id']), reverse=True)
        for item in sorted_list:
            if item['sampleName'] == sample_name:
                status = item['requisitionStatus']
                logger.info(f"样品 [{sample_name}] 匹配到的申领记录: {item}")
                logger.info(f"样品 [{sample_name}] 申领状态为 requisitionStatus={status}")
                return status
        logger.error(f"样品 [{sample_name}] 不存在于申领记录中")
        return None

    @allure.step("断言样品申领状态")
    def assert_sample_request_status(self, sample_name: str, expected_status: str):
        """
        :param sample_name: 样品名称
        :param expected_status: 期望的申领状态（5=已接收）
        """
        status = self.get_sample_request_status(sample_name)
        logger.info(f"样品 [{sample_name}] 申领状态: requisitionStatus={status}, 期望={expected_status}")
        assert status == expected_status, \
            f"样品 [{sample_name}] 申领状态不匹配，期望={expected_status}，实际={status}"

    @allure.step("效验申领记录的实际取用量")
    def assert_request_quantity(self, sample_name: str, expected_number: str, expected_unit: str):
        """
        效验申领记录：状态为已接收（5），且实际取用量的 number 和 unitId 与期望一致
        :param sample_name: 样品名称
        :param expected_number: 期望的取用量数值
        :param expected_unit: 期望的取用量单位
        """
        data_list = self._get_sample_request_list()
        sorted_list = sorted(data_list, key=lambda x: int(x['id']), reverse=True)
        # 取第一条匹配的申领记录
        record = None
        for item in sorted_list:
            if item['sampleName'] == sample_name:
                record = item
                break
        if record is None:
            raise RuntimeError(f"样品 [{sample_name}] 不存在于申领记录中")
        # 效验状态
        status = record.get('requisitionStatus')
        logger.info(f"申领状态: requisitionStatus={status}")
        assert str(status) == "5", f"样品 [{sample_name}] 应为已接收(5)，实际为 {status}"
        # 效验实际取用量
        actual = record.get('actualRequisitionQuantityWithUnit')
        if actual:
            number = actual.get('number')
            unit = actual.get('unitId')
            logger.info(f"实际取用量：{number} {unit}，期望：{expected_number} {expected_unit}")
            assert str(number) == str(expected_number), \
                f"取用量不匹配，期望={expected_number}，实际={number}"
            assert str(unit) == str(expected_unit), \
                f"取用单位不匹配，期望={expected_unit}，实际={unit}"
        else:
            raise RuntimeError(f"样品 [{sample_name}] 的申领记录没有实际取用量")

    @allure.step("断言样本ID是否与设置一致")
    def assert_sample_id(self, sample_id, sample_id_setting):
        logger.debug(f"断言样本ID是否与设置一致,样本ID：{sample_id},设置样本ID：{sample_id_setting}")
        if sample_id_setting.split('-')[0] == sample_id.split('-')[0]:
            logger.info(f"样本ID与设置一致")
        else:
            logger.error(f"样本ID与设置不一致")
            raise RuntimeError(f"样本ID与设置不一致")
