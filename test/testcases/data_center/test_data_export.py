from locator.data_center.data_center import DataCenterLocator
from object.data_center.data_center import DataCenterPage
from utils.log import logger

import allure
import pytest


@allure.epic("数据中心")
class TestDataCenterExport:

    _VIEW_CONFIG = {
        "全部数据": DataCenterLocator.all_data_tab,
        "按物质分组": DataCenterLocator.material_group_tab,
    }

    @allure.title("查看{view_mode}并导出为Excel")
    @pytest.mark.order(62)
    @pytest.mark.parametrize("view_mode", [
        pytest.param("全部数据", id="全部数据"),
        pytest.param("按物质分组", id="按物质分组"),
    ])
    def test_export_excel_and_compare(self, InCMS_page, view_mode):
        logger.info(f"==================== test_export_excel_and_compare [{view_mode}] started ====================")
        data_center_page = DataCenterPage(InCMS_page)

        data_center_page.switch_view(self._VIEW_CONFIG[view_mode], view_mode)

        # 获取接口数据（监听接口后刷新页面）
        api_data = data_center_page.get_material_list_from_api()
        # 导出 Excel
        excel_wb = data_center_page.export_all_excel()
        # 比对
        diffs = data_center_page.compare_material_data(excel_wb, api_data)
        assert diffs == [], f"Excel 与接口数据不一致，差异详情: {diffs}"
        logger.info(f"==================== test_export_excel_and_compare [{view_mode}] passed ====================")

    @allure.title("查看{view_mode}并导出为SDF")
    @pytest.mark.order(63)
    @pytest.mark.parametrize("view_mode", [
        pytest.param("全部数据", id="全部数据"),
        pytest.param("按物质分组", id="按物质分组"),
    ])
    def test_export_sdf(self, InCMS_page, view_mode):
        logger.info(f"==================== test_export_sdf [{view_mode}] started ====================")
        data_center_page = DataCenterPage(InCMS_page)

        data_center_page.switch_view(self._VIEW_CONFIG[view_mode], view_mode)

        # 导出 SDF
        data = data_center_page.export_all_sdf()
        assert data is not None and len(data) > 0, "SDF 导出文件为空"
        logger.info(f"==================== test_export_sdf [{view_mode}] passed ====================")
