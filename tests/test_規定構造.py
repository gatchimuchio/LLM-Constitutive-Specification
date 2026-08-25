from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        script = cls.root / "scripts" / "規定監査.py"
        spec = importlib.util.spec_from_file_location("規定監査", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.module = module

    def test_規定監査に問題がない(self) -> None:
        self.assertEqual(self.module.監査(), [])

    def test_正本入口はREADME_mdのみ(self) -> None:
        self.assertTrue((self.root / "README.md").exists())
        self.assertFalse((self.root / "README.ja.md").exists())

    def test_旧active実装がルートにない(self) -> None:
        self.assertFalse((self.root / "layer0_functional_conformance_v4.py").exists())
        self.assertFalse((self.root / "llm_minimal_architecture_groups_v3_0.py").exists())
        self.assertFalse((self.root / "artifacts").exists())
        self.assertFalse((self.root / "appendices").exists())

    def test_正本索引がv2確定状態(self) -> None:
        data = json.loads((self.root / "規定" / "正本索引.json").read_text(encoding="utf-8"))
        self.assertEqual(data["正式名称"], "大規模言語模型成立規定")
        self.assertEqual(data["版"], "2026-08-26-成立規定-2")
        self.assertEqual(data["状態"], "局所安定正本・再開放可")
        self.assertEqual(data["規定言語"], "日本語")

    def test_自然言語限定を解除(self) -> None:
        data = json.loads((self.root / "規定" / "正本索引.json").read_text(encoding="utf-8"))
        self.assertFalse(data["言語射程"]["自然言語限定"])
        self.assertIn("プログラム言語", data["言語射程"]["例"])

    def test_必須監査と補助監査を分離(self) -> None:
        data = json.loads((self.root / "規定" / "正本索引.json").read_text(encoding="utf-8"))
        self.assertEqual(data["局所対応必須監査"], ["差分追従", "複数対照への再利用", "再現性"])
        self.assertIn("保存追従", data["局所対応補助監査"])
        self.assertIn("破壊追従", data["局所対応補助監査"])

    def test_大規模言語模型成立文書へ置換済み(self) -> None:
        self.assertTrue((self.root / "規定" / "02_大規模言語模型成立.md").exists())
        self.assertFalse((self.root / "規定" / "02_言語模型成立.md").exists())

    def test_生成運用性は成立中核と分離(self) -> None:
        text = (self.root / "規定" / "02_大規模言語模型成立.md").read_text(encoding="utf-8")
        self.assertIn("生成運用性を分離する", text)
        self.assertIn("外部文章生成を必須にしない", text)

    def test_成立差が正本語(self) -> None:
        text = (self.root / "規定" / "01_基底語彙.md").read_text(encoding="utf-8")
        self.assertIn("## 成立差", text)
        self.assertNotIn("## 形成差", text)

    def test_修正後ダブルチェックが存在(self) -> None:
        self.assertTrue((self.root / "観測" / "2026-08-26_修正後ダブルチェック.md").exists())


if __name__ == "__main__":
    unittest.main()
