# Dichiarino - Contributing Guide

Thank you for contributing to Dichiarino! Please follow these guidelines.

## Setup

```bash
git clone https://github.com/gsaccardi/dichiarino-mcp.git
cd dichiarino-mcp
uv sync --dev
```

## Before submitting a PR

```bash
uv run ruff check src/ tests/   # lint
uv run ruff format src/ tests/  # format
uv run mypy src/                # type check
uv run pytest                   # tests
```

All four must pass. The CI will enforce this.

## Adding a new expense type (TipoSpesa)

1. Add the enum value in `src/dichiarino/types.py`
2. Add the `LimiteDetrazione` in `src/dichiarino/data/limiti_detrazioni.py`
3. Add the documents list in `src/dichiarino/tools/checklist_documenti.py`
4. Add a test case in `tests/integration/test_server.py`
5. Update `docs/tools.md` with the new type

## Adding a new tax year

1. Add `SCAGLIONI_{YEAR}` in `src/dichiarino/data/aliquote_irpef.py`
2. Add the year to `SCAGLIONI_PER_ANNO`
3. Update `ADDIZIONALI_REGIONALI_{YEAR}` with new rates
4. Add new deduction limits if changed
5. Add tests for the new year in `tests/calculators/test_irpef.py`

## Attribution

All contributions remain under the Apache License 2.0.
By contributing, you agree that your contributions will be licensed under Apache-2.0.
