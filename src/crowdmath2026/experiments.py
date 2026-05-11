import csv
import json
from fractions import Fraction
from pathlib import Path


def ensure_dir(path: Path) -> None:
    """Create directory and all parents if they do not already exist."""
    path.mkdir(parents=True, exist_ok=True)


def _fraction_default(obj: object) -> str:
    """JSON serialization helper: convert Fraction to string."""
    if isinstance(obj, Fraction):
        if obj.denominator == 1:
            return str(obj.numerator)
        return f"{obj.numerator}/{obj.denominator}"
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def write_json(path: Path, data: object) -> None:
    """Write data to a JSON file, converting Fraction values to strings."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=_fraction_default)


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    """Write a list of dicts to a CSV file using DictWriter."""
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_summary(path: Path, title: str, sections: list[str]) -> None:
    """Write a simple Markdown file with a title and a list of section strings."""
    lines = [f"# {title}", ""]
    for section in sections:
        lines.append(section)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
