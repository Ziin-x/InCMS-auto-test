class MineRegistrationLocator:
    #页面标题
    mine_registration_title = '//*[@class="main-top-title" and contains(.,"我注册的")]'
    # 注册编号
    mine_registration_number = "(//tr[.//div[@class='project_name' and contains(.,'{}')]])[1]/td[3]/p[1]"
    # 批号
    batch_number = "(//tr[.//div[@class='project_name' and contains(.,'{}')]])[1]/td[3]/p[2]"

    #我注册的页，第一行，根据批号匹配最新注册的数据，用于检测数据是否注册成功
    table_register_first_row = '//*[@class="tablescroll_wrapper"]//tr[1]/td[contains(.,"{}")]'

    #我注册的，表头元素
    register_table_header = 'table.tablescroll_head thead tr th'
    #我注册的，table元素
    register_table_row_info = '//*[@class="tablescroll_wrapper"]/table//tr[{}]/td[{}]'
