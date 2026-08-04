from config.environments_pydantic import Environment
from data.pydantic.sample_center.sample_list import SampleListData
from object.sample_center.sample_cart import SampleCartPage
from object.sample_center.sample_list import SampleListPage

import allure
import pytest

from utils.log import logger


@allure.epic("样品中心")
@allure.feature("领样车")
class TestSampleCart:

    sample_data = SampleListData.get_data()
    # 领用量为登记量的一半
    claim_amount = str(int(int(sample_data.current_amount) / 2))
    receiver = Environment.get_data().username

    @allure.title("领样车按量领用")
    @pytest.mark.order(41)
    def test_sample_cart01(self, InCMS_page, request: pytest.FixtureRequest):
        logger.info("==================== test_sample_cart01 started ====================")
        # 先清空领样车中的残留样品
        sample_cart_page = SampleCartPage(InCMS_page)
        sample_cart_page.enter_sample_cart()
        sample_cart_page.delete_all_sample()
        # 如果缓存中没有样品名称，先登记一个样品
        logger.info(f"cache.get('sample_name') 已调用")
        if request.config.cache.get("sample_name", None) is None:
            sample_list_page = SampleListPage(InCMS_page)
            sample_list_page.enter_sample_list_page()
            sample_list_page.wait_loading()
            sample_name = self.sample_data.sample_name
            sample_list_page.register_sample(
                sample_name,
                logger.info(f"cache.get('compound_sequence_project_name') 已调用")
                request.config.cache.get("compound_sequence_project_name", None),
                self.sample_data.current_amount
            )
            request.config.cache.set("sample_name", sample_name)
            logger.info(f"缓存中无样品名称，已登记样品: {sample_name}")
        # 再进入样品列表，将样品加入领样车
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.enter_sample_list_page()
        sample_list_page.wait_loading()
        sample_list_page.sample_add_to_cart()
        sample_list_page.page.wait_for_timeout(5000)
        # 再进入领样车
        sample_cart_page.enter_sample_cart()
        sample_cart_page.switch_to_quantity_tab()
        sample_cart_page.check_and_fill_claim_amount(self.claim_amount)
        sample_cart_page.choose_receiver(self.receiver)
        sample_cart_page.check_and_claim_sample()
        # 效验申领记录状态和取用量
        sample_list_page = SampleListPage(InCMS_page)
        sample_list_page.assert_request_quantity(
            logger.info(f"cache.get('sample_name') 已调用")
            request.config.cache.get("sample_name", None),
            self.claim_amount,
            "μg"
        )
        logger.info("==================== test_sample_cart01 over =======================")
