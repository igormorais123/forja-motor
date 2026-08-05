"""Regressões dos limites arquiteturais do harness FORJA."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def local_imports(module_name: str) -> set[str]:
    tree = ast.parse((ROOT / f"{module_name}.py").read_text(encoding="utf-8"))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module.split(".")[0])
    return {name for name in result if (ROOT / f"{name}.py").is_file()}


class ForjaArchitectureTests(unittest.TestCase):
    def test_package_and_n4_do_not_form_an_import_cycle(self) -> None:
        package_edges = local_imports("forja_package")
        n4_edges = local_imports("forja_n4_validate")

        self.assertIn("forja_n4_validate", package_edges)
        self.assertNotIn("forja_package", n4_edges)
        self.assertIn("forja_f8_contract", package_edges)
        self.assertIn("forja_f8_contract", n4_edges)

    def test_public_validate_f8_is_the_neutral_contract(self) -> None:
        from forja_f8_contract import validate_f8 as contract
        from forja_package import validate_f8 as public_api

        self.assertIs(contract, public_api)


if __name__ == "__main__":
    unittest.main()
