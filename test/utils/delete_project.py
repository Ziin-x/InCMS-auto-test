# from playwright.sync_api import sync_playwright
#
# from test.case30_43.pages.object.fixture_object.login_page import Login_Page_object
# from test.case30_43.pages.object.project.project_page import project_object
# from config.settings import test_normal_username, test_normal_password,PROJECT_PAGE
#
# def test_delete_project():
#     delete_project()
#
# def delete_project():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         login_page = Login_Page_object(page)
#         login_page.goto()
#         login_page.login(test_normal_username, test_normal_password)
#         page.wait_for_timeout(5000)
#         page.goto(PROJECT_PAGE)
#         project_page = project_object(page)
#         project_page.delete_project()
#         project_page.page.wait_for_timeout(2000)
#         browser.close()