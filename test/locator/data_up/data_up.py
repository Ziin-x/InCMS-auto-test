class DataUpLocator:
    #当前选中的tab元素
    active_tab ='//*[@class="my-right-detial iblock on"]'
    #当前选择的tab元素有文本信息
    active_tab_with_text = '//*[@class="my-right-detial iblock on" and contains(.,"{}")]'
    #切换tab
    switch_tab = '//*[contains(@class,"my-right-detial iblock") and contains(.,"{}")]'
    # 批量更新 - 模板下载按钮
    template_download_btn = ("role", "button", "模板下载")
    # 批量更新 - Excel上传 input
    excel_upload_input = ("selector", "input[type='file']")
    # 批量更新 - 提交按钮
    batch_submit_btn = ("role", "button", "提交更新")
    # 按模板导入
    template_import_btn = ("selector", "li:visible", {"has_text": "按模板导入"})
    # 自定义导入
    custom_import_btn = ("selector", "li:visible", {"has_text": "自定义导入"})
    # 下载批量更新模板
    download_batch_update_template_btn = ("selector", "span.prjModel.a-line", {"has_text": "下载最新项目模板"})

