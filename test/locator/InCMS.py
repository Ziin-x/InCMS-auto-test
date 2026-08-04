class InCMSLocator:
    #——————导航栏元素——————
    # 左侧导航栏可见
    left_menu_visible_ele = '//*[@class="layout-left-container" and not(contains(@style,"display: none;"))]'
    #搜索按钮
    search_button = ("selector", ".el-button.search-btn", {"has_text": "搜索"})
    #搜索框
    quick_search_input = ("role", "textbox", r"注册编号 / 批号 / 条形码等")
    #搜索弹窗搜索按钮
    search_window_search_btn = ("selector",".el-button.el-button--primary.search-button", {"has_text": "搜索"})
    # 数据中心
    data_center = ("selector", ".menu-item-container", {"has_text": "数据中心"})
    # 改用 XPath text() 精确匹配，避免 has_text 子串匹配到「数据更新审核」
    data_up = '//span[@class="menu-item-title" and text()="数据更新"]'
    # 注册按钮
    register_button = ("selector",
                       ".menu-item-container:has-text('数据中心') i.el-icon.add-substance.el-tooltip__trigger.el-tooltip__trigger")
    # 单个注册
    single_register = ("selector", ".popover-menu-item", {"has_text": "单个注册"})
    # 批量注册
    batch_register = ("selector", ".popover-menu-item", {"has_text": "批量注册"})
    # 全部项目
    all_projects = ("selector", "span.menu-item-title[title='全部项目']")
    # 数据中心项目（断言）
    data_center_project = "//span[@class='menu-item-title' and text()='{}']"
    # 数据可视化
    visualization = ("selector", ".menu-item-title", {"has_text": "数据可视化"})
    #————样品中心————
    # 样品中心
    sample_center = ("selector",".menu-item-container", {"has_text": "样品中心"})
    # 样品列表
    sample_list = ("selector",".menu-item-title", {"has_text": "样品列表"})
    #————我的————
    # 我的
    mine = ("selector", "span.menu-item-text[title='我的']:visible")
    # 我注册的
    mine_register = ("selector", ".menu-item-title", {"has_text": "我注册的"})
    # 我的审核
    my_approval = ("selector", "span.menu-item-text:visible", {"has_text": "我的审核"})
    # 数据注册审核
    data_register_approval = ("selector", ".menu-item-title", {"has_text": "数据注册审核"})
    # 数据更新审核
    data_up_approval = ("selector", ".menu-item-title", {"has_text": "数据更新审核"})
    # 样品相关审核
    sample_approval = ("selector", ".menu-item-title", {"has_text": "样品相关审核"})
    #————群内管理————
    # 群内管理
    group_management = ("selector", ".menu-item-container", {"has_text": "群内管理"})
    # 编号规则
    code_rules = ("selector", ".menu-item-title", {"has_text": "编号规则"})
    # 模板管理
    template_management = ("selector", ".menu-item-title", {"has_text": "模板管理"})
    # 成员权限管理
    member_permissions_management = ("selector", ".menu-item-title", {"has_text": "成员权限管理"})
    # 样品管理
    sample_management = ("selector", ".menu-item-title", {"has_text": "样品管理"})
    # 审核与提醒
    review_and_reminder = ("selector", ".menu-item-title", {"has_text": "审核与提醒"})

    #————企业级管理————
    # 企业级管理
    enterprise_management = ("selector", ".menu-item-container", {"has_text": "企业级管理"})
    # 库位与容器
    storage_and_container = ("selector",".menu-item-title", {"has_text": "库位与容器"})

    #————样品中心扩展————
    # 出库
    outbound = ("selector", ".menu-item-title", {"has_text": "出库"})
    # 领样车
    sample_cart = ("selector", ".menu-item-title", {"has_text": "领样车"})
    # 申领记录
    request_record = ("selector", ".menu-item-title", {"has_text": "申领记录"})
    # 分配的任务
    assigned_tasks = ("selector", ".menu-item-title", {"has_text": "分配的任务"})

    #————群内管理扩展————
    # 申领配置
    request_config = ("selector", ".menu-item-title", {"has_text": "申领配置"})