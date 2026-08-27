from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-08-28-成立規定-6"
INDEX = ROOT / "規定" / "正本索引.json"
CORE = ["言語状態空間", "条件付き言語重み関係", "持続模型関係", "完全言語状態への接続"]


def audit() -> list[str]:
    p=[]
    d=json.loads(INDEX.read_text(encoding="utf-8"))
    if d.get("版") != VERSION: p.append("版不一致")
    if d.get("言語模型機能中核") != CORE: p.append("中核不一致")
    if d.get("境界層") != ["言語模型物","言語模型実行系","利用系"]: p.append("境界三層不一致")
    if d.get("再現種別") != ["機能再現","能力再現","構造再現","因果機構再現"]: p.append("再現四分不一致")
    cg=d.get("構成語",{})
    if cg.get("同一語扱い") is not False: p.append("構成語混同")
    for k in ["因果寄与","必要性","不変"]:
        if not cg.get(k): p.append(f"構成語欠損:{k}")
    if d.get("大規模性",{}).get("比較集合事後選択禁止") is not True: p.append("scale anti-gaming欠損")

    must={
      "規定/01_基底語彙.md":["## 条件付き言語重み関係","## 局所言語模型作用","## 構成因果寄与","## 構成必要条件","## 構成不変量","## 構造再現","## 因果機構再現"],
      "規定/02_大規模言語模型成立.md":["条件付き言語重み関係","後付けで「その出力へ重み1、他へ0」","n-gram","BERT encoder artifact","MLM pre-training system","言語模型物 != 言語模型実行系 != 利用系","構成因果寄与","構成必要条件","構造再現","因果機構再現","現代LLM呼称適合"],
      "規定/03_規模記述.md":["比較集合を事後選択","模型物規模","実行系規模","利用外周の規模を無言で"],
      "規定/04_運用境界.md":["言語模型物 != 言語模型実行系 != 利用系","REALM / RETRO型retrieval"],
      "規定/05_観測と判定.md":["### n-gram","compiler境界監査","anti-posthoc監査","構成必要条件","BERT encoder artifact","MLM pre-training system","現代LLM呼称監査"],
      "規定/06_再開放.md":[VERSION,"n-gram","compiler / transducer","構成因果寄与 / 構成必要条件 / 構成不変量"],
      "README.md":[VERSION,"条件付き言語重み関係","compiler境界","n-gram境界","BERT境界","言語模型物 != 言語模型実行系 != 利用系","構成因果寄与 != 構成必要条件 != 構成不変量"]
    }
    for rel,phrases in must.items():
        f=ROOT/rel
        if not f.exists(): p.append(f"欠損:{rel}"); continue
        txt=f.read_text(encoding="utf-8")
        for s in phrases:
            if s not in txt: p.append(f"必須句欠損:{rel}:{s}")

    t=(ROOT/"規定/02_大規模言語模型成立.md").read_text(encoding="utf-8")
    for banned in ["現行版では、模型内在条件を次の四条件へ整理する","言語模型機能を三関係で記述する"]:
        if banned in t: p.append(f"旧中核残存:{banned}")

    m=ROOT/"観測/2026-08-28_構成定義v6機械監査.txt"
    if not m.exists(): p.append("v6機械監査欠損")
    else:
        mt=m.read_text(encoding="utf-8")
        for s in ["NGRAM_POSITIVE_CONTROL=true","COMPILER_POSTHOC_DELTA_FORBIDDEN=true","CAUSAL_CONTRIBUTION_NECESSITY_INVARIANT_SEPARATED=true","STATUS=PASS"]:
            if s not in mt: p.append(f"機械監査欠損:{s}")
    return p


def main():
    p=audit()
    if p:
        print("規定監査: 不合格")
        for x in p: print("-",x)
        return 1
    print("規定監査: 合格")
    return 0

if __name__ == "__main__": raise SystemExit(main())
