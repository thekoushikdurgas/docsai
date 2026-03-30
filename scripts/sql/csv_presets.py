"""Named CSV → table mappings for docs/backend/database/csv seed files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CsvPreset:
    """Relative to docs/backend/database/csv/."""

    csv_name: str
    table: str
    skip_leading_column: bool = False


# Contact360 / appointment360 billing reference data
PRESETS: dict[str, CsvPreset] = {
    "subscription_plans": CsvPreset(
        csv_name="subscription_plans.csv",
        table="subscription_plans",
        skip_leading_column=True,
    ),
    "subscription_plan_periods": CsvPreset(
        csv_name="subscription_plan_periods.csv",
        table="subscription_plan_periods",
        skip_leading_column=True,
    ),
    "addon_packages": CsvPreset(
        csv_name="addon_packages.csv",
        table="addon_packages",
        skip_leading_column=True,
    ),
    "user_profiles": CsvPreset(
        csv_name="user_profiles.csv",
        table="user_profiles",
        skip_leading_column=False,
    ),
}


def get_preset(name: str) -> CsvPreset:
    key = name.strip().lower().replace("-", "_")
    if key not in PRESETS:
        known = ", ".join(sorted(PRESETS))
        raise KeyError(f"Unknown preset {name!r}. Choose one of: {known}")
    return PRESETS[key]


def resolve_preset_csv(csv_dir: Path, preset: CsvPreset) -> Path:
    p = csv_dir / preset.csv_name
    if not p.is_file():
        raise FileNotFoundError(str(p))
    return p
