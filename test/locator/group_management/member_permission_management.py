class MemberPermissionManagementLocator:
    # 成员管理（效验）
    assert_member_management = ("selector", ".el-tabs__item.is-top.is-active", {"has_text": "成员管理"})
    # 配置注册权限
    configure_registration_permissions = (("selector", ".konvajs-content canvas"),(620,90))
    # 全部项目勾选框
    all_projects_checkbox = ("selector", ".select-all-container:has-text('全部项目') .el-checkbox")
    # 全部项目勾选框（已勾选）
    all_projects_checkbox_checked = ("selector", ".select-all-container:has-text('全部项目') .el-checkbox.is-checked")
    # 全部项目勾选框（单个勾选）
    all_projects_checkbox_indeterminate = ("selector", ".select-all-container:has-text('全部项目') .el-checkbox__input.is-indeterminate")
    # 可见/可注册（未勾选）
    visible_register = ("selector", ".checkbox-with-label-container:has-text('可见/可注册') .el-checkbox")
    # 可见/可注册（已勾选）
    visible_register_checked = ("selector", ".checkbox-with-label-container:has-text('可见/可注册') .el-checkbox.is-checked")
    # 可更新数据（未勾选）
    update_data = ("selector", ".checkbox-with-label-container:has-text('可更新数据') .el-checkbox")
    # 可更新数据（已勾选）
    update_data_checked = ("selector", ".checkbox-with-label-container:has-text('可更新数据') .el-checkbox.is-checked")
    # 提交
    submit = ("role","button","提交")

### -------------------------------------------角色权限界面-----------------------------------------------###

    # 角色权限
    role_permission = ("role", "tab","角色权限")
    # 角色权限（效验）
    assert_role_permission = ("selector", ".el-tabs__item.is-top.is-active", {"has_text": "角色权限"})
    # 出库权限下拉框
    outbound_select = ("selector", "tr:has(td:has-text('出库')) .el-select__placeholder span")
    # 页面不可见-选项
    page_invisible_option = ("role", "option", "页面不可见")
    # 可操作-选项
    operable_option = ("role", "option", "可操作")
    # 保存
    save = ("role", "button", "保存")
