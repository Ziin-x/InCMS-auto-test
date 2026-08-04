import os

#项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 环境配置
logininfo = {
    "plug":{"url":"https://plug.ineln.com/site/login-account",
            "username":"xurui",
            "password":"xurui667786354"},
    "splug":{"url":"https://splug.ineln.com/site/login-account",
            "username":"xiaoxia.x.zhang",
            "password":"123abc,zhang"},
    "otherenv":{"url":"",
            "username":"",
            "password":""}
}

#日志配置
LOG_CONFIG = {
    'name':'pyUI_web',
    'file':os.path.join(BASE_DIR,'outputs','pyUI_web.log'),
    'fmt':'%(levelname)s %(asctime)s [%(filename)s-->line:%(lineno)d]:%(message)s',
    'debug':True
}

#测试用例路径
TEST_CASES_DIR =  os.path.join(BASE_DIR,'cases')

#错误截图路径
ERROR_SCREENSHOT_DIR = os.path.join(BASE_DIR,'outputs','screenshot')

#测试数据存储路径
test_data_dir = os.path.join(BASE_DIR, 'testcases')

#报告相关
ALLURE_RESULTS_DIR = os.path.join(BASE_DIR,'outputs','allure-results')
ALLURE_REPORT_DIR = os.path.join(BASE_DIR,'outputs','allure-report')

# yaml文件前置路径
YAML_PREFIX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','yaml_data')
#参数
PYTEST_ARGS = [
    '-v',          # 详细输出
    '--tb=short',  # 简短回溯
    '-s',          # 显示输出
]

#模版创建接口
TemplateCreateAPI = "https://plugnewcms.ineln.com/fields/ajax-save-template"

# 项目id接口
ProjectIdAPI = "https://pluginproject.ineln.com/api/project/getSimpleProjectList"

# 项目操作接口
ProjectAPI = "https://pluginproject.ineln.com/api/project/operateProjectSubmit"

# 项目创建接口
ProjectCreateAPI = "https://plugnewcms.ineln.com/management/ajax-add-project"

#编号规则保存接口
NumberRuleSaveAPI = "https://plugnewcms.ineln.com/sample-management/save-serial-number-config"

# 自动生成批号保存接口
AutoBatchMemberSaveAPI = "https://plugnewcms.ineln.com/sample-management/save-batch-number-config"

#样品ID接口
SampleIDSaveAPI = "https://plugnewcms.ineln.com/sample/save-sample-number-config"

# 单个注册物质接口
SingleRegistrationSubstanceAPI = "https://plugnewcms.ineln.com/chem-substance/record-chemical-info"

# 样品登记接口
SampleRegisterAPI = "https://plugnewcms.ineln.com/sample/sample-register"

#样品列表接口
SampleListAPI = "https://plugnewcms.ineln.com/sample/get-sample-list"

# 保存审核设置接口
SaveReviewSettingAPI = "https://plugnewcms.ineln.com/management/save-submit-setting"

# 配置注册权限接口
ConfigRegisterPermissionAPI = "https://plugnewcms.ineln.com/auth/set-project-and-modules"

# 同意样品审批接口
ApprovalSampleApprovalAPI = "https://plugnewcms.ineln.com/sample-approval/agree-approval"

# 拒绝样品审批接口
RejectSampleApprovalAPI = "https://plugnewcms.ineln.com/sample-approval/refuse-approval"

# 通用配置保存状态接口
SaveGeneralConfigurationAPI = "https://plugnewcms.ineln.com/request/save-sample-request-process-config"

# 样品申领接口
SampleRequestAPI = "https://plugnewcms.ineln.com/request/submit-request"

#申领数据接口
SampleRequestDataAPI = "https://plugnewcms.ineln.com/request/get-request-record-info"

#归还样品接口
ReturnSampleAPI = "https://plugnewcms.ineln.com/request/return-sample"

#请求接收接口
RequestReceiveAPI = "https://plugnewcms.ineln.com/request/receive-request"

#完成拣货接口
CompletePickUpAPI = "https://plugnewcms.ineln.com/outbound/complete-picking"

#完成出库接口
CompleteOutboundAPI = "https://plugnewcms.ineln.com/outbound/confirm-outbound"

#删除领样车物品接口
DeleteSampleCartItemAPI = "https://plugnewcms.ineln.com/request/delete-request-sample-cart-by-ids"

# 获取角色权限
GetRolePermissionAPI = "https://plugnewcms.ineln.com/auth/get-group-roles"

# 获取分配任务列表
GetAssignedTaskAPI = "https://plugnewcms.ineln.com/assign-task/get-assigned-task"

# 数据中心物质列表接口
MaterialListAPI = "https://plugnewcms.ineln.com/center/get-material-list"





