from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION="2026-08-28-成立規定-7"
INDEX=ROOT/"規定/正本索引.json"
CORE=["完全言語状態空間","整合した言語確率法則","持続模型状態","local-to-global接続"]

def audit():
    p=[]
    d=json.loads(INDEX.read_text(encoding="utf-8"))
    if d.get("版")!=VERSION: p.append("版不一致")
    if d.get("厳密LM中核")!=CORE: p.append("厳密LM中核不一致")
    if d.get("境界層")!=["言語模型物","言語模型実行系","利用系"]: p.append("境界三層不一致")
    if d.get("再現種別")!=["機能再現","能力再現","構造再現","因果機構再現"]: p.append("再現四分不一致")
    must={
      "規定/01_基底語彙.md":["## 言語確率法則","## 正規化可能言語測度","## 言語score関係","## 厳密言語模型","## 条件付き言語模型","## 局所言語予測作用","## 構成必要条件"],
      "規定/02_大規模言語模型成立.md":["一つの整合した言語確率法則","可変長","energy-based LM","probabilistic grammar","デルタ条件分布","事後的なデルタ表現","BERT encoder artifact","言語模型物 != 言語模型実行系 != 利用系","因果効果の十分証拠ではない"],
      "規定/03_規模記述.md":["比較集合を事後選択","模型物規模","形成規模","利用系規模"],
      "規定/04_運用境界.md":["言語模型物 != 言語模型実行系 != 利用系","retrieval統合系"],
      "規定/05_観測と判定.md":["厳密LM監査","energy-based LM","posthoc delta","退化分布自体は禁止しない","BERT encoder artifact","weighted grammar境界","実行意味から依存関係を形式的に導ける"],
      "規定/06_再開放.md":[VERSION,"正規化可能性","deterministic transducer","MLM / scoring / representation境界"],
      "README.md":[VERSION,"一つの整合した言語確率法則","energy LM","delta distribution","厳密LM != 局所予測 != scorer != representation != transducer"]
    }
    for rel, phrases in must.items():
        f=ROOT/rel
        if not f.exists(): p.append(f"欠損:{rel}"); continue
        t=f.read_text(encoding="utf-8")
        for s in phrases:
            if s not in t: p.append(f"必須句欠損:{rel}:{s}")
    core=(ROOT/"規定/02_大規模言語模型成立.md").read_text(encoding="utf-8")
    for old in ["→ 条件付き言語重み W_M(. | c)","確率正規化は普遍必須にしない","compiler posthoc-delta禁止: 採用"]:
        if old in core: p.append(f"旧v6中核残存:{old}")
    m=ROOT/"観測/2026-08-28_構成定義v7機械監査.txt"
    if not m.exists(): p.append("v7機械監査欠損")
    else:
        mt=m.read_text(encoding="utf-8")
        for s in ["STRICT_LM_GLOBAL_LAW=true","ENERGY_NORMALIZABILITY_BOUNDARY=true","POSTHOC_DELTA_IS_NOT_EVIDENCE=true","DEGENERATE_DISTRIBUTION_ALLOWED_WHEN_NATIVE=true","STATUS=PASS"]:
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
if __name__=="__main__": raise SystemExit(main())
