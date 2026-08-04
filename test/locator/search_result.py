class SearchResultLocator:
    # —————— 搜索结果表格 ——————
    # 点击搜索结果界面第一个物质（canvas）
    search_results_first = (("selector","div.inform-container .konvajs-content canvas"),(150,53))
    # 搜索结果弹窗中的iframe
    search_result_iframe = ("selector", "div[role='dialog'][aria-label='搜索结果'] iframe")
    # 注册编号列（表头/单元格）
    registration_code_column = '(//td[contains(.,"{}")]//a[@target="_blank"])[last()]'
    # 物质名称列
    material_name_column = ""
    # 批号列
    batch_number_column = ""
    # 项目名称列
    project_name_column = ""
    # 注册状态列
    register_status_column = ""
    # 物质类型列
    material_type_column = ""

    # —————— 表格行操作 ——————
    # 表格行（按注册编号定位）
    table_row = ""
    # 行复选框
    row_checkbox = ""

    # —————— 顶部操作按钮 ——————
    # 导出
    export_button = ""
    # 导出选项（点击导出后的下拉选项）
    export_option = ""
    # 全屏
    full_screen_button = ""
    # 全屏（断言-激活态）
    full_screen_button_assert = ""
    # 筛选
    filter_button = ""
    # 筛选面板
    filter_panel = ""
    # 筛选选项
    filter_option = ""
    # 筛选确认/应用
    filter_confirm = ""
    # 筛选重置
    filter_reset = ""
    # 申领
    claim_button = ""
    # 申领确认
    claim_confirm = ""

    # —————— 分页 ——————
    # 总条数
    total_count = ""
    # 下一页
    next_page = ""
    # 上一页
    prev_page = ""
    # 每页条数下拉
    page_size_select = ""

    # —————— 搜索结果弹窗（iframe内） ——————
    # 搜索结果弹窗中的iframe
    search_result_iframe = ("selector", "div[role='dialog'][aria-label='搜索结果'] iframe")
    # 搜索结果中物质行的链接（参数为批号标识，如 Batch_20260512_018_xxx）
    # 用法: frame.find(load_ele_param(SearchResultLocator.search_result_row, batch_param)).get_by_role("link").click()
    search_result_row = ("role", "row", "{}")

    # —————— 加载/空状态 ——————
    # 加载中
    loading = ""
    # 无数据
    no_data = ""
