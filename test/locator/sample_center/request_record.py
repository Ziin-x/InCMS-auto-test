class RequestRecordLocator:
    # 申领记录导航
    request_record_nav = ("selector", ".menu-item-title", {"has_text": "申领记录"})
    # 已接收界面切换按钮
    received_view_btn = ("selector", ".view-change-btn", {"has_text": "已接收"})
    # 已接收界面切换按钮（active状态，用于断言已切换成功）
    received_view_btn_active = ("selector", ".view-change-btn.active", {"has_text": "已接收"})
    # 界面切换按钮（模板）【与出库界面通用】
    view_btn = "//div[contains(@class,'view-change-btn') and contains(.,'{}')]"
    # 界面切换按钮（active状态模板）【与出库界面通用】
    view_btn_active = "//div[contains(@class,'view-change-btn') and contains(@class,'active') and contains(.,'{}')]"
    # 选中所有物品（canvas相对坐标）
    check_all_request = (("selector", ".konvajs-content canvas"), (35, 16))
    # 选中第一个物品（canvas相对坐标）
    check_first_received = (("selector", ".konvajs-content canvas"), (36, 54))
    # 选中所有归还样品
    check_all_return = (("selector", ".inform-content .konvajs-content canvas"), (36, 18))
    # 归还按钮
    return_btn = ("role", "button", "归还")
    # 任务分配按钮
    assign_btn = ("role", "button", "任务分配")
    # 选择成员下拉框
    select_member = ("selector", ".el-select__wrapper.is-filterable", {"has_text": "请选择成员"})
    # 成员选项
    member_option = "//li[contains(@class,'el-select-dropdown__item') and contains(.,'{}')]"
    # 接收按钮
    receive_btn = ("role", "button", "接收")
    # 确认按钮
    confirm_btn = ("role", "button", "确认")
    # 断言-申领记录界面
    assert_request_record = ("selector", ".main-top-title", {"has_text": "申领记录"})
