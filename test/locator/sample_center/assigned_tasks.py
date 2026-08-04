class AssignedTasksLocator:
    # 断言-分配的任务界面
    assert_assigned_tasks = ("selector", ".main-top-title", {"has_text": "分配的任务"})
    # 选择第一个任务
    select_first_task = (("selector", ".inform-content .konvajs-content canvas"), (35, 54))
    # 标记为完成
    mark_complete_btn = ("role", "button", "标记为完成")
    # 标记为未完成
    mark_incomplete_btn = ("role", "button", "标记为未完成")