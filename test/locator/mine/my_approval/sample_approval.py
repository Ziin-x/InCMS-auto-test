class SampleApprovalLocator:
    # 全选
    check_all = (("selector", ".konvajs-content canvas"),(35,15))
    # 审核通过
    approval_btn = ("role", "button", "通过")
    # 审核不通过
    reject_btn = ("role", "button", "拒绝")
    # 审核拒绝原因输入框
    reject_reason_input = ("selector", "textarea[placeholder='请输入拒绝原因']")
    # 确认按钮
    confirm_btn = ("role", "button", "确认")
    # 取消按钮
    cancel_btn = ("role", "button", "取消")
    # 审核拒绝toast
    reject_result = '//*[@class="show_tip" and contains(.,"审核拒绝")]'

