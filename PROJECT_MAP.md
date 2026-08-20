# プロジェクト地図

## 現在の目的

実装方式に依存しない Layer-0 機能適合フレームワークを維持し、候補システムの個別適合と、観測済みarchitecture family間での機能責任再現を分離して監査する。

日本語を現行正本とする。`.md` の英語系互換パスが残る場合も、現行判断は `.ja.md` 正本を優先する。

## 現行v4中核

| パス | 役割 |
|---|---|
| `README.md` / `README.ja.md` | 現行公開入口。日本語正本 |
| `layer0_functional_conformance_v4.py` | candidate-local v4適合評価器 |
| `docs/layer0_v4_spec.ja.md` | 現行正本仕様 |
| `docs/5モデル横断機能責任突合_2026-08-21.md` | Llama 3 / K2-V2 / OLMo 3 / Apertus 1.5 / Kimi K3 横断証拠 |
| `docs/claim_layers.ja.md` | 主張層と現在状態 |
| `docs/claim_boundary_and_semantics.ja.md` | 主張境界 |
| `docs/component_granularity_justification.ja.md` | 責任粒度と機構数の分離 |
| `tests/test_layer0_v4.py` | positive / negative conformance tests |
| `scripts/strict_manifest.py` | tracked inventory / content の厳格検証 |
| `REPOSITORY_GIT_BLOB_MANIFEST.txt` | 自身を除く正本inventory |
| `.github/workflows/audit.yml` | CI: `make test-all` |
| `docs/v3_legacy_status.ja.md` | v3 scope と legacy 分類 |

## 現在の主張位置

- L0-A: 実行可能
- L0-B: 観測集合で支持
- L0-C: 5つの異種モデル系統で支持
- L0-D: `PRINCIPLE_CANDIDATE / REOPEN_REQUIRED`
- L0-E: OPEN

L0-Cの支持は、異なる実装機構が**同じ名前の機構へ収束した**ことを意味しない。むしろ、Attention/KDA、Dense/MoE、text-only/multimodal等の差を越えて、上位の機能責任が再現したことを意味する。

## Legacy v3 material

次は再現性のため保持するが、現行の普遍主張面ではない。

- `llm_minimal_architecture_groups_v3_0.py`
- `appendices/layer_a_obligation_graph_enumeration_v0_5/`
- `artifacts/llm_minimal_architecture_groups_v3_0_*`
- v3-oriented reference / witness documents

## 再構成デモ

`layer0_recomposition_memory_demo_bilingual_bundle/` はarchitecture再構成のデモとして保持する。これ単独を普遍的Layer-0最小性の証拠とは扱わない。
