class StorageAndContainerLocator:
    # 界面切换
    switch_button = "//div[contains(@class,'location-container-toolbar-button__text') and contains(.,'{}')]"
    # 新建
    new_button = "//div[contains(@class,'location-container-add__text') and contains(.,'{}')]"
    # 类型名称
    type_name = ("selector", ".el-form-item:has(.el-form-item__label:text('类型名称')) .el-input__inner")
    # 缩写
    abbreviation = ("selector", ".el-form-item:has(.el-form-item__label:text('缩写')) .el-input__inner")
    # 新建属性字段
    new_attribute_field = ("selector",".attribute-field-container",{"has_text":"新建"})
    # 字段标题
    field_title = ("selector",".el-input.el-input--suffix.form-input .el-input__inner")
    # 可存放的样品管类型
    store_sample_container_type = ("selector",".el-select__selected-item.el-select__placeholder.is-transparent",
                                   {"has_text": "可存放的样品管类型"})
    # 通用样品管选项
    common_sample_container_option = ("role","option","通用样品管")
    # 规格
    specification = ("selector",".el-select__selected-item.el-select__placeholder.is-transparent",
                                   {"has_text": "请选择"})
    # 孔板选项
    hole_plate_option = ("role","option","6孔板（2 X 3）")
    # 确认
    confirm_button = ("role","button","确认")
    # 创建
    create_button = ("role","button","创建")
    # 类型名称（创建后断言）
    assert_type_name = "//div[contains(@class,'cell') and contains(.,'{}')]"
