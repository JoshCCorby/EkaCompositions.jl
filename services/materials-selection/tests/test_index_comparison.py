from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from eka_materials.__main__ import main
from eka_materials.index_comparison import IndexWorksheet, compare_index


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "synthetic-index.json"


class IndexComparisonTests(unittest.TestCase):
    def setUp(self):
        self.sheet = json.loads(EXAMPLE.read_text())
        self.candidate = self.sheet["candidates"][0]

    def compare(self):
        return compare_index(IndexWorksheet.model_validate_json(json.dumps(self.sheet)))

    def test_fictional_example(self):
        result = self.compare()
        low, high = result["candidates"][0]["index_bounds"]
        self.assertAlmostEqual(low, 8e6 / 1100)
        self.assertAlmostEqual(high, 10e6 / 1000)
        self.assertEqual(result["candidates"][0]["evidence"][0]["source"],
                         self.candidate["evidence"][0]["source"])
        self.assertEqual([p["preferred_on_index"] for p in result["comparisons"]],
                         [None, "Fiction A", "Fiction B"])

    def test_equivalent_units_and_order(self):
        initial = self.compare()
        density = self.candidate["evidence"][1]
        density.update(unit="kg/m^3", value={"kind": "range", "lower": 1000, "upper": 1100})
        self.sheet["candidates"].reverse()
        result = self.compare()
        self.assertEqual(initial["comparisons"], result["comparisons"])
        self.assertEqual(initial["candidates"][0]["index_bounds"],
                         result["candidates"][0]["index_bounds"])

    def test_screen_gates_comparison(self):
        for status in ("fail", "unknown", "conflict"):
            with self.subTest(status=status):
                self.candidate["screen"] = status
                result = self.compare()
                self.assertIsNone(result["candidates"][0]["index_bounds"])
                self.assertEqual(len(result["comparisons"]), 1)

    def test_minimize_and_fractional_power(self):
        self.sheet.update(direction="minimize", powers={"tensile_yield_strength": 0.5})
        result = self.compare()
        self.assertAlmostEqual(result["candidates"][0]["index_bounds"][0], (8e6)**0.5)
        self.assertEqual(result["comparisons"][1]["preferred_on_index"], "Fiction C")

    def test_touching_ranges_have_no_forced_order(self):
        self.sheet["powers"] = {"tensile_yield_strength": 1}
        self.candidate["evidence"][0]["value"]["upper"] = 15
        self.assertIsNone(self.compare()["comparisons"][0]["preferred_on_index"])

    def test_duplicate_evidence_needs_review(self):
        other = deepcopy(self.candidate["evidence"][0])
        other["value"] = {"kind": "point", "lower": 53, "upper": 53}
        self.candidate["evidence"].append(other)
        self.assertIsNone(self.compare()["candidates"][0]["index_bounds"])
        other["applicability"] = "inapplicable"
        self.assertIsNotNone(self.compare()["candidates"][0]["index_bounds"])

    def test_unknown_inapplicable_and_absent_inputs(self):
        row = self.candidate["evidence"][0]
        for applicability in ("unknown", "inapplicable"):
            row["applicability"] = applicability
            self.assertIsNone(self.compare()["candidates"][0]["index_bounds"])
        self.candidate["evidence"].remove(row)
        self.assertIsNone(self.compare()["candidates"][0]["index_bounds"])

    def test_open_missing_and_zero_denominator(self):
        row = self.candidate["evidence"][1]
        for value in ({"kind": "upper_bound", "upper": 1.1},
                      {"kind": "missing", "missing_reason": "Unmeasured"},
                      {"kind": "range", "lower": 0, "upper": 1.1}):
            row["value"] = value
            self.assertIsNone(self.compare()["candidates"][0]["index_bounds"])

    def test_cli_success_and_bad_dimension(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["rank-index", str(EXAMPLE), "--json"]), 0)
        self.assertEqual(len(json.loads(output.getvalue())["comparisons"]), 3)
        with TemporaryDirectory() as temp:
            self.candidate["evidence"][0]["unit"] = "m"
            path = Path(temp) / "bad.json"
            path.write_text(json.dumps(self.sheet))
            with redirect_stderr(StringIO()):
                self.assertEqual(main(["rank-index", str(path)]), 2)
