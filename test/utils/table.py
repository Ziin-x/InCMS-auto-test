from utils.log import logger

import allure


@allure.step("在表格单元格中输入内容")
def fill_table_cell(container, table_selector, row_index, col_index, text,
                    row_selector="tr", cell_selector="td", use_double_click=False):
    """
    在表格的指定单元格中输入文本，支持 Page、Frame 或 baseframe 作为容器
    :param container: Playwright Page、Frame 或 baseframe 对象
    :param table_selector: 表格容器的 CSS 选择器（字符串）
    :param row_index: 行索引（从 0 开始）
    :param col_index: 列索引（从 0 开始）
    :param text: 要输入的文本
    :param row_selector: 每行的 CSS 选择器，根据实际表格结构调整
    :param cell_selector: 单元格的 CSS 选择器，根据实际表格结构调整
    :param use_double_click: 是否需要双击激活编辑，默认 False（单击）
    """
    # 定位表格
    table = container.find(table_selector)
    # 定位目标行和单元格
    try:
        logger.debug(f"准备在表格中输入：行 {row_index}, 列 {col_index}，文本 = '{text}'")
        row = table.locator(row_selector).nth(row_index)
        cell = row.locator(cell_selector).nth(col_index)
        cell.wait_for(state="visible")
        # 激活单元格
        if use_double_click:
            cell.dblclick()
        else:
            cell.click()
        # 清空并输入
        cell.fill(text)
        logger.info(f"表格输入成功：({row_index}, {col_index}) -> '{text}'")
    except Exception as e:
        logger.error(f"表格输入失败：({row_index}, {col_index}) -> '{text}'")
        raise e
