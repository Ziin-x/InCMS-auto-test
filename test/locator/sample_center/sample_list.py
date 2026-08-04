class SampleListLocator:
    # 样品列表（等待）
    wait_loading = ("selector", ".toolbar")
    # 样品登记
    sample_register = ("role", "button", "登记")
    # 批量
    batch = ("role", "button", "批量")
    # 批量登记
    batch_register = ("selector", ".el-dropdown-menu__item", {"has_text": "批量登记"})
    # 样品名称
    sample_name = ("role", "textbox", "样品名称")
    # 所属项目
    project = ("selector", ".option-cell-container",{"has_text": "请选择"})
    # 项目选项
    project_option = "//span[@class='item-name' and contains(.,'{}')]"
    # 当前的量
    current_amount = ("selector", ".el-form-item.is-required.asterisk-right.el-form-item--label-top:has-text('当前的量') .el-input__inner")
    # 提交登记
    submit_register = ("role", "button","提交登记")
    # 勾选最新样品
    check_newest_sample = (("selector", ".konvajs-content canvas"),(35,54))
    # 申领按钮
    sample_request = ("role", "button", "申领")
    # 报废按钮
    sample_scrap = ("role", "button", "报废")
    # 立即领用按钮
    sample_request_immediately = ("role", "button", "立即领用")
    # 按量领用按钮（item-btn）
    quantity_method_btn = ("selector", ".item-btn", {"has_text": "按量"})
    # 加入领样车按钮
    add_to_cart_btn = ("role", "button", "加入领样车")
    # 立刻申领按钮
    sample_request_now = ("role", "button", "立即申领")
    # 勾选全部申领
    check_all_sample = (("selector", ".inform-container-out .konvajs-content canvas"),(35,16))
    # 原因输入框
    reason_input = ("placeholder", "请输入原因 (必填)")
    # 确认按钮
    confirm_btn = ("role", "button", "确认")
