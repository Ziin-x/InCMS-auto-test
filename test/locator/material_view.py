class MaterialViewLocator:
    # —————— 物质详情页导航 ——————
    # loading元素
    loading_ele = '(//*[@class="circular"])[last()]'
    # 物质详情页 iframe
    material_view_frame = ("selector", "iframe[src*='/chemical/view']")
    # 数据更新弹窗 iframe
    data_up_frame = ("selector", "iframe[src*='/chemical/data-update']")
    # 数据更新按钮
    data_up_btn = ("role","button", "数据更新")
    # 数据更新页面中的项目名称（用于效验是否有数据更新权限）
    data_up_project_name = '//td[@style="width: 165px;" and contains(text(),"{}")]'
    #申领按钮
    request_sample_btn = ("role", "button", "申领")
    #导出按钮
    export = ("role","button","导出")
    #模块标题元素
    module_title = '//*[contains(@class,"module-part")]//div[@class="module-title center"]/b'
    # —————— 基本信息 ——————
    #获取模块的所有字段名
    basic_info_module_fields = '//div[@id="coreData"]//table//td[not(contains(@class,"label"))]'
    # 物化信息模块字段，使用字段名获取字段值
    physicochemical_info_module_fields = '//div[@id="pcData"]//table//td[not(contains(@class,"label"))]'

    #基本信息模块字段，使用字段名获取字段值
    basic_info_module_field = '//div[@id="coreData"]//table//td[normalize-space()="{}"]/following-sibling::td[1]'
    #物化信息模块字段，使用字段名获取字段值
    physicochemical_info_module_field = '//div[@id="pcData"]//table//td[normalize-space()="{}"]/following-sibling::td[1]'

    # ——————数据更新iframe——————

    # 退出数据更新
    quit_data_up_btn = ("role", "button", "退出")
    # 提交数据更新
    submit_data_up_btn = ("role", "button", "提交更新")
    # 批次修改弹层
    data_up_edit_notion = '//*[@class="select-update-type-title text-sm-regular"]'
    # 批次修改弹层
    data_up_edit_notion_label ='(//*[@class="select-update-type-content"]//label)[{}]'


    # —————— 成分信息 ——————
    # 序列信息 (DNA/RNA)
    sequence_info = "//div[contains(@class,'sequence-info')]//span[contains(@class,'sequence-text')]"
    # 序列类型
    sequence_type = "//div[contains(@class,'sequence-info')]//span[contains(@class,'sequence-type')]"
    # 自定义字段名称
    custom_field_name = "//div[contains(@class,'custom-field')]//span[contains(@class,'field-name') and contains(.,'{}')]"
    # 自定义字段值
    custom_field_value = "//div[contains(@class,'custom-field')]//span[contains(@class,'field-name') and contains(.,'{}')]/following-sibling::span"
    #——————模块信息——————
    #模块标题元素
    data_up_module_name = '//*[contains(@class,"module-part")]//div[@class="module-title center"]/b[contains(text(),"{}")]'
    #数据更新基本信息模块input
    data_up_basic_info_field = '//div[@id="coreData"]//td[contains(text(),"{}")]/following-sibling::td[1]//input[@type="text" and not(@disabled)]'
    #数据更新物化信息模块input
    data_up_physicochemical_info_field = '//div[@id="pcData"]//td[contains(text(),"{}")]/following-sibling::td[1]//input[@type="text" and not(@disabled)]'
    # —————— 操作按钮 ——————
    # 编辑
    edit_button = ("role", "button", "编辑")
    # 删除
    delete_button = ("role", "button", "删除")
    # 确认（二次确认弹窗）
    confirm = ("role", "button", "确定")
    # 取消
    cancel = ("role", "button", "取消")
