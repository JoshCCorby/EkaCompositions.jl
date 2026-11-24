"""Compare positive, multiplicative material indices after manual screening."""

from itertools import combinations
import math
from typing import Annotated, Literal, Self

from pydantic import Field, FiniteFloat, model_validator

from .models import Basis, NumericValue, Property, Record, Text, Unit
from .units import CANONICAL_UNITS, normalize


class IndexEvidence(Record):
    property: Property
    value: NumericValue
    unit: Unit | None = None
    basis: Basis
    source: Text
    conditions: Text
    applicability: Literal["applicable", "inapplicable", "unknown"]

    @model_validator(mode="after")
    def check_quantity(self) -> Self:
        if self.value.kind == "missing":
            if self.unit is not None:
                normalize(1, self.unit, self.property)
        elif self.unit is None:
            raise ValueError("numeric evidence requires a unit")
        else:
            self.value.normalized(self.unit, self.property)
        return self


class ScreenedCandidate(Record):
    name: Text
    screen: Literal["pass", "fail", "unknown", "conflict"]
    screen_reason: Text
    evidence: tuple[IndexEvidence, ...] = ()


class IndexWorksheet(Record):
    title: Text
    objective: Text
    derivation: Text
    direction: Literal["maximize", "minimize"]
    powers: Annotated[dict[Property, FiniteFloat], Field(min_length=1)]
    candidates: Annotated[tuple[ScreenedCandidate, ...], Field(min_length=1)]

    @model_validator(mode="after")
    def check_index(self) -> Self:
        if any(p == 0 for p in self.powers.values()):
            raise ValueError("omit properties with a zero exponent")
        names = [candidate.name for candidate in self.candidates]
        if len(names) != len(set(names)):
            raise ValueError("candidate names must be unique")
        return self


def index_interval(
    candidate: ScreenedCandidate, powers: dict[Property, float],
) -> tuple[tuple[float, float] | None, str | None]:
    """Return an index enclosure or a reason to withhold comparison."""
    if candidate.screen != "pass":
        return None, f"manual screen {candidate.screen}: {candidate.screen_reason}"
    low = high = 1.0
    for prop, exponent in sorted(powers.items()):
        rows = [row for row in candidate.evidence if row.property == prop
                and row.applicability != "inapplicable"]
        if len(rows) > 1:
            return None, f"{prop}: multiple evidence rows need review"
        if not rows or rows[0].applicability == "unknown":
            return None, f"{prop}: missing applicable evidence"
        row = rows[0]
        if row.value.kind == "missing":
            return None, f"{prop}: {row.value.missing_reason}"
        value = row.value.normalized(row.unit, prop)
        if value.lower is None or value.upper is None or value.lower <= 0:
            return None, f"{prop}: a positive point or closed range is needed"
        a, b = value.lower, value.upper
        if exponent < 0:
            a, b = b, a
        try:
            low *= a ** exponent
            high *= b ** exponent
        except OverflowError:
            return None, "index outside numeric range"
        if low <= 0 or not math.isfinite(high):
            return None, "index outside numeric range"
    return (low, high), None


def compare_index(sheet: IndexWorksheet) -> dict:
    rows = []
    intervals = {}
    for candidate in sorted(sheet.candidates, key=lambda item: item.name):
        bounds, reason = index_interval(candidate, sheet.powers)
        rows.append({
            **candidate.model_dump(mode="json"), "index_bounds": bounds, "reason": reason,
        })
        if bounds is not None:
            intervals[candidate.name] = bounds

    pairs = []
    for a, b in combinations(intervals, 2):
        a_lo, a_hi = intervals[a]
        b_lo, b_hi = intervals[b]
        preferred = None
        # Touching endpoints and conversion roundoff do not establish separation.
        if a_lo > b_hi and not math.isclose(a_lo, b_hi, rel_tol=1e-12):
            preferred = a if sheet.direction == "maximize" else b
        elif b_lo > a_hi and not math.isclose(b_lo, a_hi, rel_tol=1e-12):
            preferred = b if sheet.direction == "maximize" else a
        pairs.append({"a": a, "b": b, "preferred_on_index": preferred})
    return {
        **sheet.model_dump(mode="json", exclude={"candidates"}),
        "property_units": {p: CANONICAL_UNITS[p] for p in sheet.powers},
        "candidates": rows, "comparisons": pairs,
    }


def format_comparison(result: dict) -> str:
    formula = " × ".join(f"({prop} [{result['property_units'][prop]}])^{power:g}"
                         for prop, power in sorted(result["powers"].items()))
    lines = [result["title"], result["objective"], result["derivation"],
             f"{result['direction'].capitalize()} {formula}", "", "Candidate index ranges"]
    for row in result["candidates"]:
        bounds = row["index_bounds"]
        detail = row["reason"] if bounds is None else f"[{bounds[0]:.12g}, {bounds[1]:.12g}]"
        lines.append(f"  {row['name']}  {detail}")
    lines.extend(["", "Pairwise comparison on this index"])
    if not result["comparisons"]:
        lines.append("  Fewer than two candidates have comparable ranges.")
    for pair in result["comparisons"]:
        preferred = pair["preferred_on_index"]
        detail = f"favours {preferred}" if preferred else "ranges overlap, touch or tie within tolerance"
        lines.append(f"  {pair['a']} / {pair['b']}  {detail}")
    return "\n".join(lines)
