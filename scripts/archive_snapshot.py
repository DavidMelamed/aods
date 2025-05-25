"""Copy current DuckDB to archives."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

DB = Path("data/aods.duckdb")
ARCHIVE_DIR = Path("archives")


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    target = ARCHIVE_DIR / f"{ts}.duckdb"
    if DB.exists():
        shutil.copy2(DB, target)


if __name__ == "__main__":
    main()
