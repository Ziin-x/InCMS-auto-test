import re
from locator.InCMS import InCMSLocator
from locator.visualization import VisualizationLocator
from object.basepage import BasePage
from utils.load_ele_param import load_ele_param
from utils.log import logger

import allure


class VisualizationPage(BasePage):
    """数据可视化页面操作"""

    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入数据可视化页面")
    def switch_to_visualization_page(self):
        """导航至数据可视化页面"""
        try:
            self.click(InCMSLocator.visualization, timeout=1000)
            clickable_result = True
        except Exception as e:
            logger.info(f"当前页面未有导航栏元素显示，不可点击，错误原因：{e}")
            clickable_result = False
        if not clickable_result:
            current_url = self.page.url
            base_url = re.match(r'(https?://[^/]+)', current_url).group(1)
            self.page.goto(base_url)
            self.click(InCMSLocator.visualization)
        self.wait_for(VisualizationLocator.visualization_title,'visible')

    @allure.step("可视化图表生成")
    def create_visualization_chart(self, chart_type, project_name, template_name, x_field_name, y_field_name):
        logger.info(f"可视化图表生成开始：chart_type={chart_type}, project={project_name}")
        # 1. 选择图表类型
        self.click(load_ele_param(VisualizationLocator.chart_type, chart_type))
        # 2-3. 选择项目和模板
        self.select_option(VisualizationLocator.project_select, project_name)
        self.select_option(VisualizationLocator.template_select, template_name)
        # 4-5. 设置X轴和Y轴字段
        self.select_option(VisualizationLocator.field_x_combobox, x_field_name)
        self.select_option(VisualizationLocator.field_y_combobox, y_field_name)
        # 6. 点击生成图表
        self.click(VisualizationLocator.generate_chart)
        # 7. 检查canvas元素生成
        self.wait_for(VisualizationLocator.chart_canvas,'visible')
