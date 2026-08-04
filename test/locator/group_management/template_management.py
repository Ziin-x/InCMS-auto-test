class TemplateManagementLocator:
    # 项目与模板
    project_and_template_button = ("role","tab","项目与模板")
    # 项目与模板（效验）
    project_and_template_assert = ("selector",".el-tabs__item.is-top.is-active",{"has_text": "项目与模板"})

class RegistrationTemplateLocator:
    # 新增模板
    add_template_button = ("role","button","模板")
    # 模板
    template_type = "//div[@class='register-btn-name' and text()='{}']"
    # 页面frame
    template_frame = ("selector", "iframe")
    # 填加模块
    add_module_button = ("selector",".iblock.show-set-module")
    # 模块
    module = ("selector",".iblock.add-module-btn")
    # 模板名称
    template_name = ("selector",".template-title")
    # 字段设置图标
    field_setting = ("selector",".el-button.is-link.template-config-btn")
    # 成分模块配置
    component_module_configuration = ("selector",".config-dialog-title",{"has_text": "成分模块配置"})
    # 新建字段（混合物/配方）
    new_field_1 = ("selector", ".add-attribute-field-container", {"has_text": "自定义字段"})
    # 字段标题（混合物/配方）
    field_title_1 = ("role", "textbox", "请输入标题内容")
    # 确定
    confirm_button_1 = ("role","button","确定")
    # 新建字段（自定义物质）
    new_field_2 = ("selector",".add-attribute-filed-container", {"has_text": "新建"})
    # 字段标题（自定义物质）
    field_title_2 = ("selector", ".el-dialog__body:has-text('字段标题') .el-input__inner")
    # 确认（自定义物质）
    confirm_button_2 = ("selector",".el-dialog__body:has-text('字段标题') .el-button.el-button--primary",{"has_text": "确认"})
    # 确认
    confirm_button = ("role", "button", "确认")
    # 设置图标
    setting_button = "//span[text()='{}']/ancestor::div[contains(@class, 'module-part')]//span[contains(@class, 'set-field') and contains(@class, 'set-up')]"
    # 参数设置
    parameter_setting = ("selector",".set-m-btn",{"has_text": "参数设置"})
    # 新增
    add_button = ("selector",".field-opts.add.iblock",{"has_text": "新增"})
    # 参数名
    parameter_name = ("selector", ".field-name")
    # 提示信息
    tip_message = ("selector",".field-text.field-opts-box .input-part:has-text('提示信息') .form-control.content_r_form")
    # 参数选择项
    parameter_option = ("role", "textbox", "请输入选择项")
    # 保存自定义参数
    save_custom_parameter_button = ("role", "button", "保存")
    # 保存模板
    save_template_button = ("role","button","保存模板")
    # 断言模版元素
    assert_template_element = "//div[@class='cell' and text()='{}']"

class ProjectAndTemplateLocator:
    # 新增项目
    add_project_button = ("role","button","项目")
    # 项目名称（表单第一个 el-input）
    project_name = ("selector", ".create-project-form .el-form-item:nth-child(1) .el-input__inner")
    # 项目编号（表单第二个 el-input）
    project_code = ("selector", ".create-project-form .el-form-item:nth-child(2) .el-input__inner")
    # 开始时间（日期范围选择器第一个 input，placeholder 为"开始日期"）
    start_time = ("selector", "input[placeholder='开始日期']")
    # 结束时间（placeholder 为"结束日期"，有唯一 style 标记）
    end_time = ("selector", "input[placeholder='结束日期']")
    # 确定
    confirm_button = ("role","button","确定")
    # 项目与模板项目（断言）
    project_and_template = "//div[@class='project-name-cell-content el-tooltip__trigger el-tooltip__trigger' and text()='{}']"
    # 搜索框
    search_box = ("role","textbox","项目名称、项目编号")
    # 搜索按钮
    search_button = ("selector",".el-input-group__append .el-button")
    # 添加关联模版
    add_associated_template = "//tr[.//div[contains(@class, 'project-name-cell-content') and contains(text(),'{}')]]//a[contains(@class, 'add-template-link')]"
    # 关联模版下拉框
    associated_template_dropdown = ("selector",".el-select__selected-item.el-select__placeholder.is-transparent",
                                    {"has_text": "请选择关联模板"})
    # 模版选项
    template_option = "//span[@class='option-label' and text()='{}']"

