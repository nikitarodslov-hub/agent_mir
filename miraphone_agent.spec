# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Miraphone Agent.

Build command:  pyinstaller miraphone_agent.spec --noconfirm
Or just run:    build_exe.bat

Output: dist/MiraphoneAgent/MiraphoneAgent.exe
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect playwright package data (includes the Node.js driver binary)
playwright_datas, playwright_binaries, playwright_hiddenimports = collect_all("playwright")

# Collect anthropic package
anthropic_datas, anthropic_binaries, anthropic_hiddenimports = collect_all("anthropic")

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=playwright_binaries + anthropic_binaries,
    datas=(
        playwright_datas
        + anthropic_datas
        + [
            # Ship the .env.example so the user can see what keys are expected
            (".env.example", "."),
        ]
    ),
    hiddenimports=(
        playwright_hiddenimports
        + anthropic_hiddenimports
        + collect_submodules("PyQt5")
        + [
            "PyQt5.sip",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "PyQt5.QtWidgets",
            "agent",
            "agent.orchestrator",
            "agent.bitrix_monitor",
            "agent.claude_ai",
            "agent.knowledge_base",
            "agent.moysklad_api",
            "gui",
            "gui.overlay",
            "gui.setup_dialog",
            "gui.styles",
            "utils",
            "utils.sound",
            "config",
        ]
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "unittest", "email", "xml", "pydoc"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MiraphoneAgent",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # No terminal window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon=None,              # Replace with "icon.ico" if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MiraphoneAgent",
)
