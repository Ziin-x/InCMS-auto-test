class BatchImportLocator:
    # 批量导入 iframe
    batch_import_frame = ("selector", "iframe")
    # InTable 菜单按钮
    intable_menu_btn = ("selector", ".menu-item-box.intable-icon-menu")
    # 文件菜单
    file_menu_btn = ("selector", ".multilevel-menu-item.intable-icon-sub-document")
    # 导入 Excel input
    import_excel_input = ("selector", "input.drop-hidden-input[type='file']")
    # 确认按钮
    confirm_btn = ("selector", ".el-button--primary", {"has_text": "确认"})
    # 提交按钮
    submit_btn = ("role", "button","提交")
