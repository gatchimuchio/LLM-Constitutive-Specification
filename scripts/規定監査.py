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
}

必須ルート = {
    "README.md",
    "PROJECT_MAP.md",
    "CITATION.cff",
    "LICENSE",
    "LICENSE-APACHE-2.0",
    "LICENSE-CC-BY-4.0",
    "NOTICE",
}

正式名称 = "大規模言語模型成立規定"
現行版 = "2026-08-28-成立規定-4"
現行状態 = "局所安定正本・再開放可"
成立規定パス = "規定/02_大規模言語模型成立.md"
最終確認パス = "観測/2026-08-26_修正後ダブルチェック.md"
V3独立監査パス = "観測/2026-08-27_構成定義独立関係監査.md"
V3変更記録パス = "観測/2026-08-27_構成定義v3変更記録.md"
V3関係写像パス = "観測/2026-08-27_構成定義関係写像.json"
V3機械監査パス = "観測/2026-08-27_構成定義機械監査.txt"
V4変更記録パス = "観測/2026-08-28_構成定義v4変更記録.md"
V4機械監査パス = "観測/2026-08-28_構成定義v4機械監査.txt"

言語模型性成立条件 = ["独立対象", "文脈依存関係", "関係再利用", "言語対応", "局所対応"]
構成再現条件 = [
    "状態分離・保持・更新",
    "意味・関係同一性追跡",
    "未確定差の共存",
    "寄与調整と確定分離",
    "構成連鎖 / 再作用・再結合",
    "再作用閉包 / 終端成立差",
    "形成済み関係の保持 / 作用機構との分離",
]
構成再現成立境界 = [
    "作用状態性",
    "状態遷移性",
    "前段差による後段作用変化",
    "checkpoint等の実効再利用",
    "再作用は再採点ではない",
    "再結合は最終得点合算だけではない",
    "入力境界からの内生形成",
]


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

    if 成立規定パス not in 正本:
        問題.append("大規模言語模型成立規定が正本索引にない")
    if "規定/02_言語模型成立.md" in 正本:
        問題.append("旧射程の言語模型成立文書が正本索引に残存")

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

    if (ルート / "規定" / "02_言語模型成立.md").exists():
        問題.append("旧射程の02_言語模型成立.mdが現役正本に残存")

    言語射程 = データ.get("言語射程")
    if not isinstance(言語射程, dict):
        問題.append("言語射程が欠損または不正")
    else:
        if 言語射程.get("自然言語限定") is not False:
            問題.append("言語射程が自然言語限定へ戻っている")
        if "プログラム言語" not in 言語射程.get("例", []):
            問題.append("言語射程にプログラム言語がない")

    if データ.get("言語模型性成立条件") != 言語模型性成立条件:
        問題.append("言語模型性成立条件が現行正本の五区別と一致しない")
    if データ.get("構成再現条件") != 構成再現条件:
        問題.append("構成再現条件が現行正本の七区別と一致しない")
    if データ.get("構成再現成立境界") != 構成再現成立境界:
        問題.append("構成再現成立境界がv4正本と一致しない")
    if データ.get("規模面") != ["状態域規模", "関係域規模", "共有適用規模"]:
        問題.append("規模三面が現行正本と一致しない")

    原則 = データ.get("原則")
    if not isinstance(原則, dict):
        問題.append("原則が欠損または不正")
    else:
        for 鍵 in [
            "生成運用性をLLM成立から分離",
            "MINIDORAを成立証人にしない",
            "HDS_Compilerを成立証人にしない",
            "形成履歴と形成済み関係を分離",
            "下流再構成物を成立証人にしない",
            "言語模型性と構成再現適合を分離",
            "評価メタデータを作用状態と同一視しない",
            "再採点を再作用と同一視しない",
            "合成fixtureのみで端到端構成再現を確定しない",
        ]:
            if 原則.get(鍵) is not True:
                問題.append(f"v4原則欠損: {鍵}")

    規定言語文書 = ルート / "規定" / "00_規定言語.md"
    if 規定言語文書.exists():
        内容 = 規定言語文書.read_text(encoding="utf-8")
        必須句 = ["一次規定言語", "日本語先行", "他言語は例外使用", "実務上やむを得ない"]
        for 句 in 必須句:
            if 句 not in 内容:
                問題.append(f"日本語基底原則の必須句欠損: {句}")

    基底語彙 = ルート / "規定" / "01_基底語彙.md"
    if 基底語彙.exists():
        内容 = 基底語彙.read_text(encoding="utf-8")
        必須句 = [
            "## 言語体系",
            "プログラム言語",
            "## 成立差",
            "## 作用状態",
            "## 評価メタデータ",
            "## 状態差",
            "## 作用",
            "## 状態遷移",
            "## 内生形成",
            "## 状態分離",
            "## 状態保持",
            "## 状態更新",
            "## 未確定差の共存",
            "## 寄与調整",
            "## 構成連鎖",
            "## 構成再現",
            "## 形成済み関係",
            "## 形成履歴",
        ]
        for 句 in 必須句:
            if 句 not in 内容:
                問題.append(f"基底語彙の必須句欠損: {句}")

    成立規定 = ルート / 成立規定パス
    if 成立規定.exists():
        内容 = 成立規定.read_text(encoding="utf-8")
        必須句 = [
            "言語体系の射程",
            "言語模型性の成立条件",
            "構成再現条件",
            "作用状態と評価メタデータの境界",
            "状態更新と状態遷移",
            "同一の作用状態へ同じ評価器を再適用",
            "入力境界からの内生形成",
            "七条件の成立境界",
            "構成再現の非成立例",
            "checkpoint実効再利用追従",
            "寄与調整と確定分離",
            "再作用閉包 / 終端成立差",
            "差分追従",
            "複数対照への再利用",
            "再現性",
            "補助証拠",
            "保存追従",
            "破壊追従",
            "生成運用性を分離する",
            "大規模性",
        ]
        for 句 in 必須句:
            if 句 not in 内容:
                問題.append(f"大規模言語模型成立規定の必須句欠損: {句}")
        if "5.1〜5.5が" in 内容:
            問題.append("旧五監査の一律必須表現が残存")

    必須監査 = データ.get("局所対応必須監査")
    if 必須監査 != ["差分追従", "複数対照への再利用", "再現性"]:
        問題.append("局所対応必須監査が現行正本と一致しない")

    補助監査 = データ.get("局所対応補助監査")
    if not isinstance(補助監査, list) or "保存追従" not in 補助監査 or "破壊追従" not in 補助監査:
        問題.append("局所対応補助監査が現行正本と一致しない")

    ルート直下 = {p.name for p in ルート.iterdir()}
    for 禁止 in sorted(現役禁止名):
        if 禁止 in ルート直下:
            問題.append(f"旧規定資産または旧ライセンスが現役ルートに残存: {禁止}")

    if not (ルート / "旧規定" / "README.md").exists():
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
        if "プログラム言語" not in 内容:
            問題.append("READMEに自然言語限定解除が反映されていない")
        if "保存追従・破壊追従" not in 内容 or "補助証拠" not in 内容:
            問題.append("READMEに監査条件修正が反映されていない")
        if "構成再現条件" not in 内容:
            問題.append("READMEに構成再現条件が反映されていない")
        for 句 in ["作用状態 != 評価メタデータ", "再作用 != 再採点", "端到端構成再現 != fixture後段適合"]:
            if 句 not in 内容:
                問題.append(f"READMEのv4精度境界欠損: {句}")
        for 句 in ["CC-BY-4.0", "Apache License 2.0", "LICENSE-APACHE-2.0", "LICENSE-CC-BY-4.0"]:
            if 句 not in 内容:
                問題.append(f"READMEのライセンス分離表記が欠損: {句}")

    license_scope = ルート / "LICENSE"
    if license_scope.exists():
        内容 = license_scope.read_text(encoding="utf-8")
        for 句 in ["成果物の種類ごと", "Apache-2.0", "CC-BY-4.0", "デュアルライセンスではありません"]:
            if 句 not in 内容:
                問題.append(f"LICENSEの適用範囲表記が欠損: {句}")

    apache_file = ルート / "LICENSE-APACHE-2.0"
    if apache_file.exists():
        内容 = apache_file.read_text(encoding="utf-8")
        if "Apache License" not in 内容 or "Version 2.0" not in 内容:
            問題.append("LICENSE-APACHE-2.0がApache License 2.0ではない")

    cc_file = ルート / "LICENSE-CC-BY-4.0"
    if cc_file.exists():
        内容 = cc_file.read_text(encoding="utf-8")
        if "CC-BY-4.0" not in 内容 or "creativecommons.org/licenses/by/4.0/legalcode" not in 内容:
            問題.append("LICENSE-CC-BY-4.0がCC BY 4.0正式条件を参照していない")

    notice = ルート / "NOTICE"
    if notice.exists():
        内容 = notice.read_text(encoding="utf-8")
        for 句 in ["Apache License 2.0", "Creative Commons Attribution 4.0 International", "デュアルライセンスではありません"]:
            if 句 not in 内容:
                問題.append(f"NOTICEのライセンス分離表記が欠損: {句}")

    citation = ルート / "CITATION.cff"
    if citation.exists():
        内容 = citation.read_text(encoding="utf-8")
        if f'title: "{正式名称}"' not in 内容:
            問題.append("CITATION.cffの正式名称が不一致")
        if f'version: "{現行版}"' not in 内容:
            問題.append("CITATION.cffの版が不一致")
        if "license: CC-BY-4.0" not in 内容:
            問題.append("CITATION.cffの規定文書ライセンスがCC-BY-4.0ではない")

    最終確認 = ルート / 最終確認パス
    if not 最終確認.exists():
        問題.append("修正後ダブルチェックが存在しない")
    else:
        内容 = 最終確認.read_text(encoding="utf-8")
        for 句 in ["Code Llama", "LLaDA", "RWKV", "BloombergGPT", "修正後規定: 局所安定"]:
            if 句 not in 内容:
                問題.append(f"修正後ダブルチェックの裏取り欠損: {句}")

    for 相対 in [V3独立監査パス, V3変更記録パス, V3関係写像パス, V3機械監査パス]:
        if not (ルート / 相対).exists():
            問題.append(f"v3観測成果物欠損: {相対}")

    独立監査 = ルート / V3独立監査パス
    if 独立監査.exists():
        内容 = 独立監査.read_text(encoding="utf-8")
        for 句 in ["状態保持 != 記録", "寄与調整 != 確定", "最小成立条件と構成再現条件を分ける", "意味同一性を構成再現へ明示する"]:
            if 句 not in 内容:
                問題.append(f"v3独立監査の必須記録欠損: {句}")

    関係写像 = ルート / V3関係写像パス
    if 関係写像.exists():
        try:
            写像データ = json.loads(関係写像.read_text(encoding="utf-8"))
        except Exception as exc:
            問題.append(f"v3関係写像を読めない: {exc}")
        else:
            if 写像データ.get("status") != "COVERED":
                問題.append("v3関係写像statusがCOVEREDではない")
            写像 = 写像データ.get("mapping")
            if not isinstance(写像, dict) or len(写像) != 13:
                問題.append("v3関係写像が13項目ではない")

    機械監査 = ルート / V3機械監査パス
    if 機械監査.exists():
        内容 = 機械監査.read_text(encoding="utf-8")
        for 句 in ["RELATION_MACHINE_AUDIT=PASS", "SOURCE_MAPPING_COUNT=13"]:
            if 句 not in 内容:
                問題.append(f"v3機械監査結果欠損: {句}")

    for 相対 in [V4変更記録パス, V4機械監査パス]:
        if not (ルート / 相対).exists():
            問題.append(f"v4観測成果物欠損: {相対}")

    v4変更 = ルート / V4変更記録パス
    if v4変更.exists():
        内容 = v4変更.read_text(encoding="utf-8")
        for 句 in [
            "作用状態 != 評価メタデータ",
            "状態遷移 != 得点更新",
            "再作用 != 再採点",
            "端到端構成再現 != fixture後段適合",
            "v3の七区別は維持",
        ]:
            if 句 not in 内容:
                問題.append(f"v4変更記録の必須記録欠損: {句}")

    v4機械 = ルート / V4機械監査パス
    if v4機械.exists():
        内容 = v4機械.read_text(encoding="utf-8")
        for 句 in ["V4_PRECISION_AUDIT=PASS", "V4_BOUNDARY_COUNT=7", "V3_SEVEN_CONDITIONS_PRESERVED=PASS"]:
            if 句 not in 内容:
                問題.append(f"v4機械監査結果欠損: {句}")

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
