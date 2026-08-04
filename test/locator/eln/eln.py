class ELNLocator:
    # 新建记录
    create_record_btn = ("selector", ".el-button.create-button", {"has_text": "新建记录"})
    # 新建记录本
    create_notebook_link = ("selector", ".create-link", {"has_text": "新建记录本"})

    # 记录本选择框
    notebook_select = ("selector", ".label-row:has-text('记录本') + .el-form-item input")
    # 记录本选项（参数化）
    notebook_option = "//li[@class='el-select-dropdown__item']//span[contains(.,'{}')]"

    # 模版选择框
    template_select = ("selector", ".label-row:has-text('模板') + .el-form-item input")
    # 空白模板选项
    blank_template_option = ("selector", ".el-select-dropdown__item", {"has_text": "空白模板"})

    # 鹰群选择框
    group_select = ("selector",".el-select__selection", {"has_text": "请选择鹰群"})
    # 鹰群选项（参数化）
    group_option = "//li[@class='el-select-dropdown__item']//span[contains(.,'{}')]"

    # 记录本名称
    form_item_input = ("role","textbox","请输入")

    # 所属项目输入框
    project_select = ("selector", ".el-dialog input.el-input__inner[placeholder='请选择项目']")
    # 项目树节点（参数化）
    project_tree_option = "//span[@class='tree-node-label' and contains(.,'{}')]"
    # 确定按钮
    confirm_btn = ("role", "button","确定")
    # 确认按钮
    Confirm_btn = ("role", "button","确认")

### --------------------------------记录界面--------------------------------- ###
    # 添加模块
    add_module_btn = ("selector", ".add-module-btn")
    # 关闭模块面板
    panel_close_btn = ("selector", ".panel-close")
    # InDraw 模块
    indraw_module = ("selector", ".module-label", {"has_text": "InDraw"})
    # 添加产物
    add_product_btn = ("selector", "div[title='添加产物'] i.icon-add")
    # 产物搜索输入框
    product_search_input = ("placeholder", "请输入名称或CAS号")
    # 产物搜索结果选项
    product_suggestion = ("selector", ".suggestion-name", {"has_text": "苯"})
    # 产物
    product_badge = ("selector", ".material-row-num.prd", {"has_text": "P1"})
    # 注册到CMS
    register_to_cms_btn = ("selector", ".do_submit_chemical", {"has_text": "注册到CMS"})


