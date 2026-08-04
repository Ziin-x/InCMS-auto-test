import pytest
from playwright.sync_api import sync_playwright

from config.environments_pydantic import Environment
from data.pydantic.plug_pydantic import PlugPageData
from object.fixture_object.login_page_object import LoginPageObject
from object.fixture_object.plug_page_object import PlugPageObject
from utils.log import logger

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]  # 启动时最大化
        )
        yield browser
        browser.close()

env = Environment.get_data()
@pytest.fixture(scope="function")
def login_plug_page(browser):
    logger.info("==================== login before testcase ====================")
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPageObject(page)
    login_page.login_plug(env)
    yield login_page.page
    context.close()

plug_data = PlugPageData.get_data()
@pytest.fixture(scope="function")
def InCMS_page(login_plug_page):
    plug_page = PlugPageObject(login_plug_page)
    plug_page.page.wait_for_load_state('networkidle')
    plug_page.choose_product(plug_data.cms)
    return plug_page.page

@pytest.fixture(scope="function")
def InELN_page(login_plug_page):
    plug_page = PlugPageObject(login_plug_page)
    plug_page.page.wait_for_load_state('networkidle')
    plug_page.choose_product(plug_data.eln)
    return plug_page.page

def pytest_generate_tests(metafunc):
    # 检查测试函数是否需要 project_name 参数
    if "project_name" in metafunc.fixturenames:
        # 从 cache 中读取多个项目名
        cache = metafunc.config.cache
        project_name_list = []
        for key in ["compound_sequence_project_name", "mixture_formula_project_name",
                    "custom_compound_project_name", "DNA_project_name", "RNA_project_name"]:
            name = cache.get(key, None)
            if name is not None:
                project_name_list.append(name)
            else:
                logger.error(f"cache中缺少数据: {key}")

        if not project_name_list:
            raise ValueError("没有记录到项目名称")
        # 动态参数化 project_name
        metafunc.parametrize("project_name", project_name_list)