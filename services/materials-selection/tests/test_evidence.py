from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from pydantic import ValidationError

from eka_materials.__main__ import main
from eka_materials.models import Catalogue, NumericValue
from eka_materials.storage import CatalogueStore, canonical_json, digest_for, require_permission
from eka_materials.units import normalize


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "synthetic-catalogue.json"


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.catalogue = self.parse(self.raw)

    @staticmethod
    def parse(payload):
        return Catalogue.model_validate_json(json.dumps(payload))

    def test_fixture_has_distinct_identities_and_no_real_data(self):
        self.assertEqual(len(self.catalogue.grades), 3)
        self.assertEqual(len(self.catalogue.variants), 3)
        self.assertEqual(len(self.catalogue.observations), 9)
        self.assertEqual(len(self.catalogue.tasks), 3)
        self.assertTrue(all(s.kind == "synthetic" for s in self.catalogue.sources))
        self.assertTrue(all(s.url.host == "example.invalid" for s in self.catalogue.sources))
        self.assertEqual(self.catalogue.offers[0].availability, "unknown")
        self.assertIsNone(self.catalogue.offers[0].region)

    def test_same_designation_does_not_merge_grades(self):
        self.raw["grades"][1]["designation"] = self.raw["grades"][0]["designation"]
        self.assertEqual(len(self.parse(self.raw).grades), 3)

    def test_roundtrip_preserves_all_records(self):
        restored = Catalogue.model_validate_json(canonical_json(self.catalogue))
        self.assertEqual(canonical_json(restored), canonical_json(self.catalogue))

    def test_normalization_keeps_original_value_unit_and_provenance(self):
        observation = self.catalogue.observations[3]
        before = observation.model_dump_json()
        converted = observation.value.normalized(observation.unit, observation.property)
        self.assertAlmostEqual(converted.lower, 3100)
        self.assertAlmostEqual(converted.upper, 3300)
        self.assertEqual(observation.model_dump_json(), before)
        self.assertEqual(observation.source_id, "source:authored-a")
        self.assertEqual(observation.locator, "Authored row M1-D")

    def test_equivalent_units_and_offset_temperatures(self):
        self.assertAlmostEqual(normalize(1, "MPa", "tensile_yield_strength"), 1_000_000)
        self.assertAlmostEqual(normalize(1, "g/cm^3", "density"), 1000)
        self.assertAlmostEqual(normalize(100, "ohm*cm", "volume_resistivity"), 1)
        self.assertAlmostEqual(normalize(0, "degC", "service_temperature"), 273.15)
        self.assertAlmostEqual(normalize(32, "degF", "service_temperature"), 273.15)

    def test_bad_units_and_nonphysical_absolute_temperatures(self):
        for value, unit, prop in [
            (1, "W/m", "thermal_conductivity"), (1, "Pa", "density"),
            (1, "invented_unit", "density"), (-274, "degC", "service_temperature"),
            (20, "delta_degC", "service_temperature"),
        ]:
            with self.subTest(unit=unit, property=prop), self.assertRaises(ValueError):
                normalize(value, unit, prop)

    def test_missing_value_and_conditions_stay_unknown(self):
        missing = self.catalogue.observations[7]
        self.assertEqual(missing.value.kind, "missing")
        self.assertIsNone(missing.value.lower)
        self.assertIsNone(missing.value.upper)
        self.assertIsNone(missing.unit)
        self.assertIsNone(missing.conditions.temperature_k)
        self.assertEqual(self.catalogue.tasks[1].constraints, ())

    def test_conflicting_observations_are_preserved(self):
        matches = [o for o in self.catalogue.observations
                   if o.variant_id == "variant:demo-m1-bar" and o.property == "tensile_yield_strength"]
        self.assertEqual(len(matches), 2)
        self.assertEqual({o.basis for o in matches}, {"specified_limit", "measured"})
        self.assertEqual(len({o.source_id for o in matches}), 2)

    def test_bad_numeric_shapes_are_rejected(self):
        for value in [
            {"kind": "point", "lower": 3, "upper": 4},
            {"kind": "range", "lower": 4, "upper": 3},
            {"kind": "lower_bound", "lower": 3, "upper": 4},
            {"kind": "upper_bound", "lower": 3, "upper": 4},
            {"kind": "point", "lower": 3},
            {"kind": "missing"},
            {"kind": "missing", "lower": 0, "missing_reason": "Not reported"},
            {"kind": "point", "lower": 3, "upper": 3, "missing_reason": "Unknown"},
        ]:
            with self.subTest(value=value), self.assertRaises(ValidationError):
                NumericValue.model_validate_json(json.dumps(value))

    def test_strings_booleans_and_nonfinite_numbers_are_rejected(self):
        for bad in ["320", True, float("nan"), float("inf"), float("-inf")]:
            payload = deepcopy(self.raw)
            payload["observations"][0]["value"]["lower"] = bad
            with self.subTest(value=bad), self.assertRaises(ValidationError):
                self.parse(payload)

    def test_bad_conditions_and_empty_locators_are_rejected(self):
        for field, value in [("temperature_k", -1), ("humidity_percent", 101),
                             ("thickness_min_mm", -1), ("temperature_k", "298")]:
            payload = deepcopy(self.raw)
            payload["observations"][0]["conditions"][field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                self.parse(payload)
        self.raw["observations"][0]["locator"] = "   "
        with self.assertRaises(ValidationError):
            self.parse(self.raw)

    def test_reversed_thickness_is_rejected(self):
        self.raw["observations"][0]["conditions"]["thickness_min_mm"] = 20
        with self.assertRaises(ValidationError):
            self.parse(self.raw)

    def test_numeric_observation_requires_compatible_units(self):
        for unit in [None, "kg", "W/m"]:
            payload = deepcopy(self.raw)
            payload["observations"][0]["unit"] = unit
            with self.subTest(unit=unit), self.assertRaises(ValidationError):
                self.parse(payload)

    def test_wrong_type_references_are_rejected(self):
        for collection, field, target in [
            ("grades", "family_id", "grade:demo-m1"),
            ("variants", "grade_id", "family:demo-metal"),
            ("observations", "variant_id", "grade:demo-m1"),
            ("observations", "source_id", "missing:source"),
            ("offers", "variant_id", "grade:demo-m1"),
            ("offers", "source_id", "missing:source"),
        ]:
            payload = deepcopy(self.raw)
            payload[collection][0][field] = target
            with self.subTest(collection=collection, field=field), self.assertRaises(ValidationError):
                self.parse(payload)

    def test_duplicate_ids_and_constraints_are_rejected(self):
        payload = deepcopy(self.raw)
        payload["grades"][1]["id"] = payload["grades"][0]["id"]
        with self.assertRaises(ValidationError):
            self.parse(payload)
        payload = deepcopy(self.raw)
        payload["tasks"][0]["constraints"] *= 2
        with self.assertRaises(ValidationError):
            self.parse(payload)

    def test_unexpected_fields_unknown_properties_and_versions_are_rejected(self):
        for key, value in [("unexpected", 1), ("schema_version", 2), ("schema_version", True)]:
            payload = deepcopy(self.raw)
            payload[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValidationError):
                self.parse(payload)
        self.raw["observations"][0]["property"] = "ultimate_strength"
        with self.assertRaises(ValidationError):
            self.parse(self.raw)

    def test_derived_requirement_requires_its_derivation(self):
        self.raw["tasks"][0]["constraints"][0]["origin"]["kind"] = "derived"
        with self.assertRaises(ValidationError):
            self.parse(self.raw)

    def test_constraints_cannot_accept_unknown_basis_or_wrong_units(self):
        for field, value in [("acceptable_basis", ["not_stated"]),
                             ("acceptable_basis", []), ("unit", "kg"),
                             ("threshold", True), ("threshold", "200")]:
            payload = deepcopy(self.raw)
            payload["tasks"][0]["constraints"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                self.parse(payload)

    def test_strict_urls_and_dates(self):
        for field, value in [("url", "file:///tmp/source"), ("accessed_on", "yesterday")]:
            payload = deepcopy(self.raw)
            payload["sources"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                self.parse(payload)

    def test_record_order_does_not_change_snapshot_identity(self):
        for key in ("families", "grades", "variants", "sources", "observations", "tasks", "offers"):
            self.raw[key].reverse()
        self.assertEqual(canonical_json(self.parse(self.raw)), canonical_json(self.catalogue))

    def test_changes_to_evidence_revision_and_conditions_change_identity(self):
        original = digest_for(canonical_json(self.catalogue))
        for edit in ("revision", "temperature", "permission"):
            payload = deepcopy(self.raw)
            if edit == "revision":
                payload["sources"][0]["revision"] = "2"
            elif edit == "temperature":
                payload["observations"][0]["conditions"]["temperature_k"] = 300
            else:
                payload["sources"][0]["rights"]["display"] = "unknown"
            with self.subTest(edit=edit):
                self.assertNotEqual(digest_for(canonical_json(self.parse(payload))), original)

    def test_sqlite_roundtrip_deduplication_and_revision_retention(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "test.sqlite"
            with CatalogueStore(path) as store:
                first = store.put(self.catalogue)
                self.assertEqual(first, store.put(self.catalogue))
                self.raw["sources"][0]["revision"] = "2"
                second = store.put(self.parse(self.raw))
                self.assertNotEqual(first, second)
                self.assertEqual(store.get(first).sources[0].revision, "1")
                self.assertEqual(store.get(second).sources[0].revision, "2")
                self.assertEqual(store.connection.execute("SELECT count(*) FROM catalogue_snapshots").fetchone()[0], 2)
            with CatalogueStore(path, read_only=True) as store:
                self.assertEqual(canonical_json(store.get(first)), canonical_json(self.catalogue))
                with self.assertRaises(ValueError):
                    store.put(self.catalogue)

    def test_unknown_permissions_deny_storage_and_display(self):
        for status in ("unknown", "prohibited"):
            payload = deepcopy(self.raw)
            payload["sources"][0]["rights"]["retain"] = status
            with self.subTest(status=status), CatalogueStore(":memory:") as store:
                with self.assertRaises(ValueError):
                    store.put(self.parse(payload))
        self.raw["sources"][0]["rights"]["display"] = "unknown"
        with self.assertRaises(ValueError):
            require_permission(self.parse(self.raw), "display")

    def test_unknown_rights_default_to_denied(self):
        self.raw["sources"][0]["rights"] = {"basis": "No permission established", "checked_on": "2026-10-13"}
        catalogue = self.parse(self.raw)
        for operation in ("retain", "display", "redistribute"):
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                require_permission(catalogue, operation)

    def test_corrupted_or_absent_snapshot_is_rejected(self):
        with CatalogueStore(":memory:") as store:
            digest = store.put(self.catalogue)
            store.connection.execute("UPDATE catalogue_snapshots SET payload = '{}' WHERE digest = ?", (digest,))
            with self.assertRaises(ValueError):
                store.get(digest)
            with self.assertRaises(ValueError):
                store.put(self.catalogue)
            with self.assertRaises(KeyError):
                store.get("missing")

    def test_storage_revalidates_even_with_a_valid_hash(self):
        self.raw["observations"][0]["source_id"] = "source:missing"
        invalid_payload = json.dumps(self.raw)
        digest = digest_for(invalid_payload)
        with CatalogueStore(":memory:") as store:
            store.connection.execute("INSERT INTO catalogue_snapshots VALUES (?, ?)", (digest, invalid_payload))
            with self.assertRaises(ValidationError):
                store.get(digest)
            invalid_model = self.catalogue.model_copy(update={"schema_version": 2})
            with self.assertRaises(ValidationError):
                store.put(invalid_model)

    def test_read_only_missing_database_is_not_created(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "absent.sqlite"
            with self.assertRaises(sqlite3.Error):
                CatalogueStore(path, read_only=True)
            self.assertFalse(path.exists())

    def test_cli_validate_snapshot_show_and_schema(self):
        with TemporaryDirectory() as directory:
            db = str(Path(directory) / "demo.sqlite")
            out = StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["validate", str(FIXTURE)]), 0)
            result = json.loads(out.getvalue())
            self.assertFalse(result["stored"])
            self.assertFalse(result["engineering_validation"])
            out = StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["snapshot", str(FIXTURE), "--db", db]), 0)
            digest = json.loads(out.getvalue())["snapshot_sha256"]
            self.assertEqual(digest, result["snapshot_sha256"])
            out = StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["show", digest, "--db", db]), 0)
            self.assertEqual(canonical_json(Catalogue.model_validate_json(out.getvalue())), canonical_json(self.catalogue))
            out = StringIO()
            with redirect_stdout(out):
                self.assertEqual(main(["schema"]), 0)
            self.assertIn("$defs", json.loads(out.getvalue()))

    def test_cli_display_permission_and_bad_input(self):
        with TemporaryDirectory() as directory:
            db = str(Path(directory) / "demo.sqlite")
            self.raw["sources"][0]["rights"]["display"] = "unknown"
            with CatalogueStore(db) as store:
                digest = store.put(self.parse(self.raw))
            out, error = StringIO(), StringIO()
            with redirect_stdout(out), redirect_stderr(error):
                self.assertEqual(main(["show", digest, "--db", db]), 2)
                self.assertEqual(main(["validate", str(Path(directory) / "absent.json")]), 2)
            self.assertEqual(out.getvalue(), "")
            self.assertIn("display permission", error.getvalue())


if __name__ == "__main__":
    unittest.main()
