class BatchRegisterLocator:
    # 批量注册 iframe
    batch_register_frame = ("selector", "iframe")
    # 下载最新Excel项目模板
    download_template_btn = ("selector", "span.prjModel.a-line.hover_line:visible", {"has_text": "下载最新Excel项目模板"})
    # 上传成功后自动提交注册
    auto_submit_btn = ("selector", "span.choose-btn:visible", {"has_text": "上传成功后，自动提交注册"})
    # 填写注册的量时自动登记样品
    auto_register_sample_btn = ("selector", "span.checkbox-btn:visible", {"has_text": "填写注册的量时自动登记样品"})
    # 样品登记成功后直接入库
    auto_inbound_btn = ("selector", "span.checkbox-btn", {"has_text": "样品登记成功后直接入库"})
    # Excel上传 input
    excel_upload_input = ("selector", "input.webuploader-element-invisible")
    # 上传按钮
    upload_btn = ("selector", "button.restSubmit")
    # 提交按钮
    submit_btn = ("role", "button", "提交")
