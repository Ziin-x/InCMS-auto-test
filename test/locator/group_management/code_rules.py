class CodeRulesLocator:
    # 批号界面
    batch_number_page = ("role","tab","批号")
    # 批号界面（断言）
    batch_number_page_assert = ("selector",".el-tabs__item.is-top.is-active", {"has_text": "批号"})
    # 样品ID界面
    sample_id_page = ("role","tab","样品ID")
    # 样品ID界面（断言）
    sample_id_page_assert = ("selector",".el-tabs__item.is-top.is-active", {"has_text": "样品ID"})
    # 自动生成批号开关（开启状态）
    auto_generate_batch_number_opened = ("selector",".el-switch.el-switch--small.is-checked")
    # 自动生成批号开关（关闭状态）
    auto_generate_batch_number_closed = ("selector",".el-switch.el-switch--small")
    # 编码规则前缀
    code_rule_prefix = ("selector",".drag-item:has-text('前缀') .el-input__inner")
    # 输入自定义字符
    custom_character = ("selector", ".drag-item:has-text('自定义字符') .el-input__inner:visible")
    # 创建日期
    build_date = ("selector",".drag-item:has-text('创建日期')")
    # 编码规则新增字段
    add_field = ("role","button","新增")
    # 自定义字符选项
    custom_character_option = ("selector", ".el-dropdown-menu__item:visible", {"has_text": "自定义字符"})
    # 创建日期选项
    build_date_option = ("selector",".el-dropdown-menu__item:visible",{"has_text": "创建日期"})
    # 间隔符号选择框
    interval_symbol_selection = ("selector",".code-rule-config-container:has-text('间隔符号') div.el-select__wrapper:visible")
    # 间隔符号横线
    interval_symbol_line = ("selector", ".el-select-dropdown__item:visible", {"has_text": "横线"})
    # 有序流水号（选项）
    orderly_running_water_number = ("selector",".el-radio__label",{"has_text": "有序流水号"})
    # 流水号相同时递增（选项）
    serial_number_increases_simultaneously = ("selector",".el-only-child__content.el-tooltip__trigger.el-tooltip__trigger",
                                              {"has_text": "流水号相同时递增"})
    # 预览
    preview = ("selector", ".preview-box:visible")
    # 保存
    save = ("role","button","保存")
