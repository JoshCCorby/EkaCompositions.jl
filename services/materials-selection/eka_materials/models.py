"""Versioned evidence records. Validation is not engineering qualification."""

from datetime import date
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat, HttpUrl, model_validator

from .units import normalize


Text = Annotated[str, Field(min_length=1, max_length=4000)]
Id = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_.:-]{0,127}$")]
Unit = Annotated[str, Field(min_length=1, max_length=80)]
NonNegative = Annotated[FiniteFloat, Field(ge=0)]
Property = Literal[
    "density", "tensile_yield_strength", "tensile_modulus",
    "thermal_conductivity", "service_temperature", "volume_resistivity",
]
KnownBasis = Literal["typical", "guideline", "specified_limit", "measured"]
Basis = KnownBasis | Literal["not_stated"]
Permission = Literal["allowed", "unknown", "prohibited"]


class Record(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True, frozen=True, str_strip_whitespace=True,
        validate_default=True, revalidate_instances="always",
    )


class NumericValue(Record):
    kind: Literal["point", "range", "lower_bound", "upper_bound", "missing"]
    lower: FiniteFloat | None = None
    upper: FiniteFloat | None = None
    missing_reason: Text | None = None

    @model_validator(mode="after")
    def validate_shape(self) -> Self:
        if self.kind == "missing":
            if self.lower is not None or self.upper is not None or not self.missing_reason:
                raise ValueError("missing values need a reason and no numeric bounds")
            return self
        if self.missing_reason is not None:
            raise ValueError("only missing values may carry a missing_reason")
        if self.kind in ("point", "range"):
            if self.lower is None or self.upper is None or self.lower > self.upper:
                raise ValueError("point/range needs ordered lower and upper bounds")
            if self.kind == "point" and self.lower != self.upper:
                raise ValueError("point bounds must be identical")
        elif self.kind == "lower_bound":
            if self.lower is None or self.upper is not None:
                raise ValueError("lower_bound needs only a lower value")
        elif self.lower is not None or self.upper is None:
            raise ValueError("upper_bound needs only an upper value")
        return self

    def normalized(self, unit: str, property_name: str) -> Self:
        return type(self)(
            kind=self.kind,
            lower=None if self.lower is None else normalize(self.lower, unit, property_name),
            upper=None if self.upper is None else normalize(self.upper, unit, property_name),
            missing_reason=self.missing_reason,
        )


class Conditions(Record):
    temperature_k: NonNegative | None = None
    humidity_percent: Annotated[FiniteFloat, Field(ge=0, le=100)] | None = None
    thickness_min_mm: NonNegative | None = None
    thickness_max_mm: NonNegative | None = None
    direction: Text | None = None
    duration: Text | None = None
    test_method: Text | None = None
    notes: Text | None = None

    @model_validator(mode="after")
    def ordered_thickness(self) -> Self:
        if (self.thickness_min_mm is not None and self.thickness_max_mm is not None
                and self.thickness_min_mm > self.thickness_max_mm):
            raise ValueError("thickness bounds are reversed")
        return self


class Rights(Record):
    retain: Permission = "unknown"
    display: Permission = "unknown"
    redistribute: Permission = "unknown"
    basis: Text
    checked_on: date


class Source(Record):
    id: Id
    title: Text
    url: HttpUrl
    kind: Literal["synthetic", "manufacturer", "user_provided"]
    revision: Text | None = None
    accessed_on: date
    sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] | None = None
    rights: Rights


class Family(Record):
    id: Id
    name: Text


class Grade(Record):
    id: Id
    family_id: Id
    manufacturer: Text
    designation: Text


class Variant(Record):
    id: Id
    grade_id: Id
    form: Text
    temper: Text | None = None
    process: Text | None = None


class Observation(Record):
    id: Id
    variant_id: Id
    property: Property
    value: NumericValue
    unit: Unit | None = None
    basis: Basis
    conditions: Conditions
    source_id: Id
    locator: Text

    @model_validator(mode="after")
    def valid_quantity(self) -> Self:
        if self.unit is None:
            if self.value.kind != "missing":
                raise ValueError("numeric observations require source units")
        elif self.value.kind == "missing":
            normalize(1, self.unit, self.property)
        else:
            self.value.normalized(self.unit, self.property)
        return self


class Origin(Record):
    kind: Literal["supplied", "assumption", "derived"]
    statement: Text
    derivation: Text | None = None

    @model_validator(mode="after")
    def explicit_derivation(self) -> Self:
        if self.kind == "derived" and self.derivation is None:
            raise ValueError("derived inputs require an inspectable derivation")
        if self.kind != "derived" and self.derivation is not None:
            raise ValueError("derivations belong only to derived inputs")
        return self


class Constraint(Record):
    id: Id
    property: Property
    operator: Literal[">=", "<="]
    threshold: FiniteFloat
    unit: Unit
    acceptable_basis: Annotated[tuple[KnownBasis, ...], Field(min_length=1)]
    conditions: Conditions
    origin: Origin

    @model_validator(mode="after")
    def valid_threshold(self) -> Self:
        normalize(self.threshold, self.unit, self.property)
        return self


class Preference(Record):
    property: Property
    direction: Literal["minimize", "maximize"]
    origin: Origin


class Task(Record):
    id: Id
    revision: Text
    brief: Text
    constraints: tuple[Constraint, ...] = ()
    preferences: tuple[Preference, ...] = ()
    open_questions: tuple[Text, ...] = ()

    @model_validator(mode="after")
    def unique_constraints(self) -> Self:
        ids = [item.id for item in self.constraints]
        if len(ids) != len(set(ids)):
            raise ValueError("constraint IDs must be unique within a task")
        return self


class Offer(Record):
    id: Id
    variant_id: Id
    supplier: Text
    product_url: HttpUrl
    source_id: Id
    locator: Text
    observed_on: date
    region: Text | None = None
    quantity_basis: Text | None = None
    availability: Literal["unknown", "listed_available", "listed_unavailable"] = "unknown"


class Catalogue(Record):
    schema_version: Annotated[int, Field(ge=1, le=1)] = 1
    label: Text
    families: tuple[Family, ...]
    grades: tuple[Grade, ...]
    variants: tuple[Variant, ...]
    sources: tuple[Source, ...]
    observations: tuple[Observation, ...]
    tasks: tuple[Task, ...] = ()
    offers: tuple[Offer, ...] = ()

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        collections = {
            name: getattr(self, name) for name in
            ("families", "grades", "variants", "sources", "observations", "tasks", "offers")
        }
        all_ids = [record.id for records in collections.values() for record in records]
        if len(all_ids) != len(set(all_ids)):
            raise ValueError("record IDs must be unique across the catalogue")
        ids = {name: {item.id for item in items} for name, items in collections.items()}

        def require(record: Record, field: str, target: str) -> None:
            if getattr(record, field) not in ids[target]:
                raise ValueError(f"{record.id}: unresolved {field}")

        for grade in self.grades:
            require(grade, "family_id", "families")
        for variant in self.variants:
            require(variant, "grade_id", "grades")
        for record in (*self.observations, *self.offers):
            require(record, "variant_id", "variants")
            require(record, "source_id", "sources")
        return self
