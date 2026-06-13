#!/usr/bin/env python3
"""Simple cross-platform PyInstaller build helper.

Usage:
  python build.py        # create a one-folder build (dist/framework)
  python build.py --onefile  # create a single-file executable

This script uses PyInstaller's programmatic API and can include only
specified PySide6 plugin subfolders to reduce the application footprint.
"""
import os
import sys
import argparse

try:
    from PyInstaller.__main__ import run
except Exception:
    print("PyInstaller is not installed. Install it with: pip install pyinstaller")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='PyInstaller build helper')
    parser.add_argument('--onefile', action='store_true', help='Create a single-file executable')
    parser.add_argument(
        '--pyside-plugins',
        default='platforms',
        help='Comma-separated PySide6 plugin subfolders to include (default: platforms). Use "all" to fall back to --collect-all PySide6.'
    )
    args_ns = parser.parse_args()

    app_name = "framework"
    onefile = args_ns.onefile
    pyside_plugins_opt = args_ns.pyside_plugins

    base_dir = os.path.abspath(os.path.dirname(__file__))
    res_dir = os.path.join(base_dir, 'res')
    add_data = f"{res_dir}{os.pathsep}res" if os.path.exists(res_dir) else None

    pyi_args = [
        '--noconfirm',
        '--clean',
        f'--name={app_name}',
    ]

    pyi_args += ['--onefile'] if onefile else ['--onedir']

    if add_data:
        pyi_args.append(f'--add-data={add_data}')

    # Handle PySide6 packaging: default is to include only specified plugin folders
    # (e.g. 'platforms') to reduce footprint. Use --pyside-plugins=all to fall
    # back to --collect-all behavior.
    if pyside_plugins_opt.lower() == 'all':
        pyi_args += ['--collect-all', 'PySide6']
    else:
        try:
            import PySide6
            pyside_pkg_dir = os.path.dirname(PySide6.__file__)
            plugins_dir = os.path.join(pyside_pkg_dir, 'Qt', 'plugins')
            plugins = [p.strip() for p in pyside_plugins_opt.split(',') if p.strip()]
            for plugin in plugins:
                plugin_path = os.path.join(plugins_dir, plugin)
                if os.path.exists(plugin_path):
                    pyi_args.append(f'--add-data={plugin_path}{os.pathsep}PySide6/Qt/plugins/{plugin}')
                else:
                    print(f'Warning: PySide6 plugin folder not found: {plugin_path}')
        except Exception as e:
            print('Warning: could not import PySide6 at build time, falling back to --collect-all PySide6', e)
            pyi_args += ['--collect-all', 'PySide6']

    # Entry point
    pyi_args.append('main.py')

    print('Running PyInstaller with:', ' '.join(pyi_args))
    run(pyi_args)


if __name__ == '__main__':
    main()
