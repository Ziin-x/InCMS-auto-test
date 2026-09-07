# ============================================================
# conftest.py —— pytest 插件入口 + 全局 fixture
# ============================================================
# 上半部分：原有 fixture（浏览器、登录页、各产品页面）
# 下半部分：AI 失败分析流水线（v2 加固版，替换旧的"当场调 AI"逻辑）
#
# AI 流水线 4 步：
#   ① 测试运行中：某条测试失败 → makereport 钩子把失败信息记进 _failures
#   ② 全部跑完后：sessionfinish 钩子逐个问 AI → 缓存去重 → 生成 JSON + HTML 报告
#
# 为什么不"当场调 AI"（旧版的做法）：
#   - 不打断测试：调 AI 要好几秒，当场调用会拖慢整个测试进程
#   - 可去重：同一失败只问一次 AI（缓存），CI 里重复跑不重复烧 token
#   - 报告统一：所有失败汇总成一份报告，人看 HTML，脚本读 JSON
# ============================================================

import hashlib
# 算 MD5 指纹，用于"失败签名"（判断两次失败是不是同一个）

import html
# 转义 HTML 特殊字符（< > & " 等），防止 AI 输出的文本破坏报告页面

import json
# 读写 JSON 文件（缓存文件、JSON 报告）

from datetime import datetime
# 取当前时间，写进报告文件名和报告内容

from pathlib import Path
# 文件路径处理

import pytest
from playwright.sync_api import sync_playwright

from ai.client import ask_ai
# "问 AI"的唯一入口：prompt 进 → 分析结果出（重试/解析/降级都在 client.py 内部处理）

from ai.configs import PROJECT_ROOT, settings
# PROJECT_ROOT：项目根目录路径
# settings：全局配置对象（超时、截断行数、报告目录等都从它取）

from ai.system_prompt import system_prompt
# 提示词模板——一段带 {test_name}、{error_type} 等占位符的字符串

from config.environments_pydantic import Environment
from data.pydantic.plug_pydantic import PlugPageData
from object.fixture_object.login_page_object import LoginPageObject
from object.fixture_object.plug_page_object import PlugPageObject
from utils.log import logger


# ============================================================
# 原有 fixture（保持不动）
# ============================================================

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]  # 启动时最大化
        )
        yield browser
        browser.close()

env = Environment.get_data()
@pytest.fixture(scope="function")
def login_plug_page(browser):
    logger.info("==================== login before testcase ====================")
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPageObject(page)
    login_page.login_plug(env)
    yield login_page.page
    context.close()

plug_data = PlugPageData.get_data()
@pytest.fixture(scope="function")
def InCMS_page(login_plug_page):
    plug_page = PlugPageObject(login_plug_page)
    plug_page.page.wait_for_load_state('networkidle')
    plug_page.choose_product(plug_data.cms)
    return plug_page.page

@pytest.fixture(scope="function")
def InELN_page(login_plug_page):
    plug_page = PlugPageObject(login_plug_page)
    plug_page.page.wait_for_load_state('networkidle')
    plug_page.choose_product(plug_data.eln)
    return plug_page.page

def pytest_generate_tests(metafunc):
    # 检查测试函数是否需要 project_name 参数
    if "project_name" in metafunc.fixturenames:
        # 从 cache 中读取多个项目名
        cache = metafunc.config.cache
        project_name_list = []
        for key in ["compound_sequence_project_name", "mixture_formula_project_name",
                    "custom_compound_project_name", "DNA_project_name", "RNA_project_name"]:
            name = cache.get(key, None)
            if name is not None:
                project_name_list.append(name)
            else:
                logger.error(f"cache中缺少数据: {key}")

        if not project_name_list:
            raise ValueError("没有记录到项目名称")
        # 动态参数化 project_name
        metafunc.parametrize("project_name", project_name_list)


# ============================================================
# AI 失败分析流水线（v2 加固版）
# 全局状态：整个测试会话（一次 pytest 运行）共享的变量
# ============================================================

# 失败清单：运行中收集的失败信息，每条是一个字典
# 字典里的字段：test_name / error_type / error / traceback（见 makereport 钩子）
_failures: list[dict] = []

# AI 结果缓存：key = 失败签名（MD5 字符串），value = 分析结果字典
_ai_cache: dict = {}

# 缓存文件位置：test/ 目录下的隐藏文件 .ai_failure_cache.json
# Path(__file__).parent = 本文件所在的文件夹（即 test/）
# 用文件存缓存 = 上次运行的分析结果，下次运行还能用（跨运行持久化）
_CACHE_PATH = Path(__file__).parent / ".ai_failure_cache.json"

# 缓存上限：超过 500 条直接清空重来，防止缓存文件无限膨胀
_CACHE_LIMIT = 500

# 报告输出目录：项目根/ai_reports（"ai_reports" 这个值在 configs.py 的 settings 里配置）
_REPORT_DIR = PROJECT_ROOT / settings.report_dir


# ---- 工具函数①：缓存的读和写 ----

def _load_cache() -> dict:
    """启动时把上次的缓存文件读进内存。

    返回：字典 {失败签名: 分析结果}
    任何异常（文件不存在、内容损坏）都返回空字典——
    缓存是"锦上添花"的东西，绝不能因为它坏了就影响测试。
    """
    if not _CACHE_PATH.exists():
        return {}  # 第一次跑没有缓存文件，属正常情况

    try:
        # read_text：读整个文件内容为字符串
        # json.loads：字符串 → 字典
        return json.loads(_CACHE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # 文件损坏或读不了：当作没有缓存处理，不影响测试
        return {}


def _save_cache() -> None:
    """结束时把内存中的缓存写回文件，供下次运行使用。"""
    if len(_ai_cache) > _CACHE_LIMIT:
        _ai_cache.clear()  # 超上限：整体清空重来（简单策略，500 条内足够用）

    _CACHE_PATH.write_text(
        json.dumps(_ai_cache, ensure_ascii=False, indent=2),
        # dumps：字典 → JSON 字符串
        #   ensure_ascii=False：中文按原样输出（默认会转成 \uXXXX 样式，人没法看）
        #   indent=2：缩进 2 格，文件内容人类可读
        encoding="utf-8",
    )


# ---- 工具函数②：traceback 截短 + 失败签名 ----

def _truncate_traceback(text: str) -> str:
    """把超长 traceback 截短：只保留末尾 N 行（默认 30，在 .env 可配）。

    为什么要截：
      ① 省 token——几百行 traceback 每行都是钱
      ② 太长 AI 容易抓不住重点（关键信息被淹没在调用链里）
      ③ 报错根因几乎总在最后几行（最底层的报错点），前面多为调用链铺垫
    """
    lines = text.splitlines()  # 按行拆成列表，每行一个元素

    if len(lines) <= settings.max_traceback_lines:
        return text  # 本来就不长，原样返回

    # 负数下标 = 从末尾数：lines[-30:] 取最后 30 行
    # "\n".join(...) = 把 30 行重新拼回一个字符串，中间用换行符连接
    return "(前段已省略，只保留末尾关键帧)\n" + "\n".join(
        lines[-settings.max_traceback_lines:]
    )


def _failure_signature(failure: dict) -> str:
    """给一条失败计算"指纹"：同一失败 → 同一指纹 → 第二次遇到时命中缓存，不再问 AI。

    设计点（面试常问）：key 只用 test_name + error_type + error 文本，
    刻意不用完整 traceback——
    traceback 里的行号/文件路径会随代码改动漂移，导致"同一个缺陷"
    今天和明天算出不同指纹，缓存永远命中不了。
    """
    # 三块拼成一个字符串，用 :: 分隔（:: 在文本中几乎不会出现，避免误拼接）
    key = f"{failure['test_name']}::{failure['error_type']}::{failure['error']}"

    # md5：任意长度文本 → 固定 32 位十六进制指纹（不可逆、定长、方便当 key）
    return hashlib.md5(key.encode("utf-8")).hexdigest()


# ---- pytest 钩子（pytest 在特定时机自动调用，我们从不手动调用） ----

def pytest_sessionstart(session):
    """钩子①：整个测试会话开始前，pytest 调用一次。

    时机：测试还没跑之前。
    作用：把上次的缓存文件加载进内存，供本次运行查命中。
    """
    global _ai_cache  # 声明：下面要修改的是模块级全局变量（否则 Python 会把它当本地变量）
    _ai_cache = _load_cache()


@pytest.hookimpl(hookwrapper=True)
# hookwrapper=True：让我们的钩子"包住"pytest 原本的逻辑——
# 相当于"先等 pytest 干完它自己的事，我再接手"。
def pytest_runtest_makereport(item, call):
    """钩子②：每个测试的每个阶段出结果时，pytest 都会调用。

    参数（pytest 自动传入）：
      item：当前测试对象（item.nodeid = 测试全名）
      call：本次阶段的信息（call.excinfo = 失败时的异常对象）

    hookwrapper 写法（本文件最"怪"的两行，多看几遍）：
      outcome = yield      ← 暂停在这里，把控制权交还给 pytest，等它干完
      report = ...         ← pytest 干完后，代码从这里继续，我们拿结果做自己的事
    """
    outcome = yield  # 暂停，等 pytest 生成好本次阶段的结果
    report = outcome.get_result()  # 拿到 pytest 的结果对象

    # 判断"这是一次测试失败"需要两个条件同时成立：
    #   report.when == "call"  → 只看"执行阶段"。一个测试会经历三个阶段：
    #                            setup(准备) / call(执行) / teardown(清理)，
    #                            不筛选的话一条失败会被收集三次
    #   report.failed           → 这个阶段确实失败了
    if report.when == "call" and report.failed:
        _failures.append(  # 把这条失败记进清单（只收集，不调 AI、不打断测试）
            {
                "test_name": item.nodeid,
                # 测试全名，如 "test/test_xx.py::test_登录"

                "error_type": call.excinfo.type.__name__ if call.excinfo else "Unknown",
                # call.excinfo：失败时的异常对象
                #   .type = 异常类型（AssertionError / TimeoutError ...）
                #   .__name__ = 取它的名字字符串（"AssertionError"）
                # if 兜底：理论上失败时 excinfo 一定存在，但防御性写法不怕万一

                "error": str(call.excinfo.value) if call.excinfo else "",
                # .value = 异常携带的消息文本；str() 转成字符串

                "traceback": _truncate_traceback(str(report.longrepr)),
                # report.longrepr = 完整报错信息（含整条 traceback），先截短再存
            }
        )


# ---- 分析一条失败 + 生成报告 ----

def _analyze_failure(failure: dict) -> dict:
    """对一条失败做 AI 分析：先查缓存，没命中才问 AI。

    返回：分析结果字典，比缓存里的多一个 "cached" 字段标记来源。
    """
    signature = _failure_signature(failure)  # 先算指纹

    if signature in _ai_cache:
        # 缓存命中：同一失败之前已经分析过
        # {**旧字典, "cached": True} = 复制旧字典的全部内容，再补一个字段
        return {**_ai_cache[signature], "cached": True}

    try:
        # 三步走：
        #   system_prompt.format(**failure)：把失败信息填进提示词模板的占位符
        #     **failure 的作用 = 把字典"拆开"成关键字参数
        #     等价于 format(test_name=..., error_type=..., error=..., traceback=...)
        #   ask_ai(...)：调 AI，拿到 pydantic 校验过的分析结果
        #   .model_dump()：pydantic 对象 → 普通字典（方便存缓存、写 JSON）
        analysis = ask_ai(system_prompt.format(**failure)).model_dump()
    except Exception as exc:
        # 最后的保险：无论 AI 那边发生什么（网络、限流、代码 bug），
        # 都不能让 pytest 的报告流程崩溃——测试结果本身比 AI 分析重要
        analysis = {
            "classification": "unknown",
            "confidence": 0.0,
            "root_cause": f"AI 分析调用失败：{exc}",
            "evidence": [],
            "recommendation": [],
        }

    analysis["cached"] = False  # 标记：这条是本次新分析的
    # 存进缓存（剔除 "cached" 这个临时标记，保持缓存数据干净）：
    # {k: v for k, v in ... if k != "cached"} = 字典推导式，复制字典但跳过指定键
    _ai_cache[signature] = {k: v for k, v in analysis.items() if k != "cached"}
    return analysis


def _render_html(data: dict) -> str:
    """把报告数据拼成一页 HTML 文本。

    手写 HTML 模板、零依赖：为了一个表格引入 jinja2 这类模板库不划算。
    """
    rows = []  # 收集每一行表格的 HTML 片段
    for r in data["results"]:  # 遍历每条失败记录
        # html.escape()：把 < > & " 等转义——AI 输出的文本里万一有这些字符，
        # 会把页面结构搞坏甚至形成注入，必须转义
        # f-string 拼一行 <tr>
        # ''.join(...)：把证据/建议列表的多个 <li> 片段拼成一段（列表 → HTML 列表）
        rows.append(
            f"""
        <tr>
          <td>{html.escape(r['test_name'])}</td>
          <td>{html.escape(r['classification'])}</td>
          <td>{r['confidence']:.0%}</td>
          <td>{'缓存命中' if r['cached'] else '本次分析'}</td>
          <td>{html.escape(r['root_cause'])}</td>
          <td><ul>{''.join(f'<li>{html.escape(e)}</li>' for e in r['evidence'])}</ul></td>
          <td><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in r['recommendation'])}</ul></td>
        </tr>"""
        )
        # 上面 {r['confidence']:.0%} 里的 :.0% = 格式化规则：0.87 显示成 "87%"
        # '缓存命中' if ... else ... = 三元表达式：条件成立取前者，否则取后者

    # 外层 HTML 骨架 + 简单 CSS
    # 注意：CSS 里的花括号写成 {{ }}——f-string 的规则：
    #   {{ = 字面量的 { ，}} = 字面量的 }（因为 {} 在 f-string 里是占位符语法）
    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>AI 失败分析报告</title>
<style>
body {{ font-family: -apple-system, "PingFang SC", sans-serif; margin: 24px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
th {{ background: #f5f5f5; }}
</style></head>
<body>
<h1>AI 测试失败分析报告</h1>
<p>生成时间：{html.escape(data['generated_at'])} | 失败 {data['total_failures']} 个 | 本次 AI 分析 {data['analyzed_by_ai']} 个 | 缓存命中 {data['hit_cache']} 个</p>
<table>
<tr><th>测试</th><th>分类</th><th>置信度</th><th>来源</th><th>根因</th><th>证据</th><th>建议</th></tr>
{''.join(rows)}
</table>
</body></html>"""


def _write_reports(results: list[dict]) -> Path:
    """把结果写成 JSON + HTML 两份报告文件，返回文件路径（不带扩展名）。"""
    _REPORT_DIR.mkdir(parents=True, exist_ok=True)
    # 报告目录不存在就创建；存在也不报错（exist_ok=True）

    # 报告文件名带时间戳，多次运行互不覆盖：
    # 如 ai_failure_report_20260907_101530.json / .html
    stem = _REPORT_DIR / f"ai_failure_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 汇总信息 + 明细，一份数据同时供 JSON 和 HTML 两种报告使用
    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),  # 生成时间（精确到秒）
        "total_failures": len(results),                                # 失败总数
        "analyzed_by_ai": sum(1 for r in results if not r["cached"]),  # 本次真调了 AI 的条数
        "hit_cache": sum(1 for r in results if r["cached"]),           # 命中缓存的条数
        "results": results,                                            # 明细
        # sum(1 for ...)：生成器写法 = 统计满足条件的个数
    }

    # JSON 报告：给脚本读、给机器消费（后续可接 CI、通知机器人）
    Path(f"{stem}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # HTML 报告：浏览器直接打开看（给人读）
    Path(f"{stem}.html").write_text(_render_html(data), encoding="utf-8")

    return stem


def _print_summary(results: list[dict], stem: Path) -> None:
    """在终端打印一份简短总结（报告文件是完整版，这里是速览）。"""
    print("\n================= AI 失败分析 =================")
    for i, r in enumerate(results, 1):  # enumerate(x, 1)：遍历的同时从 1 开始编号
        tag = "缓存" if r["cached"] else "AI  "  # 标记来源
        first_line = r["root_cause"].splitlines()[0]  # 根因只显示第一行，避免刷屏
        print(
            f"{i}. [{tag}] {r['test_name']} -> {r['classification']}"
            f"（置信度 {r['confidence']:.0%}）\n   根因: {first_line}"
        )
    print(f"报告已生成: {stem}.json / {stem}.html")
    print("==============================================\n")


def pytest_sessionfinish(session, exitstatus):
    """钩子③：整个测试会话全部结束后，pytest 调用一次。

    时机：所有测试跑完、失败信息全部收集完毕。
    作用：流水线的第 ② 步——统一批量分析 + 生成报告。
    """
    if not _failures:
        return  # 没有失败，什么都不用做

    try:
        # 对每条失败：查缓存/问 AI，然后把失败信息和分析结果合并成一条完整记录
        # {**failure, **analysis}：两个字典解包合并（后者的键覆盖前者）
        results = [{**failure, **_analyze_failure(failure)} for failure in _failures]

        stem = _write_reports(results)  # 写 JSON + HTML 报告
        _print_summary(results, stem)   # 终端打印速览
    except Exception as exc:
        # 报告环节出错也不影响测试结果（测试早已跑完，这里只是"附加服务"）
        print(f"\n[AI 分析] 报告生成失败，不影响测试结果：{exc}\n")
    finally:
        # finally：无论上面成功与否，缓存都要写回——已经分析出的结果别浪费
        _save_cache()
