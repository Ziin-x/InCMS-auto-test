import allure


class IndrawLocator:
    # indraw编辑
    indraw_edit = ("role", "button", "编辑")
    # indraw内部的iframe定位
    indraw_iframe = ("selector", "iframe[src*='/indraw/index.html']")
    # 选择苯环类
    benzene_class = ("selector", "#frag-benzenes-tool")
    # 选择苯环
    benzene = ("selector", "#action-mp-frag-benzene")
    # 画苯环
    draw_benzene = (("selector", ".dynamic"),
                    (50, 50))
    # 关闭indraw
    close_indraw = ("selector", ".iconfont.icon-close.default.square")

@allure.step("indraw编辑")
def indraw(page):
    page.click(IndrawLocator.indraw_edit)
    # get_frame返回的是baseframe实例
    frame = page.get_frame(IndrawLocator.indraw_iframe)
    frame.frame.page.wait_for_timeout(1000)
    frame.click(IndrawLocator.benzene_class)
    frame.click(IndrawLocator.benzene)
    frame.click_canvas(IndrawLocator.draw_benzene)
    page.click(IndrawLocator.close_indraw)