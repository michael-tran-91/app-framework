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

def fetch(path: str, encoding = None):
    """Fetch a file using pseudo-URL schemes:

    - app://path/to/file  -> read from the application bundle directory (`bundle_dir`)
    - local://path/to/file -> read from the user application data directory (`app_data_dir`)
    - otherwise -> treat as a filesystem path; relative paths are resolved against `bundle_dir` if available

    Returns bytes by default.
    """
    if not path:
        raise ValueError('empty path')

    # Determine target Path
    if path.startswith('app://'):
        rel = path[len('app://'):].lstrip('/')
        base = bundle_dir or Path(__file__).resolve().parent.parent
        target = base.joinpath(rel)
    elif path.startswith('local://'):
        rel = path[len('local://'):].lstrip('/')
        target = app_data_dir.joinpath(rel)
    else:
        p = Path(path)
        if not p.is_absolute():
            base = bundle_dir or Path(__file__).resolve().parent.parent
            target = base.joinpath(path)
        else:
            target = p

    if not target.exists():
        raise FileNotFoundError(f'File not found: {target}')

    # Return bytes by default; callers can decode if they need text
    if encoding:
        return target.read_text(encoding)
    
    return target.read_bytes()