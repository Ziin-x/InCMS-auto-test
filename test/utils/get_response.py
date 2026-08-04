from utils.log import logger

import allure


@allure.step("获取响应")
def get_response(page, action, url, wait_time=10):


    logger.debug(f"开始监听 {url}，等待动作执行...")
    responses = []

    def on_response(response):
        if url in response.url:
            responses.append(response)

    page.on('response', on_response)
    try:
        action()
        logger.debug("动作执行完成，开始等待响应...")
        # 等待一段 时间，让所有可能的响应都到达
        page.wait_for_timeout(wait_time * 1000)
        if not responses:
            logger.error(f"未捕获到任何匹配 {url} 的响应")
            raise Exception(f"未捕获到任何匹配 {url} 的响应")
        # 取最后一个响应（最新）
        response = responses[-1]
        logger.info(f"捕获到 {len(responses)} 个响应，取最后一个，状态码: {response.status}")
        allure.attach(f"接口: {response.url}", name="请求URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response.status), name="状态码", attachment_type=allure.attachment_type.TEXT)
        return response
    finally:
        page.remove_listener('response', on_response)