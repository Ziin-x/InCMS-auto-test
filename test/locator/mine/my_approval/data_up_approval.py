class DataUpApprovalLocator:

    approval_btn = ("role","button","审核通过")
    reject_btn = ("role","button","审核不通过")
    #——————二次确认弹层——————
    # 审核拒绝原因输入框
    reject_reason_input = ("role", "textbox", "请输入审核拒绝的原因")
    # 确认按钮
    confirm_btn = ("role", "button", "确认")
    # 取消按钮
    cancel_btn = ("role", "button", "取消")

    # 审核通过toast
    approval_result='//*[@class="show_tip" and contains(.,"审核通过")]'
    # 审核拒绝toast
    reject_result = '//*[@class="show_tip" and contains(.,"审核拒绝")]'


    #——————注册未审核——————
    #审核页行元素，用来检测最新的数据
    table_not_approval_row = '//*[@class="tablescroll_wrapper"]//tr[{}]/td[contains(.,"{}")]'
    #数据行的checkbox
    table_not_approval_checkbox = '//*[@class="tablescroll_wrapper"]//tr[{}]/td/span[contains(@class,"checkbox-btn")]'