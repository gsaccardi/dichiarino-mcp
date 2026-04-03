# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.2.1] - 2026-04-03

---

## [0.1.0] - 2025-04-03

### Added
- MCP server (`dichiarino`) with 12 tools for Italian Modello 730 tax return assistance
- `calcola_irpef` — IRPEF lorda calculation for tax years 2023, 2024, 2025
- `calcola_detrazione_lavoro` — work income tax credit + 2025 cuneo fiscale
- `calcola_detrazioni_familiari_tool` — spouse, children, and dependent deductions
- `calcola_oneri` — Quadro E deductions (medical, mortgage, renovation, university, etc.)
- `verifica_spesa_detraibile` — expense deductibility checker with quadro assignment
- `valida_codice_fiscale_tool` — Italian codice fiscale validator and parser
- `calcola_risultato_dichiarazione` — full 730 result (rimborso or debito)
- `guida_quadro` — step-by-step guide for all Quadri (A–W, M, T)
- `lista_documenti_spesa` — required documents for each expense type
- `genera_checklist_730` — personalised compilation checklist
- `calcola_addizionale_regionale_tool` — regional IRPEF surcharge for all 20 regions
- `analizza_certificazione_unica` — CU field consistency checker
- 4 MCP resources: IRPEF tables, Quadro instructions, deadlines, regional rates
- 6 portable Agent Skills for Claude, Cursor, and agentskills.io-compatible tools
- Static fiscal data for tax years 2023, 2024, and 2025
- Codice fiscale check-digit validation and field parsing
- 123 unit and integration tests (100% pass rate)
- Strict mypy type checking and Ruff linting
- CI workflow (Python 3.11–3.13) and PyPI release workflow
- Apache 2.0 license with attribution via NOTICE

[Unreleased]: https://github.com/gsaccardi/dichiarino-mcp/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/gsaccardi/dichiarino-mcp/compare/v0.1.0...v0.2.1
[0.1.0]: https://github.com/gsaccardi/dichiarino-mcp/releases/tag/v0.1.0
