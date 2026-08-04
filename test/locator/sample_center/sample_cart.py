class SampleCartLocator:
    # 断言-领样车界面
    assert_sample_cart = ("selector", ".main-top-title", {"has_text": "领样车"})
    # 按量tab（未激活，用于点击切换）
    quantity_tab = ("selector", ".el-tabs__item.is-top", {"has_text": "按量"})
    # 按量tab（激活状态，用于断言切换成功）
    quantity_tab_active = ("selector", ".el-tabs__item.is-top.is-active", {"has_text": "按量"})
    # 选中所有样品
    check_all_sample = (("selector", ".konvajs-content canvas"),(35,15))
    # 删除
    delete_btn = ("role", "button", "删除")
    # 接收人
    receiver_btn = ("selector", ".user-select-box.input-box")
    # 接收人选项
    receiver_option = "//*[contains(@class, 'row') and contains(@class, 'is-single') and text()='{}']"
    # 选中第一个申领样品
    check_newest_sample = (("selector", ".konvajs-content canvas"),(35,55))
    # 申领量（需要双击，向第一个样品填入）
    claim_amount = (("selector", ".konvajs-content canvas"),(700,55))
    # 申领量单位下拉框
    claim_amount_unit = ("selector", ".el-input__suffix-inner")
    # 申领量单位下拉框质量
    claim_amount_unit_volume = ("selector", ".el-cascader-node__label", {"has_text":"质量"})
    # 选择μg
    claim_amount_unit_volume_μg = ("selector", ".el-cascader-node__label", {"has_text":"μg"})
    # 立即申领
    claim_now = ("role", "button", "立即申领")