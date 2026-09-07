import json
from collections import Counter
from pathlib import Path

from ai.client import ask_ai
from ai.eval.dataset import SAMPLES
from ai.system_prompt import system_prompt

CLASSES = ["application_bug", "test_bug", "environment_issue", "flaky_test", "unknown"]


def run(use_gold: bool = False) -> None:
    if use_gold:
        from ai.eval.gold_labels import GOLD

        truth_by_id = dict(GOLD)
        print(f"使用 gold_labels.py 参考答案作为真值（{len(truth_by_id)} 条）\n")
    else:
        truth_by_id = {s["id"]: s["label"] for s in SAMPLES if s.get("label") in CLASSES}
        if not truth_by_id:
            print(f"没有已标注样本（当前 0/{len(SAMPLES)} 已标注）。")
            print("请先在 dataset.py 里给每条样本的 label 字段填上五类之一，")
            print("或加 --gold 参数直接用参考答案跑基线。")
            return
        unlabeled = len(SAMPLES) - len(truth_by_id)
        if unlabeled:
            print(f"⚠️  跳过未标注样本 {unlabeled} 条，本轮评测 {len(truth_by_id)} 条\n")

    samples = [s for s in SAMPLES if s["id"] in truth_by_id]

    confusion = Counter()
    wrong = []

    for i, s in enumerate(samples, 1):
        prompt = system_prompt.format(
            test_name=s["test_name"],
            error_type=s["error_type"],
            error=s["error"],
            traceback=s["traceback"],
        )
        result = ask_ai(prompt)
        pred = result.classification
        truth = truth_by_id[s["id"]]
        ok = pred == truth
        confusion[(truth, pred)] += 1
        mark = "✓" if ok else "✗"
        print(
            f"[{i:>3}/{len(samples)}] {mark} {s['id']} "
            f"{s['test_name'].split('::')[-1]}: 预测={pred} 真实={truth}"
        )
        if not ok:
            wrong.append(
                {
                    "id": s["id"],
                    "test_name": s["test_name"],
                    "pred": pred,
                    "truth": truth,
                    "root_cause": result.root_cause,
                }
            )

    correct = len(samples) - len(wrong)
    print(f"\n准确率: {correct}/{len(samples)} = {correct / len(samples):.1%}")

    print("\n混淆矩阵（行=真实标注，列=AI预测）:")
    corner = "真实\\预测"
    header = f"{corner:<22}" + "".join(f"{c[:12]:>14}" for c in CLASSES)
    print(header)
    for truth in CLASSES:
        row = f"{truth:<22}" + "".join(f"{confusion[(truth, p)]:>14}" for p in CLASSES)
        print(row)

    out = Path(__file__).parent / "misclassified.json"
    out.write_text(json.dumps(wrong, ensure_ascii=False, indent=2), encoding="utf-8")
    if wrong:
        print(f"\n误判样本已保存到 {out}，共 {len(wrong)} 条")
        print("下一步：读这些样本，找共性错误模式 → 改 system_prompt → 重跑 → 记录进 EVAL.md")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI 失败分类评测")
    parser.add_argument("--gold", action="store_true", help="用 gold_labels.py 参考答案作为真值")
    args = parser.parse_args()
    run(use_gold=args.gold)
