class GeneralConfigurationLocator:
    # 通用配置tab（active状态，用于判断是否进入界面）
    general_config_tab = ("selector", "#tab-general.is-active", {"has_text": "通用配置"})
    # 自动出库 — 状态标签（class含disabled=关闭，否则=开启）
    auto_outbound_label = ("selector","span:visible",{"has_text": "自动出库"})
    # 自动出库 — 开关点击目标
    auto_outbound_switch = "//span[text()='自动出库']/preceding-sibling::div[1]//span[contains(@class,'el-switch__core')]"
    # 自动接收 — 状态标签
    auto_receive_label = ("selector","span:visible",{"has_text": "自动接收"})
    # 自动接收 — 开关点击目标
    auto_receive_switch = "//span[text()='自动接收']/preceding-sibling::div[1]//span[contains(@class,'el-switch__core')]"