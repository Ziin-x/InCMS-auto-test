from config.environments_pydantic import Environment
from data.pydantic.eln.eln import ELNData
from object.data_center.single_register import SingleRegisterPage
from object.eln.eln import ELNPage
from utils.log import logger

import allure
import pytest


@allure.epic("ELN")
class TestELN:

    @allure.title("ELN注册到CMS")
    @pytest.mark.order(66)
    def test_create_eln_record(self, InELN_page, request: pytest.FixtureRequest):
        logger.info("==================== test_create_eln_record started ====================")
        data = ELNData.get_data()
        env = Environment.get_data()
        project_name = request.config.cache.get("compound_sequence_project_name", None)
        logger.info(f"cache.get('compound_sequence_project_name') = {project_name}")
        notebook_name = request.config.cache.get("eln_notebook_name", None) or data.notebook_name
        logger.info(f"cache.get('eln_notebook_name') = {notebook_name}")

        eln_page = ELNPage(InELN_page)
        eln_page.create_record(
            notebook_name=notebook_name,
            group_name=env.group_name,
            project_name=project_name
        )
        request.config.cache.set("eln_notebook_name", notebook_name)

        eln_page.add_indraw_module()
        eln_page.add_product()

        eln_page.register_to_cms(env.group_name)
        single_page = SingleRegisterPage(eln_page.page)
        single_page.assert_cms_smiles()

        logger.info("==================== test_create_eln_record passed ====================")
