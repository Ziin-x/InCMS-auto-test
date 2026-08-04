from config.environments_pydantic import Environment
from data.pydantic.sample_center.assigned_tasks import AssignedTasksData
from object.common import CommonPage
from object.sample_center.assigned_tasks import AssignedTasksPage

import allure
import pytest

from utils.log import logger


@allure.epic("样品中心")
@allure.feature("分配的任务")
class TestAssignedTasks:

    data = AssignedTasksData.get_data()
    approval_user = Environment.get_data().username

    @allure.title("进入分配的任务界面，编辑任务状态并验证")
    @pytest.mark.order(43)
    def test_assigned_tasks(self, InCMS_page):
        logger.info("==================== test_assigned_tasks01 started ====================")
        assigned_tasks_page = AssignedTasksPage(InCMS_page)
        assigned_tasks_page.enter_assigned_tasks()
        # 任务在 order=34 test_sample_list02 中通过 request_record_page.assign_task() 分配
        CommonPage.sort_by_request_time_desc(assigned_tasks_page)
        assigned_tasks_page.toggle_task_status()
        logger.info("==================== test_assigned_tasks over =======================")
