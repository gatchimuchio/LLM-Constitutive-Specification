from __future__ import annotations
import importlib.util, json, unittest
from pathlib import Path

class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[1]
        spec=importlib.util.spec_from_file_location("規定監査",cls.root/"scripts/規定監査.py")
        assert spec and spec.loader
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); cls.mod=mod
    def index(self): return json.loads((self.root/"規定/正本索引.json").read_text(encoding="utf-8"))
    def read(self,p): return (self.root/p).read_text(encoding="utf-8")
    def test_監査_pass(self): self.assertEqual(self.mod.audit(),[])
    def test_v6(self): self.assertEqual(self.index()["版"],"2026-08-28-成立規定-6")
    def test_中核(self): self.assertEqual(self.index()["言語模型機能中核"],["言語状態空間","条件付き言語重み関係","持続模型関係","完全言語状態への接続"])
    def test_v5四条件を保存しない(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertNotIn("現行版では、模型内在条件を次の四条件へ整理する",t)
    def test_ngram_positive(self): self.assertIn("### n-gram",self.read("規定/05_観測と判定.md"))
    def test_compiler_posthoc_negative(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("後付けで「その出力へ重み1、他へ0」",t)
        self.assertIn("compiler / deterministic transducer",t)
    def test_BERT_MLM境界(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("BERT encoder artifact",t); self.assertIn("MLM pre-training system",t)
        self.assertIn("局所言語模型作用",t)
    def test_模型境界三層(self): self.assertEqual(self.index()["境界層"],["言語模型物","言語模型実行系","利用系"])
    def test_因果必要不変量分離(self):
        c=self.index()["構成語"]; self.assertFalse(c["同一語扱い"])
        self.assertEqual(set(c.keys()),{"因果寄与","必要性","不変","同一語扱い"})
    def test_再現四分(self): self.assertEqual(self.index()["再現種別"],["機能再現","能力再現","構造再現","因果機構再現"])
    def test_能力分離(self): self.assertIn("言語模型機能成立\n!=\n高推論能力",self.read("規定/02_大規模言語模型成立.md"))
    def test_LLM呼称分離(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("LLM機能等価",t); self.assertIn("現代LLM呼称適合",t)
    def test_scale_antigaming(self):
        s=self.index()["大規模性"]; self.assertTrue(s["比較集合事後選択禁止"]); self.assertTrue(s["模型物中心"])
    def test_監査記録(self):
        self.assertTrue((self.root/"観測/2026-08-28_構成定義v6独立再監査.md").exists())
        self.assertTrue((self.root/"観測/2026-08-28_構成定義v6機械監査.txt").exists())

if __name__=="__main__": unittest.main()
