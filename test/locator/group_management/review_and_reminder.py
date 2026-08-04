class ReviewAndReminderLocator:
    # 审核界面选择
    registration_review = "//a[contains(@href, 'approval-and-remind-setting') and contains(.,'{}')]"
    # 审核界面选择（断言）
    assert_registration_review = "//li[@class='active' and contains(.,'{}')]"
    # 当前选中的tab
    current_active_tab = '//*[contains(@class,"tab-box")]/li[@class="active"]'
    # 请选择项目
    select_project = ("selector", ".project-head-claim:has-text('请选择项目') .fs-label-wrap")
    # 项目选项
    project_option = "//div[@class='fs-option-label' and contains(.,'{}')]"
    # 请选择审核人
    select_reviewer = ("selector", ".approval-node:has-text('节点1') .fs-label-wrap:visible")
    # 搜索框
    search_box = ("role", "textbox", "搜索")
    # 审核人选项（有审核人）
    reviewer_option = "//div[contains(@class, 'fs-option') and contains(@class, 'selected') and .//div[@class='fs-option-label' and contains(., '{}')]]"
    # 审核人选项（无审核人）
    reviewer_option_no_user = "//div[contains(@class, 'fs-option') and not(contains(@class, 'selected')) and .//div[@class='fs-option-label' and contains(., '{}')]]"
    # 已选中的审核人选项（不限名称，用于取消勾选）
    any_selected_option = ("selector",".fs-option.g0.selected:visible")
    # 保存
    save = ("role","button","保存")
    # 保存成功toast
    save_success_toast = '//*[@class="show_tip" and contains(.,"保存成功")]'



    #审核节点
    approval_node = '//*[@class="approval-node"]//*[@class="fs-wrap multiple"]'
    #审核节点含有index
    approval_node_with_index = '(//*[@class="approval-node"]//*[@class="fs-wrap multiple"])[{}]'
    #审核人搜索框
    approval_user_search_input = '//*[@class="approval-node"]//*[@class="fs-wrap multiple fs-open"]//*[@class="fs-search"]//input'
    #审核
    approval_node_with_search = '//*[@class="approval-node"]//*[contains(@class,"fs-wrap multiple fs-open")]'
    #审核人选项,可能会有多个但是没适配
    approval_user_option = '//*[@class="fs-wrap multiple fs-open"]//*[@class="fs-option selected g0"]'