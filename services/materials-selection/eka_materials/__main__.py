"""Offline evidence catalogues and material-index comparisons."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys

from .index_comparison import IndexWorksheet, compare_index, format_comparison
from .models import Catalogue
from .storage import CatalogueStore, canonical_json, digest_for, require_permission


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate an input catalogue without writing it")
    validate.add_argument("catalogue", type=Path)
    save = sub.add_parser("snapshot", help="store an immutable catalogue snapshot")
    save.add_argument("catalogue", type=Path)
    save.add_argument("--db", type=Path, required=True)
    show = sub.add_parser("show", help="read a snapshot if its source display rights allow it")
    show.add_argument("digest")
    show.add_argument("--db", type=Path, required=True)
    sub.add_parser("schema", help="print the JSON schema")
    rank = sub.add_parser("rank-index", help="compare manually screened candidates on one index")
    rank.add_argument("worksheet", type=Path)
    rank.add_argument("--json", action="store_true", help="include input evidence and pairwise results")
    args = parser.parse_args(argv)
    try:
        if args.command == "rank-index":
            sheet = IndexWorksheet.model_validate_json(args.worksheet.read_bytes())
            result = compare_index(sheet)
            print(json.dumps(result, indent=2) if args.json else format_comparison(result))
            return 0
        if args.command == "schema":
            print(json.dumps(Catalogue.model_json_schema(), indent=2))
            return 0
        if args.command == "show":
            if not args.db.is_file():
                raise ValueError("snapshot database does not exist")
            with CatalogueStore(args.db, read_only=True) as store:
                catalogue = store.get(args.digest)
            require_permission(catalogue, "display")
            print(canonical_json(catalogue))
            return 0
        catalogue = Catalogue.model_validate_json(args.catalogue.read_text(encoding="utf-8"))
        digest = digest_for(canonical_json(catalogue))
        if args.command == "snapshot":
            require_permission(catalogue, "retain")
            with CatalogueStore(args.db) as store:
                digest = store.put(catalogue)
        print(json.dumps({
            "status": "valid", "snapshot_sha256": digest,
            "stored": args.command == "snapshot",
            "grades": len(catalogue.grades), "observations": len(catalogue.observations),
            "synthetic_sources": sum(s.kind == "synthetic" for s in catalogue.sources),
            "sources": len(catalogue.sources), "engineering_validation": False,
        }, indent=2))
        return 0
    except (ValueError, KeyError, OSError, sqlite3.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
