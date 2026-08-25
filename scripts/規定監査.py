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

    正本候補 = データ.get("正本候補")
    if not isinstance(正本候補, list) or not 正本候補:
        問題.append("正本候補一覧が空または不正")
        正本候補 = []

    for 相対 in 正本候補:
        対象 = ルート / str(相対)
        if not 対象.exists():
            問題.append(f"正本候補欠損: {相対}")
            continue
        if 対象.suffix != ".md":
            問題.append(f"正本候補がMarkdownではない: {相対}")
        内容 = 対象.read_text(encoding="utf-8")
        if not 内容.strip():
            問題.append(f"正本候補が空: {相対}")

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
        if "日本語正本" not in 内容:
            問題.append("READMEに日本語正本の宣言がない")
        if "旧称" not in 内容 or "Layer-0" not in 内容:
            問題.append("READMEに旧Layer-0の暫定名称化が明示されていない")
        if "Apache License 2.0" not in 内容:
            問題.append("READMEのライセンス表記がApache License 2.0ではない")

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
        if "license: Apache-2.0" not in 内容:
            問題.append("CITATION.cffのライセンスがApache-2.0ではない")

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
