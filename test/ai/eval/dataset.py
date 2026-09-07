
SAMPLES = [
    {
        "id": "001",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart01",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """self = <object.sample_cart_page.SampleCartPage object at 0x7f9c41d8e5d0>

    def add_to_cart(self, sample_name):
>       self.click(("text", sample_name))

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("text=DNA质粒001")
E     locator resolved to 0 elements
E   ============================================================""",
        "label": "",
    },
    {
        "id": "002",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register_with_approval_01",
        "error_type": "AssertionError",
        "error": "审批状态异常：期望 '已通过'，实际 '待审批'",
        "traceback": """    def assert_approval_status(self, expect_status: str):
        status = self.get_text(("selector", ".approval-status"))
>       assert status == expect_status, f"审批状态异常：期望 {expect_status!r}，实际 {status!r}"
E   AssertionError: 审批状态异常：期望 '已通过'，实际 '待审批'

test/testcases/data_center/test_single_register.py:87: AssertionError""",
        "label": "",
    },
    {
        "id": "003",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register01",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_CONNECTION_REFUSED at https://cms-test.example.com/login",
        "traceback": """    @pytest.fixture(scope="session")
    def InCMS_page(self):
        page = browser.new_page()
>       page.goto(f"{BASE_URL}/login")

E   playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at https://cms-test.example.com/login
E   Call log:
E     - navigating to "https://cms-test.example.com/login", waiting until "load"

test/conftest.py:45: Error""",
        "label": "",
    },
    {
        "id": "004",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list_search01",
        "error_type": "TimeoutError",
        "error": "Timeout 10000ms exceeded.",
        "traceback": """    def wait_search_result(self):
>       self.wait_for(("selector", ".table-row"), timeout=10000)

E   playwright._impl._errors.TimeoutError: Timeout 10000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".table-row")
E     locator resolved to 0 elements
E   ============================================================
E   备注：本地重跑该用例通过""",
        "label": "",
    },
    {
        "id": "005",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up02",
        "error_type": "Error",
        "error": "An unexpected error occurred",
        "traceback": """（CI 日志被截断，仅保留最后输出）
E   playwright._impl._errors.Error: An unexpected error occurred

test/testcases/data_up/test_data_up.py:63: Error""",
        "label": "",
    },

    {
        "id": "006",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule01",
        "error_type": "AssertionError",
        "error": "编号规则断言失败：期望 'SP-202609-001'，实际 'SP-202609-001'",
        "traceback": """    def test_code_rule01(self, load_code_rules_page, request):
        code = self.get_text(("selector", ".code-display"))
>       assert code == "SP-202609-001", f"编号规则断言失败：期望 'SP-202609-001'，实际 {code!r}"
E   AssertionError: 编号规则断言失败：期望 'SP-202609-001'，实际 'SP-202609-002'

test/testcases/group_management/test_code_rules.py:42: AssertionError""",
        "label": "",
    },
    {
        "id": "007",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "AssertionError",
        "error": "批量注册数量不符：期望 10 条，列表实际显示 9 条",
        "traceback": """    def test_batch_register(self, InCMS_page):
        self.batch_register(data)
        count = self.get_list_count()
>       assert count == len(data), f"批量注册数量不符：期望 {len(data)} 条，列表实际显示 {count} 条"
E   AssertionError: 批量注册数量不符：期望 10 条，列表实际显示 9 条

test/testcases/data_center/test_batch_register.py:56: AssertionError""",
        "label": "",
    },
    {
        "id": "008",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "AssertionError",
        "error": "注册接口响应异常：期望 200，实际 502",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/batch_register" in r.url) as resp:
            self.click(("role", "button", "提交"))
            response = resp.value
>           assert response.status == 200, f"注册接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 注册接口响应异常：期望 200，实际 502
E   请求: POST https://cms-test.example.com/api/v1/batch_register

test/testcases/data_center/test_batch_register.py:48: AssertionError""",
        "label": "",
    },
    {
        "id": "009",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template01",
        "error_type": "TimeoutError",
        "error": "Timeout 15000ms exceeded.",
        "traceback": """    def test_create_template01(self, InCMS_page):
        self.open_template_dialog()
>       self.wait_for(("role", "dialog"), timeout=15000)

E   playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
E   =========================== logs ===========================
E   waiting for get_by_role("dialog")
E     locator resolved to 0 elements
E   ============================================================
E   备注：重跑后弹窗正常出现""",
        "label": "",
    },
    {
        "id": "010",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization01",
        "error_type": "MemoryError",
        "error": "",
        "traceback": """    def test_visualization01(self, load_visualization_page, request):
        self.draw_on_canvas(...)

E   MemoryError

（CI 节点内存不足，进程被终止，无更多日志）""",
        "label": "",
    },

    {
        "id": "011",
        "test_name": "test/testcases/data_center/test_data_export.py::test_export_excel_and_compare",
        "error_type": "KeyError",
        "error": "'物质名称'",
        "traceback": """    def test_export_excel_and_compare(self, InCMS_page, view_mode):
        df = self.read_exported_excel(download_path)
>       names = df["物质名称"].tolist()

E   KeyError: '物质名称'

test/testcases/data_center/test_data_export.py:71: KeyError""",
        "label": "",
    },
    {
        "id": "012",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "记录创建时间异常：期望当前日期，实际 '1970-01-01'",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        self.create_record(...)
        create_time = self.get_text(("selector", ".record-time"))
>       assert create_time.startswith(today), f"记录创建时间异常：期望当前日期，实际 {create_time!r}"
E   AssertionError: 记录创建时间异常：期望当前日期，实际 '1970-01-01'

test/testcases/eln/test_eln.py:95: AssertionError""",
        "label": "",
    },
    {
        "id": "013",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up01",
        "error_type": "FileNotFoundError",
        "error": "[Errno 2] No such file or directory: '/Users/tester/uploads/sample.xlsx'",
        "traceback": """    def test_single_data_up01(self, InCMS_page, request):
>       self.upload_file("/Users/tester/uploads/sample.xlsx")

E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/tester/uploads/sample.xlsx'

test/testcases/data_up/test_data_up.py:38: FileNotFoundError""",
        "label": "",
    },
    {
        "id": "014",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container02",
        "error_type": "TimeoutError",
        "error": "Timeout 20000ms exceeded.",
        "traceback": """    def test_storage_and_container02(self, InCMS_page):
>       self.wait_for(("selector", ".container-list .item"), timeout=20000)

E   playwright._impl._errors.TimeoutError: Timeout 20000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".container-list .item")
E     locator resolved to 0 elements
E   ============================================================
E   备注：同一用例在昨天和前天各失败 1 次、成功 3 次，无规律""",
        "label": "",
    },
    {
        "id": "015",
        "test_name": "test/testcases/sample_center/test_assigned_tasks.py::test_assigned_tasks",
        "error_type": "AssertionError",
        "error": "任务列表断言失败：期望包含 '任务A'",
        "traceback": """    def test_assigned_tasks(self, InCMS_page):
        tasks = self.get_task_names()
>       assert "任务A" in tasks, f"任务列表断言失败：期望包含 '任务A'"

E   AssertionError: 任务列表断言失败：期望包含 '任务A'

（无其他日志，日志文件被轮转覆盖）""",
        "label": "",
    },

    {
        "id": "016",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart02",
        "error_type": "Error",
        "error": "strict mode violation: locator resolved to 3 elements",
        "traceback": """    def test_sample_cart02(self, InCMS_page, request):
>       self.click(("selector", ".add-cart-btn"))

E   playwright._impl._errors.Error: strict mode violation: locator(".add-cart-btn") resolved to 3 elements:
E   - <button class="add-cart-btn">加入领样车</button>
E   - <button class="add-cart-btn">加入领样车</button>
E   - <button class="add-cart-btn">加入领样车</button>

test/testcases/sample_center/test_sample_cart.py:44: Error""",
        "label": "",
    },
    {
        "id": "017",
        "test_name": "test/testcases/group_management/test_member_permission_management.py::test_member_permission_flow",
        "error_type": "AssertionError",
        "error": "权限控制异常：无删除权限的用户仍可见删除按钮",
        "traceback": """    def test_member_permission_flow(self, InCMS_page, browser, request, permission_data):
        login_as_member(permission_data["member"])
        delete_btn = self.locator(("role", "button", "删除"))
>       assert not delete_btn.is_visible(), "权限控制异常：无删除权限的用户仍可见删除按钮"
E   AssertionError: 权限控制异常：无删除权限的用户仍可见删除按钮

test/testcases/group_management/test_member_permission_management.py:103: AssertionError""",
        "label": "",
    },
    {
        "id": "018",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register03",
        "error_type": "AssertionError",
        "error": "保存接口响应异常：期望 200，实际 500",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/register" in r.url) as resp:
            self.click(("role", "button", "保存"))
            response = resp.value
>           assert response.status == 200, f"保存接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 保存接口响应异常：期望 200，实际 500

test/testcases/data_center/test_single_register.py:62: AssertionError""",
        "label": "",
    },
    {
        "id": "019",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        self.switch_to_iframe(("selector", "#editor-frame"))
>       self.wait_for(("selector", ".ql-editor"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".ql-editor")
E     locator resolved to 0 elements
E   ============================================================
E   备注：iframe 已成功切换，但内部富文本编辑器未加载""",
        "label": "",
    },
    {
        "id": "020",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list_filter02",
        "error_type": "AssertionError",
        "error": "筛选结果断言失败：期望 3 条，实际 5 条",
        "traceback": """    def test_sample_list_filter02(self, InCMS_page):
        self.apply_filter({"状态": "已入库", "类型": "DNA"})
        rows = self.get_table_rows()
>       assert len(rows) == 3, f"筛选结果断言失败：期望 3 条，实际 {len(rows)} 条"
E   AssertionError: 筛选结果断言失败：期望 3 条，实际 5 条

（日志仅保留到此，上游 fixture 输出未记录）""",
        "label": "",
    },

    {
        "id": "021",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization02",
        "error_type": "AssertionError",
        "error": "画布点击断言失败：期望坐标 (320, 240) 处出现选中标记",
        "traceback": """    def test_visualization02(self, load_visualization_page):
        self.click_canvas(320, 240)
>       assert self.has_selection_marker(), "画布点击断言失败：期望坐标 (320, 240) 处出现选中标记"
E   AssertionError: 画布点击断言失败：期望坐标 (320, 240) 处出现选中标记

test/testcases/visualization/test_visualization.py:58: AssertionError""",
        "label": "",
    },
    {
        "id": "022",
        "test_name": "test/testcases/data_center/test_data_export.py::test_export_excel_and_compare",
        "error_type": "AssertionError",
        "error": "导出行数不符：页面显示 25 条，Excel 实际 24 行",
        "traceback": """    def test_export_excel_and_compare(self, InCMS_page, view_mode):
        page_count = self.get_list_total()
        df = self.read_exported_excel(download_path)
>       assert len(df) == page_count, f"导出行数不符：页面显示 {page_count} 条，Excel 实际 {len(df)} 行"
E   AssertionError: 导出行数不符：页面显示 25 条，Excel 实际 24 行

test/testcases/data_center/test_data_export.py:82: AssertionError""",
        "label": "",
    },
    {
        "id": "023",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template02",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_NAME_NOT_RESOLVED at https://cms-test.example.com",
        "traceback": """    def test_create_template02(self, InCMS_page):
>       self.page.goto(f"{BASE_URL}/template/create")

E   playwright._impl._errors.Error: Page.goto: net::ERR_NAME_NOT_RESOLVED at https://cms-test.example.com
E   Call log:
E     - navigating to "https://cms-test.example.com/template/create", waiting until "load"

test/testcases/group_management/test_template_management.py:33: Error""",
        "label": "",
    },
    {
        "id": "024",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule02",
        "error_type": "AssertionError",
        "error": "编号前缀断言失败：期望 'DNA-'，实际 'RNA-'",
        "traceback": """    def test_code_rule02(self, load_code_rules_page, request):
        code = self.generate_code("DNA质粒")
>       assert code.startswith("DNA-"), f"编号前缀断言失败：期望 'DNA-'，实际 {code[:4]!r}..."
E   AssertionError: 编号前缀断言失败：期望 'DNA-'，实际 'RNA-'...

test/testcases/group_management/test_code_rules.py:66: AssertionError
E   备注：该用例上周通过，本周开始失败；编号规则配置未变""",
        "label": "",
    },
    {
        "id": "025",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register05",
        "error_type": "KeyboardInterrupt",
        "error": "",
        "traceback": """    def test_single_register05(self, InCMS_page, request):
        self.fill_register_form(...)

E   KeyboardInterrupt

（测试在 CI 上被手动终止，无失败断言）""",
        "label": "",
    },

    {
        "id": "026",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
>       self.click(("role", "button", "保存记录"))

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for get_by_role("button", name="保存记录")
E     locator resolved to 0 elements
E   ============================================================
E   备注：页面上按钮文案为"保存"，测试代码用"保存记录"（产品最近改过文案）""",
        "label": "",
    },
    {
        "id": "027",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container01",
        "error_type": "AssertionError",
        "error": "容器删除断言失败：删除后列表仍显示 3 个容器",
        "traceback": """    def test_storage_and_container01(self, InCMS_page):
        self.delete_container("容器A")
        count = self.get_container_count()
>       assert count == 2, f"容器删除断言失败：删除后列表仍显示 {count} 个容器"
E   AssertionError: 容器删除断言失败：删除后列表仍显示 3 个容器

test/testcases/enterprise_level_management/test_storage_and_container.py:47: AssertionError""",
        "label": "",
    },
    {
        "id": "028",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up03",
        "error_type": "AssertionError",
        "error": "上传接口响应异常：期望 200，实际 504",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/upload" in r.url) as resp:
            self.upload_file(file_path)
            response = resp.value
>           assert response.status == 200, f"上传接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 上传接口响应异常：期望 200，实际 504

test/testcases/data_up/test_data_up.py:52: AssertionError""",
        "label": "",
    },
    {
        "id": "029",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart03",
        "error_type": "Error",
        "error": "strict mode violation: locator resolved to 2 elements",
        "traceback": """    def test_sample_cart03(self, InCMS_page, request):
        self.open_cart()
>       self.click(("role", "button", "删除"))

E   playwright._impl._errors.Error: strict mode violation: get_by_role("button", name="删除") resolved to 2 elements
E   备注：偶发出现，重跑通过；列表异步加载完成后仅剩 1 个删除按钮""",
        "label": "",
    },
    {
        "id": "030",
        "test_name": "test/testcases/group_management/test_member_permission_management.py::test_member_permission_flow",
        "error_type": "Error",
        "error": "Browser process exited unexpectedly",
        "traceback": """E   playwright._impl._errors.Error: Browser process exited unexpectedly

（无截图、无网络日志，浏览器内核崩溃原因不明）""",
        "label": "",
    },

    {
        "id": "031",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register06",
        "error_type": "AssertionError",
        "error": "必填校验异常：空表单仍可提交成功",
        "traceback": """    def test_single_register06(self, InCMS_page, request):
        self.click(("role", "button", "保存"))
>       assert self.get_error_hint() == "请填写必填项", "必填校验异常：空表单仍可提交成功"
E   AssertionError: 必填校验异常：空表单仍可提交成功
E   （接口断言显示保存接口返回 200，数据已入库）""",
        "label": "",
    },
    {
        "id": "032",
        "test_name": "test/testcases/sample_center/test_assigned_tasks.py::test_assigned_tasks",
        "error_type": "TimeoutError",
        "error": "Timeout 15000ms exceeded.",
        "traceback": """    def test_assigned_tasks(self, InCMS_page):
>       self.wait_for(("selector", ".task-item"), timeout=15000)

E   playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".task-item")
E     locator resolved to 0 elements
E   ============================================================
E   备注：任务中心页面 3 天前改版，DOM 结构已变化""",
        "label": "",
    },
    {
        "id": "033",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_CERT_DATE_INVALID at https://cms-test.example.com",
        "traceback": """    def test_batch_register(self, InCMS_page):
>       self.page.goto(f"{BASE_URL}/batch_register")

E   playwright._impl._errors.Error: Page.goto: net::ERR_CERT_DATE_INVALID at https://cms-test.example.com
E   Call log:
E     - navigating to "https://cms-test.example.com/batch_register", waiting until "load"

test/testcases/data_center/test_batch_register.py:41: Error""",
        "label": "",
    },
    {
        "id": "034",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization03",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_visualization03(self, load_visualization_page):
>       self.click_canvas(160, 120)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("canvas")
E     locator resolved to 1 element
E   ============================================================
E   备注：canvas 已存在但点击后无任何响应；重跑偶发通过""",
        "label": "",
    },
    {
        "id": "035",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container04",
        "error_type": "AssertionError",
        "error": "断言失败：expected '可用' but got '已满'",
        "traceback": """    def test_storage_and_container04(self, InCMS_page):
        status = self.get_container_status()
>       assert status == "可用", f"expected '可用' but got {status!r}"
E   AssertionError: expected '可用' but got '已满'

（日志中无接口请求记录，疑似断言前状态已被其他用例修改）""",
        "label": "",
    },

    {
        "id": "036",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rules03",
        "error_type": "AssertionError",
        "error": "批量编号断言失败：100 个编号中出现重复",
        "traceback": """    def test_code_rules03(self, load_code_rules_page, request):
        codes = self.batch_generate_codes(100)
>       assert len(set(codes)) == 100, f"批量编号断言失败：100 个编号中出现重复"
E   AssertionError: 批量编号断言失败：100 个编号中出现重复
E   （重复编号：SP-202609-057 出现 2 次）""",
        "label": "",
    },
    {
        "id": "037",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "富文本内容断言失败：粘贴的图片未保存",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        self.paste_image_to_editor()
        self.click(("role", "button", "保存"))
>       assert self.editor_contains_image(), "富文本内容断言失败：粘贴的图片未保存"
E   AssertionError: 富文本内容断言失败：粘贴的图片未保存

test/testcases/eln/test_eln.py:112: AssertionError""",
        "label": "",
    },
    {
        "id": "038",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list01",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_CONNECTION_TIMED_OUT at https://cms-test.example.com/sample/list",
        "traceback": """    def test_sample_list01(self, InCMS_page):
>       self.page.goto(f"{BASE_URL}/sample/list")

E   playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_TIMED_OUT at https://cms-test.example.com/sample/list
E   Call log:
E     - navigating to "https://cms-test.example.com/sample/list", waiting until "load"

test/testcases/sample_center/test_sample_list.py:28: Error""",
        "label": "",
    },
    {
        "id": "039",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register04",
        "error_type": "TimeoutError",
        "error": "Timeout 20000ms exceeded.",
        "traceback": """    def test_single_register04(self, InCMS_page):
        self.fill_register_form(...)
        self.click(("role", "button", "保存"))
>       self.wait_for(("selector", ".toast-success"), timeout=20000)

E   playwright._impl._errors.TimeoutError: Timeout 20000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".toast-success")
E     locator resolved to 0 elements
E   ============================================================
E   备注：接口已返回 200，仅成功提示未出现；重跑通过""",
        "label": "",
    },
    {
        "id": "040",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register02",
        "error_type": "AssertionError",
        "error": "断言失败：expected '草稿' but got None",
        "traceback": """    def test_single_register02(self, InCMS_page):
        status = self.get_first_row_status()
>       assert status == "草稿", f"expected '草稿' but got {status!r}"
E   AssertionError: expected '草稿' but got None

（列表接口返回正常，前端表格渲染异常导致取值失败）""",
        "label": "",
    },

    {
        "id": "041",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container03",
        "error_type": "Error",
        "error": "Frame was detached",
        "traceback": """    def test_storage_and_container03(self, InCMS_page):
        self.switch_to_iframe(("selector", "#storage-frame"))
>       self.click(("role", "button", "确定"))

E   playwright._impl._errors.Error: Frame was detached
E   =========================== logs ===========================
E   frame locator("#storage-frame") was detached from the page
E   ============================================================
E   备注：弹窗 iframe 索引写死为 0，本次运行中页面有 2 个 iframe""",
        "label": "",
    },
    {
        "id": "042",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list_search03",
        "error_type": "AssertionError",
        "error": "组合搜索断言失败：期望结果为空，实际 2 条",
        "traceback": """    def test_sample_list_search03(self, InCMS_page):
        self.search({"名称": "质粒X", "状态": "已出库"})
        rows = self.get_table_rows()
>       assert len(rows) == 0, f"组合搜索断言失败：期望结果为空，实际 {len(rows)} 条"
E   AssertionError: 组合搜索断言失败：期望结果为空，实际 2 条
E   （"质粒X"已出库，但搜索返回 2 条"质粒X-1"、"质粒X-2"草稿记录，疑似模糊匹配逻辑错误）""",
        "label": "",
    },
    {
        "id": "043",
        "test_name": "test/testcases/data_center/test_data_export.py::test_export_sdf",
        "error_type": "AssertionError",
        "error": "导出接口响应异常：期望 200，实际 404",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/export/sdf" in r.url) as resp:
            self.click(("role", "button", "导出SDF"))
            response = resp.value
>           assert response.status == 200, f"导出接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 导出接口响应异常：期望 200，实际 404

test/testcases/data_center/test_data_export.py:39: AssertionError""",
        "label": "",
    },
    {
        "id": "044",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template03",
        "error_type": "TimeoutError",
        "error": "Timeout 10000ms exceeded.",
        "traceback": """    def test_create_template03(self, InCMS_page):
        self.open_template_dialog()
        self.fill_form(...)
>       self.click(("role", "button", "保存"))

E   playwright._impl._errors.TimeoutError: Timeout 10000ms exceeded.
E   =========================== logs ===========================
E   waiting for get_by_role("button", name="保存")
E     locator resolved to 1 element
E     element is not stable - it is animating
E   ============================================================
E   备注：保存按钮入场动画未结束导致点击失败，重跑通过""",
        "label": "",
    },
    {
        "id": "045",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up01",
        "error_type": "AssertionError",
        "error": "上传进度断言失败：等待 60s 后进度仍为 99%",
        "traceback": """    def test_single_data_up01(self, InCMS_page, request):
        self.upload_file(file_path)
>       assert self.wait_progress_done(60), "上传进度断言失败：等待 60s 后进度仍为 99%"
E   AssertionError: 上传进度断言失败：等待 60s 后进度仍为 99%

test/testcases/data_up/test_data_up.py:47: AssertionError""",
        "label": "",
    },

    {
        "id": "046",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule02",
        "error_type": "AssertionError",
        "error": "编号日期断言失败：期望 '20260907'，实际 '20260906'",
        "traceback": """    def test_code_rule02(self, load_code_rules_page, request):
        code = self.generate_code("DNA质粒")
>       assert today_str in code, f"编号日期断言失败：期望 {today_str!r}，实际编号为 {code!r}"
E   AssertionError: 编号日期断言失败：期望 '20260907'，实际编号为 'SP-20260906-012'

test/testcases/group_management/test_code_rules.py:70: AssertionError""",
        "label": "",
    },
    {
        "id": "047",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register_with_approval_02",
        "error_type": "AssertionError",
        "error": "审批列表断言失败：期望出现 1 条待审批记录，实际 0 条",
        "traceback": """    def test_single_register_with_approval_02(self, InCMS_page, request):
        self.submit_for_approval("SP-202609-001")
>       assert self.get_approval_count() == 1, "审批列表断言失败：期望出现 1 条待审批记录，实际 0 条"
E   AssertionError: 审批列表断言失败：期望出现 1 条待审批记录，实际 0 条

test/testcases/data_center/test_single_register.py:96: AssertionError""",
        "label": "",
    },
    {
        "id": "048",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "登录态异常：请求返回 401",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/eln/save" in r.url) as resp:
            self.click(("role", "button", "保存"))
            response = resp.value
>           assert response.status == 200, f"登录态异常：请求返回 {response.status}"
E   AssertionError: 登录态异常：请求返回 401

test/testcases/eln/test_eln.py:88: AssertionError""",
        "label": "",
    },
    {
        "id": "049",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list_pagination01",
        "error_type": "AssertionError",
        "error": "翻页断言失败：点击第 2 页后仍显示第 1 页数据",
        "traceback": """    def test_sample_list_pagination01(self, InCMS_page):
        self.click(("selector", ".pagination li:nth-child(3)"))
        first_row = self.get_first_row_name()
>       assert first_row != page1_first_name, "翻页断言失败：点击第 2 页后仍显示第 1 页数据"
E   AssertionError: 翻页断言失败：点击第 2 页后仍显示第 1 页数据
E   备注：分页组件前端逻辑疑似缓存了第一页数据；偶发，重跑通过""",
        "label": "",
    },
    {
        "id": "050",
        "test_name": "test/testcases/group_management/test_member_permission_management.py::test_member_permission_flow",
        "error_type": "Error",
        "error": "Permission denied",
        "traceback": """    def test_member_permission_flow(self, InCMS_page, browser, request, permission_data):
        login_as_member(permission_data["member"])
>       self.page.goto(f"{BASE_URL}/member/manage")

E   playwright._impl._errors.Error: Permission denied

（无接口日志、无页面信息，疑似网关层直接拦截）""",
        "label": "",
    },

    {
        "id": "051",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "KeyError",
        "error": "'batch_no'",
        "traceback": """    def test_batch_register(self, InCMS_page):
        template_data = load_yaml("register_template.yaml")
        for row in template_data:
>           batch_no = row["batch_no"]

E   KeyError: 'batch_no'

test/testcases/data_center/test_batch_register.py:49: KeyError""",
        "label": "",
    },
    {
        "id": "052",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart04",
        "error_type": "AssertionError",
        "error": "领样车数量断言失败：加入 2 个样品后数量仍为 1",
        "traceback": """    def test_sample_cart04(self, InCMS_page, request):
        self.add_to_cart("样品A")
        self.add_to_cart("样品B")
        count = self.get_cart_count()
>       assert count == 2, f"领样车数量断言失败：加入 2 个样品后数量仍为 {count}"
E   AssertionError: 领样车数量断言失败：加入 2 个样品后数量仍为 1

test/testcases/sample_center/test_sample_cart.py:68: AssertionError""",
        "label": "",
    },
    {
        "id": "053",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register01",
        "error_type": "AssertionError",
        "error": "登录接口响应异常：期望 200，实际 429",
        "traceback": """    @pytest.fixture(scope="session")
    def InCMS_page(self, browser):
        page = browser.new_page()
>       with page.expect_response(lambda r: "/api/v1/login" in r.url) as resp:
            page.goto(f"{BASE_URL}/login")
            response = resp.value
>           assert response.status == 200, f"登录接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 登录接口响应异常：期望 200，实际 429

test/conftest.py:52: AssertionError""",
        "label": "",
    },
    {
        "id": "054",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization01",
        "error_type": "TimeoutError",
        "error": "Timeout 15000ms exceeded.",
        "traceback": """    def test_visualization01(self, load_visualization_page, request):
>       self.wait_for(("selector", "canvas"), timeout=15000)

E   playwright._impl._errors.TimeoutError: Timeout 15000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("canvas")
E     locator resolved to 0 elements
E   ============================================================
E   备注：可视化模块依赖的图形服务偶发启动慢，重跑通过""",
        "label": "",
    },
    {
        "id": "055",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "UnicodeDecodeError",
        "error": "'utf-8' codec can't decode byte 0xb5 in position 128: invalid start byte",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        record = load_yaml("eln_record.yaml")
>       content = record["content"]

E   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 128: invalid start byte

test/testcases/eln/test_eln.py:34: UnicodeDecodeError""",
        "label": "",
    },

    {
        "id": "056",
        "test_name": "test/testcases/data_center/test_data_export.py::test_download_register_template_and_compare",
        "error_type": "TimeoutError",
        "error": "Timeout 5000ms exceeded.",
        "traceback": """    def test_download_register_template_and_compare(self, InCMS_page):
        self.click(("role", "button", "下载模板"))
>       self.wait_for_download(timeout=5000)

E   playwright._impl._errors.TimeoutError: Timeout 5000ms exceeded.
E   备注：下载接口正常返回 200，文件较大时生成耗时超过 5 秒，偶发超时""",
        "label": "",
    },
    {
        "id": "057",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "AssertionError",
        "error": "特殊字符保存断言失败：名称 'DNA@#1' 保存后显示乱码",
        "traceback": """    def test_batch_register(self, InCMS_page):
        self.register_material("DNA@#1")
        saved = self.get_material_name()
>       assert saved == "DNA@#1", f"特殊字符保存断言失败：名称 'DNA@#1' 保存后显示 {saved!r}"
E   AssertionError: 特殊字符保存断言失败：名称 'DNA@#1' 保存后显示 'DNA@#1'
E   （显示正常但接口返回数据中编码异常，导出时乱码）""",
        "label": "",
    },
    {
        "id": "058",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list01",
        "error_type": "AssertionError",
        "error": "列表接口响应异常：期望 200，实际 503",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/sample/list" in r.url) as resp:
            self.page.goto(f"{BASE_URL}/sample/list")
            response = resp.value
>           assert response.status == 200, f"列表接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 列表接口响应异常：期望 200，实际 503

test/testcases/sample_center/test_sample_list.py:31: AssertionError""",
        "label": "",
    },
    {
        "id": "059",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template01",
        "error_type": "AssertionError",
        "error": "模板字段断言失败：保存后字段 '备注' 丢失",
        "traceback": """    def test_create_template01(self, InCMS_page):
        self.fill_form({"名称": "模板A", "备注": "测试备注"})
        self.click(("role", "button", "保存"))
        detail = self.get_template_detail()
>       assert detail.get("备注") == "测试备注", "模板字段断言失败：保存后字段 '备注' 丢失"
E   AssertionError: 模板字段断言失败：保存后字段 '备注' 丢失

test/testcases/group_management/test_template_management.py:57: AssertionError""",
        "label": "",
    },
    {
        "id": "060",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container01",
        "error_type": "ImportError",
        "error": "cannot import name 'ContainerPage' from 'object.storage_page'",
        "traceback": """test/testcases/enterprise_level_management/test_storage_and_container.py:5: in <module>
    from object.storage_page import ContainerPage

E   ImportError: cannot import name 'ContainerPage' from 'object.storage_page'""",
        "label": "",
    },

    {
        "id": "061",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart05",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_sample_cart05(self, InCMS_page, request):
        self.click(("selector", ".submit-cart-btn"))
>       self.wait_for(("text", "申领成功"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("text=申领成功")
E     locator resolved to 0 elements
E   ============================================================
E   备注：产品改版后成功提示文案改为"申领提交成功"，提示语硬编码未更新""",
        "label": "",
    },
    {
        "id": "062",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule01",
        "error_type": "AssertionError",
        "error": "编号前缀断言失败：期望 'SP-'，实际 'sp-'",
        "traceback": """    def test_code_rule01(self, load_code_rules_page, request):
        code = self.generate_code("样品")
>       assert code.startswith("SP-"), f"编号前缀断言失败：期望 'SP-'，实际 {code[:4]!r}..."
E   AssertionError: 编号前缀断言失败：期望 'SP-'，实际 'sp-'...

test/testcases/group_management/test_code_rules.py:38: AssertionError""",
        "label": "",
    },
    {
        "id": "063",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "保存接口响应异常：期望 200，实际 500",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/eln/save" in r.url) as resp:
            self.click(("role", "button", "保存"))
            response = resp.value
>           assert response.status == 200, f"保存接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 保存接口响应异常：期望 200，实际 500

test/testcases/eln/test_eln.py:84: AssertionError""",
        "label": "",
    },
    {
        "id": "064",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up02",
        "error_type": "AssertionError",
        "error": "上传结果断言失败：期望 5 条成功，实际 3 条",
        "traceback": """    def test_single_data_up02(self, InCMS_page, request):
        self.upload_file(file_path)
        result = self.get_upload_result()
>       assert result["success"] == 5, f"上传结果断言失败：期望 5 条成功，实际 {result['success']} 条"
E   AssertionError: 上传结果断言失败：期望 5 条成功，实际 3 条
E   备注：结果页显示 2 条"解析失败"，重跑后 5 条全部成功""",
        "label": "",
    },
    {
        "id": "065",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list03",
        "error_type": "AssertionError",
        "error": "assert None is not None",
        "traceback": """    def test_sample_list03(self, InCMS_page):
        detail = self.get_first_row_detail()
>       assert detail is not None

E   AssertionError: assert None is not None

（代码行无自定义报错信息，日志无接口异常）""",
        "label": "",
    },

    {
        "id": "066",
        "test_name": "test/testcases/group_management/test_member_permission_management.py::test_role_permission",
        "error_type": "AssertionError",
        "error": "角色权限断言失败：普通成员可见管理员菜单",
        "traceback": """    def test_role_permission(self, InCMS_page):
        login_as_role("普通成员")
>       assert not self.menu_visible("系统管理"), "角色权限断言失败：普通成员可见管理员菜单"
E   AssertionError: 角色权限断言失败：普通成员可见管理员菜单

test/testcases/group_management/test_member_permission_management.py:121: AssertionError""",
        "label": "",
    },
    {
        "id": "067",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "记录列表断言失败：新建记录未出现在列表",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        self.create_record("实验记录A")
        names = self.get_record_names()
>       assert "实验记录A" in names, "记录列表断言失败：新建记录未出现在列表"
E   AssertionError: 记录列表断言失败：新建记录未出现在列表
E   备注：保存接口返回 200，列表接口日志正常，疑似前端列表缓存未刷新""",
        "label": "",
    },
    {
        "id": "068",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up01",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_CONNECTION_RESET at https://cms-test.example.com/data_up",
        "traceback": """    def test_single_data_up01(self, InCMS_page, request):
>       self.page.goto(f"{BASE_URL}/data_up")

E   playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_RESET at https://cms-test.example.com/data_up

test/testcases/data_up/test_data_up.py:30: Error""",
        "label": "",
    },
    {
        "id": "069",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container02",
        "error_type": "AssertionError",
        "error": "容量限制断言失败：超容量物品仍可入库",
        "traceback": """    def test_storage_and_container02(self, InCMS_page):
        self.store_item("超大体积样品")
>       assert self.get_error_hint() == "超出容器容量", "容量限制断言失败：超容量物品仍可入库"
E   AssertionError: 容量限制断言失败：超容量物品仍可入库
E   （入库接口返回 200，无任何校验拦截）""",
        "label": "",
    },
    {
        "id": "070",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization04",
        "error_type": "AssertionError",
        "error": "导出图片断言失败：导出的图片为空白（文件大小 0 字节）",
        "traceback": """    def test_visualization04(self, load_visualization_page):
        self.draw_on_canvas(...)
        path = self.export_canvas_image()
>       assert os.path.getsize(path) > 0, "导出图片断言失败：导出的图片为空白（文件大小 0 字节）"
E   AssertionError: 导出图片断言失败：导出的图片为空白（文件大小 0 字节）

test/testcases/visualization/test_visualization.py:83: AssertionError""",
        "label": "",
    },

    {
        "id": "071",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register03",
        "error_type": "Error",
        "error": "locator.text_content: 找不到元素",
        "traceback": """    def test_single_register03(self, InCMS_page):
        self.register(...)
>       status = self.get_text(("selector", ".status-badge"))

E   playwright._impl._errors.Error: locator(".status-badge") resolved to 0 elements
E   备注：注册后状态标签类名改版为 ".status-tag"，locator 层未同步更新""",
        "label": "",
    },
    {
        "id": "072",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list_search02",
        "error_type": "AssertionError",
        "error": "搜索结果断言失败：搜索 'RNA' 返回 0 条，期望 2 条",
        "traceback": """    def test_sample_list_search02(self, InCMS_page):
        self.search("RNA")
        rows = self.get_table_rows()
>       assert len(rows) == 2, f"搜索结果断言失败：搜索 'RNA' 返回 {len(rows)} 条，期望 2 条"
E   AssertionError: 搜索结果断言失败：搜索 'RNA' 返回 0 条，期望 2 条

test/testcases/sample_center/test_sample_list.py:55: AssertionError""",
        "label": "",
    },
    {
        "id": "073",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template04",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_SSL_PROTOCOL_ERROR at https://cms-test.example.com",
        "traceback": """    def test_create_template04(self, InCMS_page):
>       self.page.goto(f"{BASE_URL}/template/list")

E   playwright._impl._errors.Error: Page.goto: net::ERR_SSL_PROTOCOL_ERROR at https://cms-test.example.com
E   Call log:
E     - navigating to "https://cms-test.example.com/template/list", waiting until "load"

test/testcases/group_management/test_template_management.py:29: Error""",
        "label": "",
    },
    {
        "id": "074",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register01",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_single_register01(self, InCMS_page):
        self.fill_register_form(...)
        self.click(("role", "button", "保存"))
>       self.wait_for(("text", "注册成功"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("text=注册成功")
E     locator resolved to 0 elements
E   ============================================================
E   备注：接口返回 200 且数据入库；提示语偶发不展示（前端通知组件竞态），重跑通过""",
        "label": "",
    },
    {
        "id": "075",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule01",
        "error_type": "AssertionError",
        "error": "assert 'SP-202609-001' == ''",
        "traceback": """    def test_code_rule01(self, load_code_rules_page, request):
        code = self.get_generated_code()
>       assert code == "SP-202609-001"

E   AssertionError: assert 'SP-202609-001' == ''
E   （取值为空串，页面元素存在但渲染时机异常；日志无其他信息）""",
        "label": "",
    },

    {
        "id": "076",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart01",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_sample_cart01(self, InCMS_page, request):
        self.add_to_cart("DNA质粒001")
>       self.click(("role", "button", "去结算"))

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for get_by_role("button", name="去结算")
E     locator resolved to 0 elements
E   ============================================================
E   备注：按钮文案已改为"提交申领"，测试脚本未更新""",
        "label": "",
    },
    {
        "id": "077",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "自动保存断言失败：编辑 5 分钟后未触发自动保存",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        self.edit_record(...)
        time.sleep(5 * 60)
>       assert self.autosave_flag_visible(), "自动保存断言失败：编辑 5 分钟后未触发自动保存"
E   AssertionError: 自动保存断言失败：编辑 5 分钟后未触发自动保存

test/testcases/eln/test_eln.py:118: AssertionError""",
        "label": "",
    },
    {
        "id": "078",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register04",
        "error_type": "AssertionError",
        "error": "保存接口响应异常：期望 200，实际 502",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/register" in r.url) as resp:
            self.click(("role", "button", "保存"))
            response = resp.value
>           assert response.status == 200, f"保存接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 保存接口响应异常：期望 200，实际 502

test/testcases/data_center/test_single_register.py:60: AssertionError""",
        "label": "",
    },
    {
        "id": "079",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register_with_approval_01",
        "error_type": "AssertionError",
        "error": "审批操作断言失败：审批人列表为空",
        "traceback": """    def test_single_register_with_approval_01(self, InCMS_page, request):
        self.open_approval_dialog()
        approvers = self.get_approver_list()
>       assert approvers, "审批操作断言失败：审批人列表为空"
E   AssertionError: 审批操作断言失败：审批人列表为空
E   备注：偶发；审批人数据依赖上游同步任务，同步延迟时列表为空""",
        "label": "",
    },
    {
        "id": "080",
        "test_name": "test/testcases/data_center/test_data_export.py::test_export_sdf",
        "error_type": "AssertionError",
        "error": "断言失败：expected 24.5 but got None",
        "traceback": """    def test_export_sdf(self, InCMS_page, view_mode):
        weight = self.get_first_row_weight()
>       assert weight == 24.5, f"expected 24.5 but got {weight!r}"
E   AssertionError: expected 24.5 but got None

（无接口日志；页面元素定位成功但文本为空）""",
        "label": "",
    },

    {
        "id": "081",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization01",
        "error_type": "AssertionError",
        "error": "画布导出断言失败：点击导出后无下载触发",
        "traceback": """    def test_visualization01(self, load_visualization_page, request):
        self.draw_on_canvas(...)
>       with self.page.expect_download() as dl:
            self.click_canvas(380, 200)
        E   AssertionError: 画布导出断言失败：点击导出后无下载触发
        E   （点击坐标与导出按钮位置偏差，分辨率差异导致）""",
        "label": "",
    },
    {
        "id": "082",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template05",
        "error_type": "AssertionError",
        "error": "模板列表断言失败：删除后仍显示 '模板B'",
        "traceback": """    def test_create_template05(self, InCMS_page):
        self.delete_template("模板B")
        names = self.get_template_names()
>       assert "模板B" not in names, "模板列表断言失败：删除后仍显示 '模板B'"
E   AssertionError: 模板列表断言失败：删除后仍显示 '模板B'

test/testcases/group_management/test_template_management.py:74: AssertionError""",
        "label": "",
    },
    {
        "id": "083",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart06",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_CONNECTION_REFUSED at http://cms-test.example.com:8080",
        "traceback": """    def test_sample_cart06(self, InCMS_page, request):
>       self.page.goto(f"{BASE_URL}:8080/cart")

E   playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://cms-test.example.com:8080
E   备注：environment.yaml 中 base_url 端口配置错误""",
        "label": "",
    },
    {
        "id": "084",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list04",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_sample_list04(self, InCMS_page):
        self.apply_filter({"类型": "全部"})
>       self.wait_for(("selector", ".table-row"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".table-row")
E     locator resolved to 0 elements
E   ============================================================
E   备注：连续失败 3 次后第 4 次通过；列表接口偶发返回空数组""",
        "label": "",
    },
    {
        "id": "085",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up03",
        "error_type": "AssertionError",
        "error": "文件校验断言失败：上传 .xlsx 文件被提示格式不支持",
        "traceback": """    def test_single_data_up03(self, InCMS_page, request):
        self.upload_file("sample.xlsx")
>       assert self.get_error_hint() is None, f"文件校验断言失败：上传 .xlsx 文件被提示格式不支持"
E   AssertionError: 文件校验断言失败：上传 .xlsx 文件被提示格式不支持
E   （需求文档明确支持 .xlsx 格式）""",
        "label": "",
    },

    {
        "id": "086",
        "test_name": "test/testcases/group_management/test_code_rules.py::test_code_rule03",
        "error_type": "AssertionError",
        "error": "编号规则断言失败：实际 'SP-20260907-001'，期望 'SP-20260906-001'",
        "traceback": """    def test_code_rule03(self, load_code_rules_page, request):
        code = self.generate_code("样品")
>       assert code == "SP-20260906-001", f"编号规则断言失败：实际 {code!r}，期望 'SP-20260906-001'"
E   AssertionError: 编号规则断言失败：实际 'SP-20260907-001'，期望 'SP-20260906-001'
E   备注：期望值硬编码为昨天的日期，跨天执行必挂""",
        "label": "",
    },
    {
        "id": "087",
        "test_name": "test/testcases/sample_center/test_assigned_tasks.py::test_assigned_tasks",
        "error_type": "AssertionError",
        "error": "任务分配断言失败：分配后接收方任务列表仍为空",
        "traceback": """    def test_assigned_tasks(self, InCMS_page):
        self.assign_task("任务A", "成员B")
        login_as("成员B")
        tasks = self.get_task_names()
>       assert tasks, "任务分配断言失败：分配后接收方任务列表仍为空"
E   AssertionError: 任务分配断言失败：分配后接收方任务列表仍为空

test/testcases/sample_center/test_assigned_tasks.py:57: AssertionError""",
        "label": "",
    },
    {
        "id": "088",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "登录接口响应异常：期望 200，实际 503",
        "traceback": """    @pytest.fixture(scope="session")
    def InELN_page(self, browser):
>       with browser.new_page() as page:
            with page.expect_response(lambda r: "/api/v1/login" in r.url) as resp:
                page.goto(f"{BASE_URL}/eln")
                response = resp.value
>               assert response.status == 200, f"登录接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 登录接口响应异常：期望 200，实际 503

test/conftest.py:66: AssertionError""",
        "label": "",
    },
    {
        "id": "089",
        "test_name": "test/testcases/enterprise_level_management/test_storage_and_container.py::test_storage_and_container04",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_storage_and_container04(self, InCMS_page):
        self.click(("role", "button", "新建容器"))
>       self.wait_for(("selector", ".container-form"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".container-form")
E     locator resolved to 0 elements
E   ============================================================
E   备注：偶发失败，重跑通过；无接口异常日志""",
        "label": "",
    },
    {
        "id": "090",
        "test_name": "test/testcases/data_center/test_batch_register.py::test_batch_register",
        "error_type": "Error",
        "error": "Response payload is not completed",
        "traceback": """    def test_batch_register(self, InCMS_page):
>       with self.page.expect_response(lambda r: "/api/v1/batch_register" in r.url) as resp:
            self.click(("role", "button", "提交"))
            response = resp.value

E   playwright._impl._errors.Error: Response payload is not completed

（浏览器控制台无报错，网络日志中断）""",
        "label": "",
    },

    {
        "id": "091",
        "test_name": "test/testcases/group_management/test_member_permission_management.py::test_role_permission",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_role_permission(self, InCMS_page):
        login_as_role("管理员")
>       self.wait_for(("selector", ".menu-item"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".menu-item")
E     locator resolved to 0 elements
E   ============================================================
E   备注：菜单改版后类名变更为 ".nav-item"，locator 未同步""",
        "label": "",
    },
    {
        "id": "092",
        "test_name": "test/testcases/sample_center/test_sample_cart.py::test_sample_cart07",
        "error_type": "AssertionError",
        "error": "申领数量断言失败：可申领库存为 0 时仍可提交",
        "traceback": """    def test_sample_cart07(self, InCMS_page, request):
        self.add_to_cart("零库存样品")
        self.submit_cart()
>       assert self.get_error_hint() == "库存不足", "申领数量断言失败：可申领库存为 0 时仍可提交"
E   AssertionError: 申领数量断言失败：可申领库存为 0 时仍可提交
E   （提交接口返回 200，申领单已生成）""",
        "label": "",
    },
    {
        "id": "093",
        "test_name": "test/testcases/data_center/test_data_export.py::test_export_excel_and_compare",
        "error_type": "Error",
        "error": "Page.goto: net::ERR_NETWORK_CHANGED at https://cms-test.example.com/data_center",
        "traceback": """    def test_export_excel_and_compare(self, InCMS_page, view_mode):
>       self.page.goto(f"{BASE_URL}/data_center")

E   playwright._impl._errors.Error: Page.goto: net::ERR_NETWORK_CHANGED at https://cms-test.example.com/data_center

test/testcases/data_center/test_data_export.py:27: Error""",
        "label": "",
    },
    {
        "id": "094",
        "test_name": "test/testcases/visualization/test_visualization.py::test_visualization02",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_visualization02(self, load_visualization_page):
>       self.click_canvas(320, 240)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator("canvas")
E     locator resolved to 0 elements
E   ============================================================
E   备注：画布组件加载依赖 CDN 资源，CDN 不稳定时画布偶发加载失败""",
        "label": "",
    },
    {
        "id": "095",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register05",
        "error_type": "Error",
        "error": "Process finished with exit code 137",
        "traceback": """E   Process finished with exit code 137 (OOM killed)

（CI 节点内存耗尽，测试进程被系统杀死，无 traceback）""",
        "label": "",
    },

    {
        "id": "096",
        "test_name": "test/testcases/data_up/test_data_up.py::test_single_data_up01",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_single_data_up01(self, InCMS_page, request):
>       self.click(("role", "button", "选择文件"))

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for get_by_role("button", name="选择文件")
E     locator resolved to 0 elements
E   ============================================================
E   备注：上传页改版，按钮文案改为"上传文件"，测试脚本未更新""",
        "label": "",
    },
    {
        "id": "097",
        "test_name": "test/testcases/group_management/test_template_management.py::test_create_template06",
        "error_type": "AssertionError",
        "error": "模板排序断言失败：新建模板未排在首位",
        "traceback": """    def test_create_template06(self, InCMS_page):
        self.create_template("模板C")
        first = self.get_first_template_name()
>       assert first == "模板C", "模板排序断言失败：新建模板未排在首位"
E   AssertionError: 模板排序断言失败：新建模板未排在首位
E   （列表实际按更新时间倒序，需求未明确排序规则，需求文档待确认）""",
        "label": "",
    },
    {
        "id": "098",
        "test_name": "test/testcases/data_center/test_single_register.py::test_single_register02",
        "error_type": "AssertionError",
        "error": "列表接口响应异常：期望 200，实际 504",
        "traceback": """>       with self.page.expect_response(lambda r: "/api/v1/material/list" in r.url) as resp:
            self.page.goto(f"{BASE_URL}/data_center")
            response = resp.value
>           assert response.status == 200, f"列表接口响应异常：期望 200，实际 {response.status}"
E   AssertionError: 列表接口响应异常：期望 200，实际 504

test/testcases/data_center/test_single_register.py:35: AssertionError""",
        "label": "",
    },
    {
        "id": "099",
        "test_name": "test/testcases/sample_center/test_sample_list.py::test_sample_list05",
        "error_type": "TimeoutError",
        "error": "Timeout 30000ms exceeded.",
        "traceback": """    def test_sample_list05(self, InCMS_page):
        self.search("质粒")
>       self.wait_for(("selector", ".table-row"), timeout=30000)

E   playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
E   =========================== logs ===========================
E   waiting for locator(".table-row")
E     locator resolved to 0 elements
E   ============================================================
E   备注：测试数据前置用例未执行（依赖链路被跳过），库中无"质粒"数据""",
        "label": "",
    },
    {
        "id": "100",
        "test_name": "test/testcases/eln/test_eln.py::test_create_eln_record",
        "error_type": "AssertionError",
        "error": "assert '已保存' == '保存中'",
        "traceback": """    def test_create_eln_record(self, InELN_page, request):
        status = self.get_save_status()
>       assert status == "已保存"

E   AssertionError: assert '已保存' == '保存中'
E   （断言时机早于保存完成；无接口日志）""",
        "label": "",
    },
]
