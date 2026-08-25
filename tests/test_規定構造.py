from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


class 規定構造試験(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        script = root / "scripts" / "規定監査.py"
        spec = importlib.util.spec_from_file_location("規定監査", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.module = module

    def test_規定監査に問題がない(self) -> None:
        self.assertEqual(self.module.監査(), [])

    def test_正本入口はREADME_mdのみ(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "README.md").exists())
        self.assertFalse((root / "README.ja.md").exists())

    def test_旧active実装がルートにない(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / "layer0_functional_conformance_v4.py").exists())
        self.assertFalse((root / "llm_minimal_architecture_groups_v3_0.py").exists())
        self.assertFalse((root / "artifacts").exists())
        self.assertFalse((root / "appendices").exists())


if __name__ == "__main__":
    unittest.main()
