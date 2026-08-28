from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-08-28-成立規定-8"
INDEX = ROOT / "規定/正本索引.json"
CORE = [
    "完全言語状態空間",
    "持続模型状態",
    "整合した言語確率法則",
    "局所条件から完全法則への接続",
]
TOP_REPO = "https://github.com/gatchimuchio/cognitive-engineering-foundations"
TOP_COMMIT = "60131da52ba7931ed7f82c7648a74ac790f50d08"
ABILITY_AXES = [
    "状態担体", "作用", "状態差", "後続利用", "参照変更",
    "経路変更", "計算量変更", "再参照", "再結合", "循環尺度",
]


def _標準出力UTF8化() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="strict")


def audit() -> list[str]:
    誤り: list[str] = []
    try:
        索引 = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"正本索引読込失敗:{exc}"]

    if 索引.get("版") != VERSION:
        誤り.append("版不一致")
    if 索引.get("規定言語") != "日本語":
        誤り.append("規定言語不一致")
    if 索引.get("基底言語") != "日本語":
        誤り.append("基底言語不一致")
    if 索引.get("厳密言語模型中核") != CORE:
        誤り.append("厳密言語模型中核不一致")
    if 索引.get("能力作用観測単位") != ABILITY_AXES:
        誤り.append("能力作用観測単位不一致")
    if 索引.get("境界層") != ["言語模型物", "言語模型実行系", "利用系"]:
        誤り.append("境界三分不一致")
    if 索引.get("再現種別") != ["機能再現", "能力再現", "構造再現", "因果機構再現"]:
        誤り.append("再現四分不一致")

    最上位 = 索引.get("最上位理論正本", {})
    if 最上位.get("リポジトリ") != TOP_REPO:
        誤り.append("最上位理論正本リポジトリ不一致")
    if 最上位.get("参照コミット") != TOP_COMMIT:
        誤り.append("最上位理論正本commit不一致")

    必須資料 = {
        "規定/00_規定言語.md": [
            TOP_REPO,
            "唯一の基底・規定言語",
            "実務上やむを得ない接続面",
            "他言語を削除しても日本語だけで意味が閉じる",
        ],
        "規定/01_基底語彙.md": [
            "## 言語確率法則",
            "## 言語得点関係",
            "## 厳密言語模型",
            "## 局所条件から完全法則への接続",
            "## 状態担体",
            "## 後続利用",
            "## 経路変更",
            "## 循環尺度",
        ],
        "規定/02_大規模言語模型成立.md": [
            "一つの整合した言語確率法則",
            "局所条件から完全法則への接続",
            "退化分布そのものは禁止しない",
            "言語模型物\n≠ 言語模型実行系\n≠ 利用系",
            "能力作用は `07_能力作用構成.md` で別に監査",
            "再開放は固定順序では行わず",
        ],
        "規定/03_規模記述.md": [
            "比較集合を事後選択",
            "模型物規模",
            "形成規模",
            "利用系規模",
        ],
        "規定/04_運用境界.md": [
            "言語模型物\n≠ 言語模型実行系\n≠ 利用系",
            "参照取得統合系",
            "外部実行循環",
            "能力作用構成同一性",
        ],
        "規定/05_観測と判定.md": [
            "## 2. 厳密言語模型監査",
            "## 9. 能力作用監査",
            "状態が作られた\n≠ 後続で使われた",
            "退化分布自体は禁止しない",
            "日本語側の切り出し",
        ],
        "規定/06_再開放.md": [
            VERSION,
            "固定列は廃止する",
            "これは**優先順位ではない**",
            "循環再帰",
            "cognitive-engineering-foundations",
        ],
        "規定/07_能力作用構成.md": [
            "厳密言語模型成立\n≠\n高能力",
            "状態が存在する\n≠ 状態が後続利用される",
            "能力作用横断候補",
            "保存状態数815 / 再利用0",
        ],
        "README.md": [
            VERSION,
            "基底言語・規定言語: **日本語**",
            "局所条件から完全法則への接続",
            "能力作用構成",
            "固定された「再開放順序」を廃止",
        ],
        "PROJECT_MAP.md": [
            VERSION,
            "認知工学基底理論",
            "状態担体",
            "固定された再開放順序は置かない",
        ],
    }

    for 相対, 句群 in 必須資料.items():
        path = ROOT / 相対
        if not path.exists():
            誤り.append(f"欠損:{相対}")
            continue
        本文 = path.read_text(encoding="utf-8")
        for 句 in 句群:
            if 句 not in 本文:
                誤り.append(f"必須句欠損:{相対}:{句}")

    if "規定/07_能力作用構成.md" not in 索引.get("正本", []):
        誤り.append("能力作用構成が正本索引にない")

    原則 = 索引.get("原則", {})
    for key in (
        "日本語を基底規定言語とする",
        "他言語は実務上必要な場合のみ例外使用",
        "能力作用構成を厳密言語模型成立条件へ混入しない",
        "再開放に固定順序を置かない",
    ):
        if 原則.get(key) is not True:
            誤り.append(f"原則不一致:{key}")

    for 旧語 in ("厳密LM中核", "local-to-global接続"):
        if 旧語 in 索引:
            誤り.append(f"旧索引語残存:{旧語}")

    機械 = ROOT / "観測/2026-08-28_構成定義v8機械監査.txt"
    if not 機械.exists():
        誤り.append("v8機械監査欠損")
    else:
        文 = 機械.read_text(encoding="utf-8")
        for 句 in (
            f"版={VERSION}",
            "規定言語=日本語",
            "厳密言語模型中核維持=true",
            "能力作用構成分離=true",
            "再開放固定順序=false",
            "循環再帰=true",
            "状態=合格",
        ):
            if 句 not in 文:
                誤り.append(f"機械監査欠損:{句}")

    return 誤り


def main() -> int:
    _標準出力UTF8化()
    誤り = audit()
    if 誤り:
        print("規定監査: 不合格")
        for 項目 in 誤り:
            print(f"- {項目}")
        return 1
    print("規定監査: 合格")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
