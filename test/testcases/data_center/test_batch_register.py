from data.pydantic.data_center.batch_register import BatchRegisterData
from object.common import CommonPage
from object.data_center.batch_register import BatchRegisterPage
from utils.log import logger

import allure
import pytest


@allure.epic("数据中心")
@allure.feature("批量注册")
class TestBatchRegister:

    _EXPECTED_TEMPLATE_HEADERS = [
        "63486_0", "0_smiles", "0_isomer_type", "0_sequence", "0_submit_mass",
        "0_salt_id", "0_salt_number", "0_sol_id", "0_sol_number",
        "0_purity", "0_barcode", "0_type", "0_code",
        "6381_29578", "6382_name", "6382_UniprotACC",
        "6384_2108", "6384_2109", "6384_2110",
        "6385_2721", "6385_2722", "6385_2723", "6385_2724", "6385_2725", "6385_2726", "6385_2727",
        "6386_5461", "6386_5462", "6386_5463", "6386_5464", "6386_5465", "6386_5466", "6386_5467", "6386_5468", "6386_5469",
        "6387_825", "6387_826",
        "6388_913", "6388_914",
    ]

    _EXPECTED_TEMPLATE_FIELDS = [
        "*批号(带星号的为必填列)", "SMILES/Mol", "异构体类型", "序列（多个用双竖线分隔）",
        "*注册的量[数字+体积或质量单位(L/ml/g/mg等)]",
        "盐型", "成盐数量", "溶剂", "溶剂数量",
        "纯度", "条形码", "类型", "代号", "自动化测试参数",
        "Name(如果有多组数据，请用 || 隔开)", "UniprotACC(如果有多组数据，请用 || 隔开)",
        "字段1(如果有多组数据，请用 || 隔开)", "字段2(如果有多组数据，请用 || 隔开)",
        "自动化测试参数(如果有多组数据，请用 || 隔开)",
        "实验批号(如果有多组数据，请用 || 隔开)", "样品浓度(mg/mL)(如果有多组数据，请用 || 隔开)",
        "IC50(μmol/L)(如果有多组数据，请用 || 隔开)", "实验对象(如果有多组数据，请用 || 隔开)",
        "Inhibition(%)(如果有多组数据，请用 || 隔开)", "pIC50(如果有多组数据，请用 || 隔开)",
        "自动化测试参数(如果有多组数据，请用 || 隔开)",
        "颜色", "形态", "熔点(℃)", "沸点(℃)", "密度(g/mL)", "溶解性(mg/mL)", "旋光性", "存储条件", "自动化测试参数",
        "实验名称", "实验结果", "字段一", "字段二",
        "样品ID（未填写默认由系统自动生成）", "样品名称",
        "当前的量（未填写默认为注册的量）",
        "容器ID（未填写默认由系统自动生成）",
        "样品管/孔板类型（未填写默认为通用样品管）",
        "孔位（样品管/孔板类型为孔板时可填，未填写则默认放入第一个空白空位）",
        "最末级库位ID",
        "盒内位置坐标（最末级库位为盒子时可填，未填写则默认放入第一个空位置）",
    ]

    @allure.title("下载批量注册模板并与预期比对")
    @pytest.mark.order(64)
    def test_download_register_template_and_compare(self, InCMS_page):
        logger.info("==================== test_download_register_template_and_compare started ====================")
        batch_page = BatchRegisterPage(InCMS_page)
        batch_page.enter_batch_register()
        wb = batch_page.download_register_template()
        assert wb is not None, "批量注册模板下载失败"
        diffs = CommonPage.compare_template_to_expected(
            wb, self._EXPECTED_TEMPLATE_HEADERS, self._EXPECTED_TEMPLATE_FIELDS
        )
        assert diffs == [], f"下载的模板与预期模板不一致，差异详情: {diffs}"
        logger.info("==================== test_download_register_template_and_compare passed ====================")

    @allure.title("批量注册")
    @pytest.mark.order(65)
    def test_batch_register(self, InCMS_page):
        logger.info("==================== test_batch_register started ====================")
        data = BatchRegisterData.get_data()
        batch_number = data.batch_number

        batch_page = BatchRegisterPage(InCMS_page)
        batch_page.enter_batch_register()
        # 设置自动提交与登记选项
        batch_page.setup_auto_submit_and_register()
        # 生成批量注册 Excel
        file_path = batch_page.generate_register_excel(
            self._EXPECTED_TEMPLATE_HEADERS,
            self._EXPECTED_TEMPLATE_FIELDS,
            batch_number,
            data.smiles,
            data.register_amount,
        )
        logger.debug(f"生成的文件路径: {file_path}")
        # 上传批量注册 Excel
        batch_page.upload_register_excel(file_path)
        # 验证物质是否注册成功
        batch_page.wait_for_download_complete()
        batch_page.assert_material_exists(batch_number)
        logger.info("==================== test_batch_register passed ====================")
