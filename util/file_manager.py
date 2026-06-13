from platformdirs import user_data_dir
from pathlib import Path
import sys

APP_NAME = "MyApp"
APP_AUTHOR = "MyCompany"   # optional, used on Windows

app_data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
app_data_dir.mkdir(parents=True, exist_ok=True)

bundle_dir = None
if getattr(sys, "frozen", False):
    bundle_dir = Path(sys._MEIPASS).resolve()
else:
    argv0 = Path(sys.argv[0]) if sys.argv and sys.argv[0] else None
    try:
        bundle_dir = argv0.resolve().parent
    except Exception:
        pass

def _fetch_app(path: str):
    pass

def _fetch_bundle(path: str):
    pass

def fetch(path: str):
    pass