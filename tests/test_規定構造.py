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
    def idx(self): return json.loads((self.root/"規定/正本索引.json").read_text(encoding="utf-8"))
    def read(self,p): return (self.root/p).read_text(encoding="utf-8")
    def test_監査(self): self.assertEqual(self.mod.audit(),[])
    def test_v7(self): self.assertEqual(self.idx()["版"],"2026-08-28-成立規定-7")
    def test_厳密LM中核(self): self.assertEqual(self.idx()["厳密LM中核"],["完全言語状態空間","整合した言語確率法則","持続模型状態","local-to-global接続"])
    def test_ngram(self): self.assertIn("n-gram",self.idx()["positive_control"][0])
    def test_energy(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("finite partition function",t); self.assertIn("正規化可能",t)
    def test_weighted_grammar_split(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("arbitrary weighted grammar",t); self.assertIn("probabilistic grammar",t)
    def test_variable_length(self): self.assertIn("EOS、停止法則、長さ分布",self.read("規定/02_大規模言語模型成立.md"))
    def test_delta_boundary(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("デルタ条件分布",t); self.assertIn("その系がlanguage distributionを模型化していることを示さない",t)
        self.assertNotIn("一意出力を事後的にデルタ分布へ読み替えることを禁止する",t)
    def test_BERT_MLM(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("BERT encoder artifact",t); self.assertIn("joint distribution",t)
    def test_模型境界(self): self.assertEqual(self.idx()["境界層"],["言語模型物","言語模型実行系","利用系"])
    def test_因果文書境界(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("因果効果の十分証拠ではない",t)
        self.assertIn("実行意味から依存関係を形式的に導ける",t)
    def test_再現四分(self): self.assertEqual(self.idx()["再現種別"],["機能再現","能力再現","構造再現","因果機構再現"])
    def test_能力分離(self): self.assertIn("GPQAは能力監査",self.read("規定/02_大規模言語模型成立.md"))
    def test_scale(self): self.assertTrue(self.idx()["大規模性"]["比較集合事後選択禁止"])
    def test_v6_core_removed(self): self.assertNotIn("→ 条件付き言語重み W_M(. | c)",self.read("規定/02_大規模言語模型成立.md"))
    def test_audit_records(self):
        self.assertTrue((self.root/"観測/2026-08-28_構成定義v7独立再監査.md").exists())
        self.assertTrue((self.root/"観測/2026-08-28_構成定義v7機械監査.txt").exists())

    def test_degenerate_distribution_not_banned(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("退化分布そのものは禁止しない",t)
        self.assertIn("入出力写像という外延だけでは",t)
    def test_sample_space_closure(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("標本空間そのものを先に固定",t)
        self.assertIn("無限系列",t)
    def test_source_semantics_causal_boundary(self):
        t=self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("実行意味から依存関係を形式的に導ける",t)
        self.assertIn("因果効果の十分証拠ではない",t)

if __name__=="__main__": unittest.main()
