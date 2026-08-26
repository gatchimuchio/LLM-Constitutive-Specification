from __future__ import annotations

import json
from pathlib import Path

ルート = Path(__file__).resolve().parents[1]
索引 = ルート / "規定" / "正本索引.json"
現行版 = "2026-08-27-成立規定-3"
現行状態 = "局所安定正本・再開放可"
正式名称 = "大規模言語模型成立規定"

必須ルート = {"README.md","PROJECT_MAP.md","CITATION.cff","LICENSE","LICENSE-APACHE-2.0","LICENSE-CC-BY-4.0","NOTICE"}
現役禁止名 = {"layer0_functional_conformance_v4.py","llm_minimal_architecture_groups_v3_0.py","README.ja.md","REPOSITORY_GIT_BLOB_MANIFEST.txt","REPOSITORY_SHA256_MANIFEST.txt","appendices","artifacts","layer0_recomposition_memory_demo_bilingual_bundle","LICENSE-MIT"}


def 監査() -> list[str]:
    問題=[]
    for name in sorted(必須ルート):
        if not (ルート/name).exists(): 問題.append(f"必須ルートファイル欠損: {name}")
    if not 索引.exists(): return 問題+["正本索引が存在しない"]
    try: data=json.loads(索引.read_text(encoding="utf-8"))
    except Exception as exc: return 問題+[f"正本索引を読めない: {exc}"]
    if data.get("規定言語")!="日本語": 問題.append("規定言語が日本語ではない")
    if data.get("正式名称")!=正式名称: 問題.append("正式名称が不一致")
    if data.get("版")!=現行版: 問題.append("版が現行正本と一致しない")
    if data.get("状態")!=現行状態: 問題.append("状態が局所安定正本ではない")
    scope=data.get("言語射程",{})
    if scope.get("自然言語限定") is not False or "プログラム言語" not in scope.get("例",[]): 問題.append("言語射程がv3正本と一致しない")
    if data.get("言語模型性成立条件") != ["独立対象","文脈依存関係","関係再利用","言語対応","局所対応"]: 問題.append("言語模型性成立条件が五区別でない")
    expected_repro=["状態分離・保持・更新","意味・関係同一性追跡","未確定差の共存","寄与調整と確定分離","構成連鎖 / 再作用・再結合","再作用閉包 / 終端成立差","形成済み関係の保持 / 作用機構との分離"]
    if data.get("構成再現条件") != expected_repro: 問題.append("構成再現条件がv3正本と一致しない")
    if data.get("局所対応必須監査") != ["差分追従","複数対照への再利用","再現性"]: 問題.append("局所対応必須監査が不一致")
    aux=data.get("局所対応補助監査",[])
    if "保存追従" not in aux or "破壊追従" not in aux: 問題.append("局所対応補助監査が不一致")
    if data.get("規模面") != ["状態域規模","関係域規模","共有適用規模"]: 問題.append("規模三面が不一致")
    principles=data.get("原則",{})
    for key in ["生成運用性をLLM成立から分離","MINIDORAを成立証人にしない","HDS_Compilerを成立証人にしない","言語模型性と構成再現適合を分離"]:
        if principles.get(key) is not True: 問題.append(f"原則欠損: {key}")
    canonical=data.get("正本",[])
    for rel in canonical:
        p=ルート/str(rel)
        if not p.exists(): 問題.append(f"正本欠損: {rel}")
        elif not p.read_text(encoding="utf-8").strip(): 問題.append(f"正本が空: {rel}")
    required_obs=["観測/2026-08-26_修正後ダブルチェック.md","観測/2026-08-27_構成定義独立関係監査.md","観測/2026-08-27_構成定義v3変更記録.md","観測/2026-08-27_構成定義関係写像.json","観測/2026-08-27_構成定義機械監査.txt"]
    for rel in required_obs:
        if not (ルート/rel).exists(): 問題.append(f"観測成果物欠損: {rel}")
    basic=(ルート/"規定/01_基底語彙.md").read_text(encoding="utf-8") if (ルート/"規定/01_基底語彙.md").exists() else ""
    for phrase in ["## 状態分離","## 状態保持","## 状態更新","## 未確定差の共存","## 寄与調整","## 構成連鎖","## 形成済み関係"]:
        if phrase not in basic: 問題.append(f"基底語彙のv3語義欠損: {phrase}")
    main=(ルート/"規定/02_大規模言語模型成立.md").read_text(encoding="utf-8") if (ルート/"規定/02_大規模言語模型成立.md").exists() else ""
    for phrase in ["言語模型性の成立条件","構成再現条件","寄与調整と確定分離","再作用閉包 / 終端成立差","生成運用性を分離する","大規模性"]:
        if phrase not in main: 問題.append(f"成立規定のv3必須句欠損: {phrase}")
    readme=(ルート/"README.md").read_text(encoding="utf-8") if (ルート/"README.md").exists() else ""
    for phrase in [正式名称,現行版,"局所安定正本","構成再現条件","CC-BY-4.0","Apache License 2.0","LICENSE-APACHE-2.0","LICENSE-CC-BY-4.0"]:
        if phrase not in readme: 問題.append(f"README必須句欠損: {phrase}")
    citation=(ルート/"CITATION.cff").read_text(encoding="utf-8") if (ルート/"CITATION.cff").exists() else ""
    if f'version: "{現行版}"' not in citation: 問題.append("CITATION.cff版不一致")
    for forbidden in sorted(現役禁止名):
        if (ルート/forbidden).exists(): 問題.append(f"旧規定資産または禁止物が現役ルートに残存: {forbidden}")
    if not (ルート/"旧規定/README.md").exists(): 問題.append("旧規定への履歴導線がない")
    return 問題


def main()->int:
    issues=監査()
    if issues:
        print("規定監査: 不合格")
        for issue in issues: print(f"- {issue}")
        return 1
    print("規定監査: 合格")
    return 0

if __name__ == "__main__": raise SystemExit(main())
