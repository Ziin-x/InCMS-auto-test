from locator.InCMS import InCMSLocator
from locator.mine.mine_registration import MineRegistrationLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure
from playwright.sync_api import expect


class MineRegistrationPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

    @allure.step("进入我的注册页面")
    def enter_mine_registration_page(self):
        try:
            self.wait_for(MineRegistrationLocator.mine_registration_title,'visible',timeout=5000)
            current_page= True
            self.reload()
        except Exception as e:
            logger.info(f'当前不处于我注册的页面，错误原因{str(e)},即将跳转至我注册的页')
            current_page = False
        if not current_page:
            if self.is_visible(InCMSLocator.mine_register):
                self.click(InCMSLocator.mine_register)
            else:
                self.click(InCMSLocator.mine)
                self.click(InCMSLocator.mine_register)

    @allure.step("获取注册编号")
    def get_registration_number(self,project_name):
        project_loc = load_ele_param(MineRegistrationLocator.mine_registration_number,project_name)
        return self.get_text(project_loc)

    @allure.step("获取批号")
    def get_batch_number(self,project_name):
        project_loc = load_ele_param(MineRegistrationLocator.batch_number,project_name)
        return self.get_text(project_loc)

    @allure.step("断言注册编号和批号是否与设置一致")
    def assert_registration_code_and_batch_number(self,registration_code,registration_code_setting,batch_number,batch_number_setting):
        logger.info("开始断言断言注册编号和批号是否与设置一致")
        try:
            if (registration_code_setting.split("-")[0]+registration_code_setting.split("-")[2] == registration_code.split("-")[0]+registration_code.split("-")[2]
                    and batch_number_setting.split("-")[1] == batch_number.split("-")[1]):
                logger.info("注册编号和批号一致")
                return True
            else:
                logger.info("注册编号和批号不一致")
                return False
        except Exception as e:
            logger.error(f"断言失败，请检查，错误：{e}")
            raise

    @allure.step("我注册的页最新注册的数据落入第一行")
    def check_mine_register_new_data(self,batch_number):
        self.enter_mine_registration_page()
        try:
            self.wait_for(load_ele_param(MineRegistrationLocator.table_register_first_row,batch_number),'visible')
        except AssertionError as e:
            logger.error(f'注册失败,注册的物质未落入我的页面，批号{batch_number}，错误原因{str(e)}')
            raise

    @allure.step("获取表头-序号")
    def get_table_header_index(self):
        # th_count = self.page.locator(MineRegistrationLocator.register_table_header).count()
        self.wait_for(load_ele_param(MineRegistrationLocator.register_table_row_info, 1, 1), 'visible')
        header_map = {}
        th_elements = self.page.locator(MineRegistrationLocator.register_table_header).all()
        for index, th in enumerate(th_elements):
            # 获取表头文本，去除空白字符
            text = th.inner_text()
            text = text.strip()
            if text:  # 忽略空表头
                index_num = index + 1
                header_map[text] = index_num
        return header_map

    @allure.step("断言表格中第几行第几列包含元素")
    def check_row_info_assert(self, row_index: int, column: int, expected: str, is_contain=True):
        """
        :param row_index:行序
        :param column: 列序
        :param expected: 包含文本
        :return:
        """
        locator = self.page.locator(
            load_ele_param(MineRegistrationLocator.register_table_row_info, row_index, column)
        )
        if is_contain:
            # 断言元素包含指定文本（自动等待、重试）
            expect(locator).to_contain_text(expected)
        else:
            # 断言元素不包含指定文本
            expect(locator).not_to_contain_text(expected)
