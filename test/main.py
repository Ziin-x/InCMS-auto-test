import os
import shutil
import subprocess
import sys

import pytest

from config.setting import PYTEST_ARGS

# 确保工作目录切换到项目根目录（main.py 所在目录）
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

ALLURE_RESULTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "allure-results")
ALLURE_REPORT_DIR = os.path.join(PROJECT_ROOT, "outputs", "allure-report")


def main():
    # 1. 确保结果目录存在
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

    # 2. 运行 pytest，指定 allure 结果目录和测试路径
    print("🚀 开始运行测试用例...")
    pytest_args = [
        *PYTEST_ARGS,
        f"--alluredir={ALLURE_RESULTS_DIR}",
        "testcases/",
    ]
    exit_code = pytest.main(pytest_args)

    if exit_code != pytest.ExitCode.OK:
        print(f"⚠️ 测试用例未全部通过 (exit code: {exit_code})，但仍将继续生成报告")

    # 3. 生成 Allure 报告
    print("📊 正在生成 Allure 报告...")
    if os.path.exists(ALLURE_REPORT_DIR):
        shutil.rmtree(ALLURE_REPORT_DIR)

    try:
        subprocess.run(
            ["allure", "generate", ALLURE_RESULTS_DIR, "-o", ALLURE_REPORT_DIR, "--clean"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(f"✅ 报告生成成功：{ALLURE_REPORT_DIR}")
    except FileNotFoundError:
        print("❌ 未找到 allure 命令，请确保已安装 Allure 并添加到环境变量中")
        print("   安装参考：https://docs.qameta.io/allure/#_installing_a_commandline")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("❌ 生成报告失败：")
        print(e.stderr)
        sys.exit(1)

    print("🎉 所有任务完成！")


if __name__ == "__main__":
    main()
