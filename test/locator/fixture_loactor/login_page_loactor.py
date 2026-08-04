class LoginPageLocator:
    # 登录
    account_input = ("role", "textbox", "账号")
    # 密码
    password_input = ('selector', 'input[type="password"]')
    # 登录按钮
    login_button = ("selector", ".btn.blue.login-btn")
    # 登录plug检查的元素
    check_login_plug = ("selector",".menu-title", {"has_text": "欢迎来到plug"})
    # 平台图标元素
    product_ele = '//*[contains(@class,"fl module-box") and contains(.,"{}")]'
