# Building with PyInstaller

Quick steps to create a distributable bundle using PyInstaller.

- Install dev requirements (recommended):

```bash
pip install -r requirements-dev.txt
```

- Build (one-folder):

```bash
python build.py
```

- Build (single executable):

```bash
python build.py --onefile
```

Output will be in the `dist/` directory (`dist/framework/` for onedir or `dist/framework.exe` for onefile on Windows).

Notes
- The `build.py` script uses `--collect-all PySide6` to include PySide6 package data and plugin files.
- The `res/` directory is automatically bundled (if present).
- If you run into missing Qt platform plugin errors at runtime, try building with a spec file and explicitly including PySide6 plugins, or inspect the `dist/` folder to ensure `platforms` is present.
