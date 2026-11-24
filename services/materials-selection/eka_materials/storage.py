"""Immutable, content-addressed catalogue snapshots in local SQLite."""

import hashlib
import json
from pathlib import Path
import sqlite3

from .models import Catalogue


def canonical_json(catalogue: Catalogue) -> str:
    checked = Catalogue.model_validate_json(catalogue.model_dump_json())
    payload = checked.model_dump(mode="json")
    for key in ("families", "grades", "variants", "sources", "observations", "tasks", "offers"):
        payload[key].sort(key=lambda item: item["id"])
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest_for(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def require_permission(catalogue: Catalogue, operation: str) -> None:
    if operation not in ("retain", "display", "redistribute"):
        raise ValueError("unknown permission operation")
    denied = [source.id for source in catalogue.sources
              if getattr(source.rights, operation) != "allowed"]
    if denied:
        raise ValueError(f"{operation} permission is not allowed for: {', '.join(denied)}")


class CatalogueStore:
    def __init__(self, path: str | Path, *, read_only: bool = False):
        self.read_only = read_only
        if read_only:
            self.connection = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)
        else:
            self.connection = sqlite3.connect(path)
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS catalogue_snapshots "
                "(digest TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.close()

    def put(self, catalogue: Catalogue) -> str:
        if self.read_only:
            raise ValueError("cannot write to a read-only catalogue store")
        payload = canonical_json(catalogue)
        require_permission(Catalogue.model_validate_json(payload), "retain")
        digest = digest_for(payload)
        with self.connection:
            existing = self.connection.execute(
                "SELECT payload FROM catalogue_snapshots WHERE digest = ?", (digest,)
            ).fetchone()
            if existing and existing[0] != payload:
                raise ValueError("existing snapshot failed integrity check")
            self.connection.execute(
                "INSERT OR IGNORE INTO catalogue_snapshots VALUES (?, ?)", (digest, payload)
            )
        return digest

    def get(self, digest: str) -> Catalogue:
        row = self.connection.execute(
            "SELECT payload FROM catalogue_snapshots WHERE digest = ?", (digest,)
        ).fetchone()
        if row is None:
            raise KeyError(f"snapshot not found: {digest}")
        if digest_for(row[0]) != digest:
            raise ValueError("snapshot failed integrity check")
        return Catalogue.model_validate_json(row[0])
