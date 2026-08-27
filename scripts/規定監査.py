from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "規定" / "正本索引.json"
VERSION = "2026-08-28-成立規定-5"
TITLE = "大規模言語模型成立規定"
STATUS = "局所安定正本・再開放可"

LM_CONDITIONS = ["言語状態域", "条件付き言語差形成", "構成再利用", "言語状態接続"]
AUDIT_CONDITIONS = ["独立対象固定", "言語対応", "差分追従", "複数対照への再利用", "未列挙構成監査", "再現性"]

REQUIRED_ROOT = {
    "README.md", "PROJECT_MAP.md", "CITATION.cff", "LICENSE",
    "LICENSE-APACHE-2.0", "LICENSE-CC-BY-4.0", "NOTICE",
}
REQUIRED_CANON = [
    "規定/00_規定言語.md", "規定/01_基底語彙.md", "規定/02_大規模言語模型成立.md",
    "規定/03_規模記述.md", "規定/04_運用境界.md", "規定/05_観測と判定.md",
    "規定/06_再開放.md",
]


def require_text(path: Path, phrases: list[str], problems: list[str]) -> None:
    if not path.exists():
        problems.append(f"欠損: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            problems.append(f"{path.relative_to(ROOT)} 必須句欠損: {phrase}")


def 監査() -> list[str]:
    problems: list[str] = []

    for name in sorted(REQUIRED_ROOT):
        if not (ROOT / name).exists():
            problems.append(f"必須ルート欠損: {name}")

    if not INDEX.exists():
        return problems + ["正本索引欠損"]

    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        return problems + [f"正本索引JSON不正: {exc}"]

    if data.get("正式名称") != TITLE:
        problems.append("正式名称不一致")
    if data.get("版") != VERSION:
        problems.append("版不一致")
    if data.get("状態") != STATUS:
        problems.append("状態不一致")
    if data.get("規定言語") != "日本語":
        problems.append("規定言語不一致")
    if data.get("正本") != REQUIRED_CANON:
        problems.append("正本一覧不一致")
    if data.get("言語模型性成立条件") != LM_CONDITIONS:
        problems.append("言語模型性成立条件がv5四条件と不一致")
    if data.get("識別監査条件") != AUDIT_CONDITIONS:
        problems.append("識別監査条件がv5六条件と不一致")
    if data.get("再現区分") != ["機能再現", "構成再現"]:
        problems.append("機能再現/構成再現分離が不正")

    repro = data.get("構成再現", {})
    if repro.get("普遍固定条件") is not False or repro.get("元模型相対") is not True:
        problems.append("構成再現が元模型相対・非固定条件になっていない")

    scale = data.get("規模", {})
    if scale.get("固定面") is not False or scale.get("方式") != "規模プロファイル":
        problems.append("規模が固定三面から規模プロファイルへ移行していない")

    formed = data.get("形成物", {})
    if formed.get("上位概念") != "形成済み模型状態":
        problems.append("形成物上位概念が形成済み模型状態ではない")

    boundary = data.get("模型境界", {})
    if boundary.get("部品種別で固定しない") is not True or boundary.get("retrievalを一律外周化しない") is not True:
        problems.append("模型境界が部品種別分類へ戻っている")

    principles = data.get("原則", {})
    for key in [
        "模型成立条件と識別監査条件を分離",
        "機能再現と構成再現を分離",
        "構成再現条件数を固定しない",
        "形成済み模型状態を未観測の意味関係へ昇格しない",
        "retrieval等を部品名だけで模型外へ固定しない",
        "下流失敗時に上位定義まで再開放する",
        "条件数を履歴互換性のために保守しない",
    ]:
        if principles.get(key) is not True:
            problems.append(f"v5原則欠損: {key}")

    for rel in REQUIRED_CANON:
        path = ROOT / rel
        if not path.exists():
            problems.append(f"正本欠損: {rel}")
        elif not path.read_text(encoding="utf-8").strip():
            problems.append(f"正本空: {rel}")

    require_text(ROOT / "規定/01_基底語彙.md", [
        "## 言語状態域", "## 条件付き言語差形成", "## 構成再利用", "## 言語状態接続",
        "## 形成済み模型状態", "## 機能再現", "## 構成再現", "## 構成不変量", "## 模型境界",
    ], problems)

    require_text(ROOT / "規定/02_大規模言語模型成立.md", [
        "言語模型性の成立条件", "言語状態域", "条件付き言語差形成", "構成再利用", "言語状態接続",
        "v4五条件から外したもの", "機能再現と構成再現を分ける", "普遍の固定七条件を置かない",
        "構成再現対象プロファイル", "構成不変量", "v4七条件の扱い", "識別監査", "規模プロファイル",
    ], problems)

    require_text(ROOT / "規定/03_規模記述.md", [
        "規模プロファイル", "固定三面", "実現規模", "形成規模", "言語状態域規模", "構成再利用規模",
    ], problems)

    require_text(ROOT / "規定/04_運用境界.md", [
        "模型境界の判定", "retrievalの境界", "REALM", "RETRO", "機能再現 != 構成再現",
    ], problems)

    require_text(ROOT / "規定/05_観測と判定.md", [
        "言語模型性四条件の監査", "anti-lookup監査", "architecture横断監査", "機能再現監査",
        "構成再現監査", "構成不変量監査", "上位定義自体を再開放候補",
    ], problems)

    require_text(ROOT / "規定/06_再開放.md", [
        "条件数を保守しない", "言語模型性四条件", "構成観測軸を普遍構成条件へ誤昇格",
    ], problems)

    require_text(ROOT / "README.md", [
        VERSION, "言語模型性の四条件", "機能再現と構成再現", "旧七条件の扱い", "規模プロファイル",
    ], problems)
    require_text(ROOT / "PROJECT_MAP.md", [VERSION, "旧五条件を模型成立条件として維持しない"], problems)
    require_text(ROOT / "CITATION.cff", [f'version: "{VERSION}"', "license: CC-BY-4.0"], problems)

    v5_report = ROOT / "観測/2026-08-28_構成定義v5全面再監査.md"
    require_text(v5_report, [
        "v4言語模型性五条件の誤り", "v4構成再現七条件の誤り", "機能再現と構成再現の混線",
        "形成済み関係", "模型境界の誤り", "規模三面の誤り", "architecture横断テスト",
    ], problems)

    machine = ROOT / "観測/2026-08-28_構成定義v5機械監査.txt"
    require_text(machine, [
        "V5_FULL_REOPEN_AUDIT=PASS", "OLD_FIVE_CONDITIONS_PRESERVED=NO",
        "OLD_SEVEN_CONDITIONS_UNIVERSAL=NO", "LANGUAGE_MODEL_INTRINSIC_CONDITION_COUNT=4",
    ], problems)

    for hist in [
        "観測/2026-08-27_構成定義独立関係監査.md",
        "観測/2026-08-27_構成定義v3変更記録.md",
        "観測/2026-08-28_構成定義v4変更記録.md",
    ]:
        if not (ROOT / hist).exists():
            problems.append(f"履歴観測欠損: {hist}")

    text02 = (ROOT / "規定/02_大規模言語模型成立.md").read_text(encoding="utf-8") if (ROOT / "規定/02_大規模言語模型成立.md").exists() else ""
    if "v3の七区別は維持する" in text02 or "v4までの五区別を維持" in text02:
        problems.append("旧条件数保守表現が現行正本に残存")

    return problems


def main() -> int:
    problems = 監査()
    if problems:
        print("規定監査: 不合格")
        for p in problems:
            print(f"- {p}")
        return 1
    print("規定監査: 合格")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
