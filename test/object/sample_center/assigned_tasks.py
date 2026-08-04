import allure

from config.setting import GetAssignedTaskAPI
from locator.InCMS import InCMSLocator
from locator.sample_center.assigned_tasks import AssignedTasksLocator
from object.basepage import BasePage
from utils.log import logger


class AssignedTasksPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @allure.step("进入分配的任务界面")
    def enter_assigned_tasks(self):
        self.ensure_dropdown_expanded(InCMSLocator.sample_center, InCMSLocator.assigned_tasks)
        self.click(InCMSLocator.assigned_tasks)
        self.wait_for(AssignedTasksLocator.assert_assigned_tasks, "visible")
        logger.info("已成功进入分配的任务界面")

    @allure.step("选中第一个任务")
    def select_first_task(self):
        self.click_canvas(AssignedTasksLocator.select_first_task)
        logger.info("已选中第一个任务")

    def _get_newest_task(self, data_list):
        """遍历任务列表，按自增 id 找最新任务"""
        return max(data_list, key=lambda x: int(x['id']))

    @allure.step("切换最新任务状态并验证")
    def toggle_task_status(self):
        """遍历取最新任务 → 读取完成状态 → 点击按钮切换 → 接口验证"""
        # 1. 获取任务列表
        self.page.wait_for_timeout(3000)
        response = self.page.request.get(GetAssignedTaskAPI, params={})
        if response.status != 200:
            raise RuntimeError(f"获取分配任务列表失败，响应状态码：{response.status}")

        data_list = response.json()['data']['dataList']
        if not data_list:
            raise RuntimeError("分配任务列表为空，无法执行状态切换")

        # 2. 遍历取最新（按自增 id）
        newest_task = self._get_newest_task(data_list)
        current_status = newest_task['finish_status']  # "0"=未完成, "1"=已完成

        logger.info(f"最新任务 id={newest_task['id']}, apply_id={newest_task['apply_id']}, "
                    f"当前状态 finish_status={current_status}")

        # 3. 选中第一个任务（画布相对坐标）
        self.select_first_task()

        # 4. 根据当前状态点击对应按钮切换
        if current_status == "0":
            self.click(AssignedTasksLocator.mark_complete_btn)
            expected_new_status = "1"
            logger.info("当前为未完成，点击「标记为完成」")
        else:
            self.click(AssignedTasksLocator.mark_incomplete_btn)
            expected_new_status = "0"
            logger.info("当前为已完成，点击「标记为未完成」")

        self.page.wait_for_timeout(2000)

        # 5. 再次调用接口验证状态变更
        response2 = self.page.request.get(GetAssignedTaskAPI, params={})
        if response2.status != 200:
            raise RuntimeError(f"验证接口调用失败，响应状态码：{response2.status}")

        data_list2 = response2.json()['data']['dataList']
        updated_task = self._get_newest_task(data_list2)
        actual_status = updated_task['finish_status']

        logger.info(f"切换后状态 finish_status={actual_status}, 期望={expected_new_status}")
        assert actual_status == expected_new_status, \
            f"任务状态切换失败！期望 finish_status={expected_new_status}，实际={actual_status}"
        logger.info("任务状态切换成功")
