class VisualizationLocator:
    """数据可视化页面元素定位"""
    #数据可视化 title
    visualization_title = '//*[@class="main-top-title" and contains(.,"数据可视化")]'

    # —————— 图表类型选择 ——————
    # 图表类型选项（按文本筛选，再定位内部img点击选中）
    chart_type = '//*[@class="analysis-type-select "]//span[@class="analysis-item" and contains(.,"{}")]/img'
    #——————图表参数设置——————
    #————数据源————
    # 项目下拉框（id定位）
    project_select = "#project"
    # 模板下拉框（id定位）
    template_select = "#template"
    #项目选项
    project_select_option = '//*[@id="project"]/option[contains(.,"{}")]'
    #项目模板选项
    template_select_option = '//*[@id="template"]/option[contains(.,"{}")]'
    #————坐标————
    # 字段combobox（用于X轴/Y轴字段选择，使用时按索引定位）
    field_x_combobox = '//*[@class="field-select number-field x-axis"]'
    # Y轴select
    field_y_combobox = '//*[@class="field-select number-field y-axis"]'

    # —————— 操作按钮 ——————
    # 生成图表按钮
    generate_chart = ("role", "button", "生成图表")

    #canvas 元素
    chart_canvas = '//*[@id="main"]//canvas'
