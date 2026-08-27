from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location("規定監査", cls.root / "scripts" / "規定監査.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.audit = module

    def index(self):
        return json.loads((self.root / "規定" / "正本索引.json").read_text(encoding="utf-8"))

    def test_監査(self):
        self.assertEqual(self.audit.監査(), [])

    def test_v5_version(self):
        data = self.index()
        self.assertEqual(data["版"], "2026-08-28-成立規定-5")

    def test_旧五条件を維持しない(self):
        self.assertEqual(self.index()["言語模型性成立条件"], ["言語状態域", "条件付き言語差形成", "構成再利用", "言語状態接続"])
        self.assertNotIn("独立対象", self.index()["言語模型性成立条件"])
        self.assertNotIn("局所対応", self.index()["言語模型性成立条件"])

    def test_監査条件を模型条件から分離(self):
        self.assertEqual(self.index()["識別監査条件"], ["独立対象固定", "言語対応", "差分追従", "複数対照への再利用", "未列挙構成監査", "再現性"])

    def test_旧七条件を普遍化しない(self):
        self.assertFalse(self.index()["構成再現"]["普遍固定条件"])
        self.assertTrue(self.index()["構成再現"]["元模型相対"])

    def test_機能再現と構成再現を分離(self):
        self.assertEqual(self.index()["再現区分"], ["機能再現", "構成再現"])

    def test_形成済み模型状態が上位(self):
        self.assertEqual(self.index()["形成物"]["上位概念"], "形成済み模型状態")

    def test_retrievalを一律外周化しない(self):
        self.assertTrue(self.index()["模型境界"]["retrievalを一律外周化しない"])

    def test_規模三面を固定しない(self):
        self.assertFalse(self.index()["規模"]["固定面"])
        self.assertEqual(self.index()["規模"]["方式"], "規模プロファイル")

    def test_構成不変量に因果証拠を要求(self):
        text = (self.root / "規定" / "02_大規模言語模型成立.md").read_text(encoding="utf-8")
        self.assertIn("構成不変量の採用条件", text)
        self.assertIn("除去・無効化", text)
        self.assertIn("介入した状態差", text)

    def test_anti_lookup(self):
        text = (self.root / "規定" / "05_観測と判定.md").read_text(encoding="utf-8")
        self.assertIn("anti-lookup監査", text)
        self.assertIn("未列挙", text)

    def test_横断アーキテクチャを保持(self):
        text = (self.root / "規定" / "05_観測と判定.md").read_text(encoding="utf-8")
        for name in ["Llama", "BERT", "T5", "RWKV", "LLaDA", "REALM", "RETRO"]:
            self.assertIn(name, text)

    def test_条件数を保守しない(self):
        text = (self.root / "規定" / "06_再開放.md").read_text(encoding="utf-8")
        self.assertIn("条件数を保守しない", text)
        self.assertIn("五条件・七条件・三面", text)


if __name__ == "__main__":
    unittest.main()
