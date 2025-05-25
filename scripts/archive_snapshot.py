
import datetime
import pathlib
import shutil
from aods.data_io.duck_store import DB_PATH

ARCHIVE_ROOT = pathlib.Path('archives')

def main() -> None:
    today = datetime.date.today().isoformat()
    dest_dir = ARCHIVE_ROOT / today
    dest_dir.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        shutil.copy2(DB_PATH, dest_dir / DB_PATH.name)

if __name__ == '__main__':

    main()
