class DataCenterLocator:
    # 更多操作按钮（三点菜单，区别于 icon-DotsEllipsis 图标）
    more_button = ("selector", "button.el-button.more-button")
    # 全部导出Excel
    export_all_excel = ("selector", ".el-dropdown-menu__item", {"has_text": "全部导出Excel"})
    # 全部导出SDF
    export_all_sdf = ("selector", ".el-dropdown-menu__item", {"has_text": "全部导出SDF"})
    # 下载框
    floating_inbox = ("selector", ".floating-inbox")
    # 下载任务结果按钮
    floating_inbox_download = ("selector", ".floating-inbox-action-button")
    # 全部数据
    all_data_tab = ("selector", "li.view-li:visible", {"has_text": "全部数据"})
    # 按物质分组
    material_group_tab = ("selector", "li.view-li:visible", {"has_text": "按物质分组"})
