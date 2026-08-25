from __future__ import annotations

import json
from pathlib import Path


ルート = Path(__file__).resolve().parents[1]
索引 = ルート / "規定" / "正本索引.json"

現役禁止名 = {
    "layer0_functional_conformance_v4.py",
    "llm_minimal_architecture_groups_v3_0.py",
    "README.ja.md",
    "REPOSITORY_GIT_BLOB_MANIFEST.txt",
    "REPOSITORY_SHA256_MANIFEST.txt",
    "appendices",
    "artifacts",
    "layer0_recomposition_memory_demo_bilingual_bundle",
    "LICENSE-MIT",
    "LICENSE-CC-BY-4.0",
}

必須ルート = {
    "README.md",
    "PROJECT_MAP.md",
    "CITATION.cff",
    "LICENSE",
    "NOTICE",
}

正式名称 = "言語模型成立規定"
現行版 = "2026-08-25-成立規定-1"
現行状態 = "局所安定正本・再開放可"


def 監査() -> list[str]:
    問題: list[str] = []

    for 名前 in sorted(必須ルート):
        if not (ルート / 名前).exists():
            問題.append(f"必須ルートファイル欠損: {名前}")

    if not 索引.exists():
        問題.append("正本索引が存在しない")
        return 問題

    try:
        データ = json.loads(索引.read_text(encoding="utf-8"))
    except Exception as exc:
        問題.append(f"正本索引を読めない: {exc}")
        return 問題

    if データ.get("規定言語") != "日本語":
        問題.append("規定言語が日本語ではない")
    if データ.get("正式名称") != 正式名称:
        問題.append("正式名称が現行正本と一致しない")
    if データ.get("版") != 現行版:
        問題.append("版が現行正本と一致しない")
    if データ.get("状態") != 現行状態:
        問題.append("状態が局所安定正本ではない")

    正本 = データ.get("正本")
    if not isinstance(正本, list) or not 正本:
        問題.append("正本一覧が空または不正")
        正本 = []

    for 相対 in 正本:
        対象 = ルート / str(相対)
        if not 対象.exists():
            問題.append(f"正本欠損: {相対}")
            continue
        if 対象.suffix != ".md":
            問題.append(f"正本がMarkdownではない: {相対}")
        内容 = 対象.read_text(encoding="utf-8")
        if not 内容.strip():
            問題.append(f"正本が空: {相対}")
        if "（仮称）" in 内容:
            問題.append(f"正本に仮称表示が残存: {相対}")

    規定言語文書 = ルート / "規定" / "00_規定言語.md"
    if 規定言語文書.exists():
        内容 = 規定言語文書.read_text(encoding="utf-8")
        必須句 = [
            "一次規定言語",
            "日本語先行",
            "他言語は例外使用",
            "実務上やむを得ない",
        ]
        for 句 in 必須句:
            if 句 not in 内容:
                問題.append(f"日本語基底原則の必須句欠損: {句}")

    成立規定 = ルート / "規定" / "02_言語模型成立.md"
    if 成立規定.exists():
        内容 = 成立規定.read_text(encoding="utf-8")
        必須句 = [
            "成立差",
            "差分追従",
            "保存追従",
            "破壊追従",
            "複数対照への再利用",
            "再現性",
            "生成運用性を分離する",
        ]
        for 句 in 必須句:
            if 句 not in 内容:
                問題.append(f"言語模型成立規定の必須句欠損: {句}")
        if "形成差" in 内容:
            問題.append("言語模型成立規定に旧正本語『形成差』が残存")

    ルート直下 = {p.name for p in ルート.iterdir()}
    for 禁止 in sorted(現役禁止名):
        if 禁止 in ルート直下:
            問題.append(f"旧規定資産または旧ライセンスが現役ルートに残存: {禁止}")

    旧規定 = ルート / "旧規定" / "README.md"
    if not 旧規定.exists():
        問題.append("旧規定への履歴導線がない")

    readme = ルート / "README.md"
    if readme.exists():
        内容 = readme.read_text(encoding="utf-8")
        if 正式名称 not in 内容:
            問題.append("READMEに正式名称がない")
        if 現行版 not in 内容:
            問題.append("READMEに現行版がない")
        if "局所安定正本" not in 内容:
            問題.append("READMEに局所安定正本の宣言がない")
        if "旧称" not in 内容 or "Layer-0" not in 内容:
            問題.append("READMEに旧Layer-0の暫定名称化が明示されていない")
        if "Apache License 2.0" not in 内容:
            問題.append("READMEのライセンス表記がApache License 2.0ではない")
        if "（仮称）" in 内容 or "再構築中" in 内容:
            問題.append("READMEに未確定表示が残存")

    license_file = ルート / "LICENSE"
    if license_file.exists():
        内容 = license_file.read_text(encoding="utf-8")
        if "Apache License" not in 内容 or "Version 2.0" not in 内容:
            問題.append("LICENSEがApache License 2.0ではない")

    notice = ルート / "NOTICE"
    if notice.exists():
        内容 = notice.read_text(encoding="utf-8")
        if "Apache License 2.0" not in 内容:
            問題.append("NOTICEのライセンス表記がApache License 2.0ではない")
        if "Copyright 2026 がっちむち♂" not in 内容:
            問題.append("NOTICEに著作権表示がない")

    citation = ルート / "CITATION.cff"
    if citation.exists():
        内容 = citation.read_text(encoding="utf-8")
        if 'title: "言語模型成立規定"' not in 内容:
            問題.append("CITATION.cffの正式名称が不一致")
        if f'version: "{現行版}"' not in 内容:
            問題.append("CITATION.cffの版が不一致")
        if "license: Apache-2.0" not in 内容:
            問題.append("CITATION.cffのライセンスがApache-2.0ではない")

    最終閉包 = ルート / "観測" / "2026-08-25_最終閉包監査.md"
    if not 最終閉包.exists():
        問題.append("最終閉包監査が存在しない")

    if (ルート / "README.ja.md").exists():
        問題.append("README.ja.mdを作らない。README.md自体を日本語正本入口とする")

    return 問題


def main() -> int:
    問題 = 監査()
    if 問題:
        print("規定監査: 不合格")
        for 項目 in 問題:
            print(f"- {項目}")
        return 1

    print("規定監査: 合格")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
