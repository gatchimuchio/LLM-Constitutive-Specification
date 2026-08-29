from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location("規定監査", cls.root / "scripts/規定監査.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cls.mod = mod

    def idx(self):
        return json.loads((self.root / "規定/正本索引.json").read_text(encoding="utf-8"))

    def read(self, path: str):
        return (self.root / path).read_text(encoding="utf-8")

    def test_監査(self):
        self.assertEqual(self.mod.audit(), [])

    def test_v9凍結(self):
        idx = self.idx()
        self.assertEqual(idx["版"], "2026-08-29-成立規定-9")
        self.assertEqual(idx["状態"], "凍結正本・射程内反例時のみ再開放")
        self.assertTrue(idx["原則"]["凍結後は射程内反例のみ再開放"])

    def test_日本語基底(self):
        idx = self.idx()
        self.assertEqual(idx["規定言語"], "日本語")
        self.assertEqual(idx["基底言語"], "日本語")
        self.assertTrue(idx["原則"]["他言語は実務上必要な場合のみ例外使用"])
        self.assertIn("唯一の基底・規定言語", self.read("規定/00_規定言語.md"))

    def test_最上位理論正本(self):
        top = self.idx()["最上位理論正本"]
        self.assertEqual(top["リポジトリ"], "https://github.com/gatchimuchio/cognitive-engineering-foundations")
        self.assertEqual(top["参照コミット"], "60131da52ba7931ed7f82c7648a74ac790f50d08")

    def test_v8中核を維持(self):
        self.assertEqual(
            self.idx()["厳密言語模型中核"],
            ["完全言語状態空間", "持続模型状態", "整合した言語確率法則", "局所条件から完全法則への接続"],
        )

    def test_ngramを方式名で排除しない(self):
        self.assertIn("n-gram言語模型", self.idx()["成立対照"])

    def test_エネルギー境界(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("有限で正の正規化定数", text)
        self.assertIn("正規化可能な法則", text)

    def test_重み付き文法を分ける(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("任意重み付き文法", text)
        self.assertIn("確率文法型言語模型", text)

    def test_可変長(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("終端記号、停止法則、長さ分布", text)
        self.assertIn("無限系列", text)

    def test_退化分布境界(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("退化分布そのものは禁止しない", text)
        self.assertIn("事後的に一意出力へ確率1を付ける", text)

    def test_BERT境界(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("BERT符号化器", text)
        self.assertIn("伏字予測", text)
        self.assertIn("完全分布", text)

    def test_模型境界(self):
        self.assertEqual(self.idx()["境界層"], ["言語模型物", "言語模型実行系", "利用系"])

    def test_再現四分(self):
        self.assertEqual(self.idx()["再現種別"], ["機能再現", "能力再現", "構造再現", "因果機構再現"])

    def test_能力作用を独立させる(self):
        idx = self.idx()
        self.assertEqual(
            idx["能力作用観測単位"],
            ["状態担体", "作用", "状態差", "後続利用", "参照変更", "経路変更", "計算量変更", "再参照", "再結合", "循環尺度"],
        )
        self.assertTrue(idx["原則"]["能力作用構成を厳密言語模型成立条件へ混入しない"])
        self.assertIn("厳密言語模型成立\n≠\n高能力", self.read("規定/07_能力作用構成.md"))

    def test_状態存在と後続利用を分ける(self):
        text = self.read("規定/07_能力作用構成.md")
        self.assertIn("状態が存在する\n≠ 状態が後続利用される", text)
        self.assertIn("保存状態数815 / 再利用0", text)

    def test_循環尺度を分ける(self):
        text = self.read("規定/07_能力作用構成.md")
        for phrase in ("深さ方向輸送", "系列持続更新", "内部反復", "外部実行循環", "形成循環"):
            self.assertIn(phrase, text)

    def test_因果境界(self):
        text = self.read("規定/02_大規模言語模型成立.md")
        self.assertIn("因果効果の十分根拠ではない", text)
        self.assertIn("実行意味から依存関係を直接導ける", text)

    def test_局所作用と意思決定構造を分ける(self):
        text = self.read("規定/08_構成定義の到達限界.md")
        for phrase in ("観測可能な局所作用群", "局所作用再現", "作用関係再現", "意思決定構造再現", "能力主体"):
            self.assertIn(phrase, text)
        self.assertTrue(self.idx()["原則"]["局所作用群を意思決定構造へ昇格しない"])

    def test_MINIDORAとHDS境界(self):
        idx = self.idx()["MINIDORA_HDS境界"]
        self.assertTrue(idx["MINIDORAでHDS判断主体が必要"])
        self.assertTrue(idx["HDSをLLM普遍成立条件にしない"])
        self.assertTrue(idx["HDS内部原理を本規定で定義しない"])
        self.assertTrue(idx["HDS改定を本規定へ自動逆流させない"])
        text = self.read("規定/08_構成定義の到達限界.md")
        self.assertIn("HDSは本構成定義の答えではない", text)
        self.assertIn("MINIDORAではHDSを採用する", text)

    def test_HDS変更で再開放しない(self):
        text = self.read("規定/06_再開放.md")
        self.assertIn("HDSの内部原理・判断規則・実装の変更", text)
        self.assertIn("HDSは本規定の射程外", text)

    def test_再開放に固定順序を置かない(self):
        text = self.read("規定/06_再開放.md")
        self.assertIn("固定列は廃止する", text)
        self.assertIn("これは**優先順位ではない**", text)
        self.assertTrue(self.idx()["原則"]["再開放に固定順序を置かない"])

    def test_循環再帰(self):
        text = self.read("規定/06_再開放.md")
        for phrase in ("構成定義", "構文化", "実装", "実測"):
            self.assertIn(phrase, text)

    def test_大規模性(self):
        self.assertTrue(self.idx()["大規模性"]["比較集合事後選択禁止"])

    def test_v9監査記録(self):
        self.assertTrue((self.root / "観測/2026-08-29_構成定義v9変更記録.md").exists())
        self.assertTrue((self.root / "観測/2026-08-29_構成定義v9再監査.md").exists())
        self.assertTrue((self.root / "観測/2026-08-29_構成定義v9機械監査.txt").exists())

    def test_FROZEN(self):
        self.assertTrue((self.root / "FROZEN.md").exists())
        self.assertIn("通常改訂は停止する", self.read("FROZEN.md"))


if __name__ == "__main__":
    unittest.main()
