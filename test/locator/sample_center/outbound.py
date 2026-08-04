class OutboundLocator:
    # 断言-出库界面
    assert_outbound = ("selector", ".main-top-title", {"has_text": "出库"})
    # 全选样品
    select_all_sample = (("selector", ".konvajs-content canvas"), (35, 18))
    # 拣货
    pick_up = ("selector", ".operation-item", {"has_text": "拣货"})
    # 出库
    outbound = ("selector", ".operation-item", {"has_text": "出库"})
    # 全选所有拣货订单
    select_all_pick_up_order = (("selector", ".el-drawer__body .konvajs-content canvas"), (63, 17))
    # 完成拣货
    complete_pick_up = ("role", "button", "完成拣货")
    # 确认
    confirm = ("role", "button", "确认")
