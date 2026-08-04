class SingleRegisterLocator:
    loading_ele = '(//*[@class="circular"])[last()]'
    # 选择项目
    select_project = ("selector", ".el-select__selected-item.el-select__placeholder.is-transparent",
                      {"has_text": "请选择项目"})
    # 项目选项
    project_option = "//li[@class='el-select-dropdown__item' and contains(.,'{}')]"
    # 选择模版
    # select_template = ("selector", ".el-select__selected-item.el-select__placeholder.is-transparent",)
    select_template = '//*[@class="form-item" and contains(.,"模板")]//input'
    # 模版选项
    template_option = "//li[@class='el-select-dropdown__item' and contains(.,'{}')]"
    # 确定
    confirm = ("role", "button","确定")
    # 下一步
    next_step = ("role", "button","下一步")
    # SMILES 值
    smiles_value = ("selector", ".label[data='smiles']")
    # frame元素
    frame = ("selector", "iframe:visible")
    # 模块（断言）
    module = "//div[@class='module-title center' and contains(.,'{}')]"
    # 参数
    parameter = ("//div[contains(@class, 'module-title') and contains(.,'基本信息')]"
                 "/ancestor::div[contains(@class, 'module-part')]"
                 "//td[text()='{}']")
    # 批号
    batch_number = "tr:has-text('批号') input#exp_code"
    # 注册的量
    register_amount = "tr:has-text('注册的量') input[name='submit_mass']"
    # 提交注册
    submit_register = ("role", "button","提交注册")
    # 登记样品
    register_sample = ("role", "button", "登记样品")
    #注册step2上方按钮
    step2_button = '//*[@class="next-button"]/button[contains(.,"{}")]'
    #提交toast
    success_toast = '//*[@class="el-message__content" and contains(.,"成功")]'

    #——————成分信息相关元素——————
    #————化合物————
    #Indraw画布
    # indraw画布相关元素
    indraw_frame = ("selector", "iframe[src*='/indraw/index.html']")
    # indraw画布
    indraw_canvas = '//*[@id="indraw-canvas-box"]'
    #异构体类型
    isomer_type = '//*[@class="isomer-selector"]//input'
    isomer_type_option = '//*[contains(@class,"el-select-dropdown__item")]//span[text()="{}"]'
    # 序列元素
    # 添加序列按钮（+）
    add_sequence_btn = '//*[@class="add-row-btn"]'
    # 序列名称
    sequence_name_with_index = '//*[@class="sequence-table"]//tbody/tr[{}]/td//*[@class="cell-content name"]/textarea'
    # 序列
    sequence_with_index ='//*[@class="sequence-table"]//tbody/tr[{}]/td//*[@class="cell-content sequence"]/textarea'

    #————DNA&RNA————
    # sequence的iframe
    sequence_iframe = ("selector", "iframe[src*='/insequence/index.html']")
    #新建序列
    new_sequence  =  '//*[@class="button-box"]/i[contains(@class,"new-sequence")]'
    #打开序列
    open_sequence_file = '//*[@class="button-box"]/i[contains(@class,"open-sequence")]'
    #导入序列
    import_sequence = '//*[@class="button-box"]/i[contains(@class,"import-sequence")]'
    #序列输入框
    sequence_input = '//*[@class="el-textarea"]/textarea'
    #序列确认框
    sequence_confirm_btn = ("role","button", "确认")
    #序列选中的类型
    sequence_type_selected = '(//*[@class="el-radio is-checked"])[1]'
    #序列类型
    sequence_type =  '//label[contains(@class,"el-radio")  and contains(.,"{}")]'
    #绘制的sequence画布
    draw_sequence = '//*[@class="view-box-main"]'
    #————自定义物质————
    #自定义字段
    custom_filed = '//*[@class="field-item" and contains(.,"{}")]//input'
    #基本信息模块元素
    basic_module_filed = "//div[@id='coreData']//table//td[contains(text(),'{}')]/following-sibling::td[1]//input[not(@type='hidden')]"
