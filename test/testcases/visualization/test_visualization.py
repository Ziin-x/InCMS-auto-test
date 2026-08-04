from data.pydantic.visualization.visualization import VisualizationData
from object.visualization_page import VisualizationPage

import allure
import pytest


@allure.epic("数据可视化")
class TestVisualization:
    data = VisualizationData.get_data()
    chart_type = data.chart_type
    project_name = data.project_name
    template_name = data.template_name
    x_field = data.x_field
    y_field = data.y_field

    @pytest.fixture(scope="function")
    def load_visualization_page(self, InCMS_page):
        visualization_page = VisualizationPage(InCMS_page)
        visualization_page.switch_to_visualization_page()
        return visualization_page.page

    @allure.title("数据可视化生成图表")
    @pytest.mark.order(42)
    def test_visualization01(self, load_visualization_page, request: pytest.FixtureRequest):
        visualization_page = VisualizationPage(load_visualization_page)
        visualization_page.create_visualization_chart(self.chart_type,self.project_name,self.template_name,self.x_field,self.y_field)

