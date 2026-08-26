from __future__ import annotations

import importlib.util, json, unittest
from pathlib import Path

class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[1]
        script=cls.root/"scripts/規定監査.py"
        spec=importlib.util.spec_from_file_location("規定監査",script); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); cls.module=module
    def test_規定監査に問題がない(self): self.assertEqual(self.module.監査(),[])
    def test_正本入口はREADME_mdのみ(self):
        self.assertTrue((self.root/"README.md").exists()); self.assertFalse((self.root/"README.ja.md").exists())
    def test_正本索引がv3確定状態(self):
        d=json.loads((self.root/"規定/正本索引.json").read_text(encoding="utf-8"))
        self.assertEqual(d["正式名称"],"大規模言語模型成立規定"); self.assertEqual(d["版"],"2026-08-27-成立規定-3"); self.assertEqual(d["状態"],"局所安定正本・再開放可")
    def test_自然言語限定を解除(self):
        d=json.loads((self.root/"規定/正本索引.json").read_text(encoding="utf-8")); self.assertFalse(d["言語射程"]["自然言語限定"]); self.assertIn("プログラム言語",d["言語射程"]["例"])
    def test_言語模型性と構成再現を分離(self):
        d=json.loads((self.root/"規定/正本索引.json").read_text(encoding="utf-8"))
        self.assertEqual(d["言語模型性成立条件"],["独立対象","文脈依存関係","関係再利用","言語対応","局所対応"])
        self.assertEqual(len(d["構成再現条件"]),7); self.assertTrue(d["原則"]["言語模型性と構成再現適合を分離"])
    def test_構成再現語彙を保持(self):
        t=(self.root/"規定/01_基底語彙.md").read_text(encoding="utf-8")
        for x in ["## 状態分離","## 状態保持","## 状態更新","## 未確定差の共存","## 寄与調整","## 構成連鎖","## 形成済み関係"]: self.assertIn(x,t)
    def test_生成運用性は成立中核と分離(self):
        t=(self.root/"規定/02_大規模言語模型成立.md").read_text(encoding="utf-8"); self.assertIn("生成運用性を分離する",t); self.assertIn("外部文章生成を必須にしない",t)
    def test_v3監査成果物を保存(self):
        for x in ["2026-08-27_構成定義独立関係監査.md","2026-08-27_構成定義v3変更記録.md","2026-08-27_構成定義関係写像.json","2026-08-27_構成定義機械監査.txt"]: self.assertTrue((self.root/"観測"/x).exists())

if __name__=="__main__": unittest.main()
