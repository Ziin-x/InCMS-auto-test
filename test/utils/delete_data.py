import json
from test.case30_43.pages.object.fixture_object.inproject import \
    inproject_object
from test.case30_43.pages.object.fixture_object.login_page import \
    Login_Page_object
from config.settings import (project_delete_api, project_list_api,
                                  task_id_api, test_normal_password,
                                  test_normal_username, work_report_delete_api,
                                  work_report_list_api, work_time_delete_api)
from test.conftest import data_file
from utils.log import logger

from playwright.sync_api import sync_playwright


def test_delete_data():
    delete_data()

def delete_data():
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    with sync_playwright() as p:
        project_name_list = data.get("project_name",[])
        project_code_list = data.get("project_code",[])
        task_name_list = data.get("task_name",[])
        work_report_list = data.get("work_report",[])
        if not project_name_list or not project_code_list:
            logger.error("没有记录到项目名称或编码")
        if not task_name_list:
            logger.error("没有记录到任务名称")
        if not work_report_list:
            logger.error("没有记录到工作汇报")
        project_name = project_name_list[0]
        project_code = project_code_list[0]
        task_name = task_name_list[0]
        work_report = work_report_list[0]
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        login_page = Login_Page_object(page)
        login_page.goto()
        login_page.login(test_normal_username, test_normal_password)
        inproject_page = inproject_object(page)
        inproject_page.goto_project()
        project_id = get_project_id(project_name, inproject_page.page)
        print(project_id)
        delete_project(project_id, project_code,project_name,inproject_page.page)
        task_id = None
        task_id = get_task_id(project_id, task_name, inproject_page.page)
        delete_work_time(payload1, task_id, inproject_page.page)
        delete_work_time(payload2, task_id, inproject_page.page)
        work_report_id = get_work_report_id(work_report, inproject_page.page)
        delete_work_report(work_report_id, inproject_page.page)


# def get_session(self):
#     session = requests.Session()
#     session.cookies.update(self.cookies)
#     session.headers.update({"Authorization": f"{self.token}"})
#     self.session = session
#
# def get_cookies(self,page):
#     logger.debug("开始获取cookie")
#     try:
#         logger.debug("开始获取cookie并处理")
#         cookies_original = page.context.cookies()
#         if cookies_original != None:
#             logger.info("获取cookie成功")
#         else:
#             logger.error("获取cookie失败")
#     except Exception as e:
#         raise e
#     cookies = {c['name']:c['value'] for c in cookies_original}
#     return cookies
#
# def get_token(self,page):
#     try:
#         logger.debug("开始获取token并处理")
#         token = page.evaluate("() => localStorage.getItem('token')")
#         if not token:
#             token = page.evaluate("() => sessionStorage.getItem('token')")
#         if token != None:
#             logger.info("获取token成功")
#         else:
#             logger.error("获取token失败")
#     except Exception as e:
#         raise e
#     return token

def get_project_id(project_name, page):
    print(f"请求的URL: {project_list_api}")
    payload = {}
    response = page.request.post(project_list_api, data=payload)
    if response.status == 200:
        logger.info("获取项目列表成功")
    else:
        logger.error(f"获取项目列表失败，获取到的响应为{response.json()}")
        print(response.json()['data'])
    data = response.json()['data']
    for i in data:
        if i['name'] == project_name:
            logger.info(f"获取项目id为{i}")
            return i['id']


def delete_project(project_id,project_code,project_name, page):
    payload = {
        "project_data": [
            {
                "project_id": project_id,
                "reason": "",
                "approval_node_list": [],
                "attachment": "",
                "start_time": "",
                "end_time": "",
                "end_type": None,
                "code":project_code,
                "name":project_name
            }
        ],
        "operate_type": "project_delete"
    }
    response = page.request.post(project_delete_api, data=payload)
    logger.info(f"删除的项目名称: {project_name}")
    print(response.json())

def get_task_id(project_id,task_name,page):
    print(f"请求的URL: {task_id_api}")
    payload =  {
        "from":1,
        "itemId": project_id
    }
    response = page.request.post(task_id_api, data=payload)
    if response.status == 200:
        logger.info("获取任务列表成功")
    else:
        logger.error(f"获取任务列表失败，获取到的响应为{response.json()}")
        # 打印响应对象的类型
    print(response.json())
    data = response.json()['data']['taskList']
    for i in data:
        if i['name'] == task_name:
            logger.info(f"获取任务id为{i}")
            return i['id']


ts1 = 1766937600000   # 2025-12-29 UTC
ts2 = 1767024000000   # 2025-12-30 UTC
payload1 = {
    "reason": "",
    "reqs": [
        {
            "date": str(ts1),
            "data": [{
                "taskId": None,
                "value": 0
            }]
        }
    ],
}
payload2 = {
    "reason": "",
    "reqs": [
        {
            "date": str(ts2),
            "data": [{
                "taskId": None,
                "value": 0
            }]
        }
    ],
}
def delete_work_time(payload,task_id,page):
    print(f"请求的URL: {work_time_delete_api}")
    payload["reqs"][0]["data"][0]["taskId"] = task_id
    response = page.request.post(work_time_delete_api, data=payload)
    if response.status == 200:
        logger.info("删除工时成功")
    else:
        logger.error(f"未工时，获取到的响应为{response.json()}")
        print(response.json())

def get_work_report_id(work_report_name,page):
    print(f"请求的URL: {work_report_list_api}")
    payload = {}
    response = page.request.post(work_report_list_api, data=payload)
    if response.status == 200:
        logger.info("获取汇报列表成功")
    else:
        logger.error(f"获取汇报列表失败，获取到的响应为{response.json()}")
    print(response.json()['data']['dataList'])
    data = response.json()['data']['dataList']
    for i in data:
        if i['name'] == work_report_name:
            logger.info(f"获取汇报id为{i['id']}，name={i['name']}")
            return i['id']

def delete_work_report(work_report_id,page):
    payload = {
        "id":[work_report_id],
        "type":0
    }
    print(f"请求的URL: {work_report_delete_api}")
    response = page.request.post(work_report_delete_api, data=payload)
    if response.status == 200:
        logger.info("删除汇报成功")
    else:
        logger.error(f"删除汇报失败，获取到的响应为{response.json()}")
        print(response.json())

def test_delete():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        login_page = Login_Page_object(page)
        login_page.goto()
        login_page.login(test_normal_username, test_normal_password)
        inproject_page = inproject_object(page)
        inproject_page.goto_project()
        work_report_id = get_work_report_id("接口自动化报告删除测试05251",page)
        print(work_report_id)
        delete_work_report(work_report_id,page)
