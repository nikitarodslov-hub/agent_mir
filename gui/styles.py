"""Dark theme colour constants and Qt stylesheet strings."""


class Colors:
    BG = "#1a1a2e"
    PANEL = "#16213e"
    ACCENT_GREEN = "#4ecca3"
    ACCENT_BLUE = "#0f3460"
    ACCENT_BLUE_HOVER = "#1a4a80"
    TEXT = "#e0e0e0"
    TEXT_DIM = "#7777aa"
    BORDER = "#2a2a4a"
    BTN_SEND = "#2d8a5e"
    BTN_SEND_HOVER = "#3aad78"
    BTN_SEND_PRESSED = "#1f6644"


STYLES: dict[str, str] = {
    "window": f"background-color: {Colors.BG};",

    "root": f"""
        QWidget#root {{
            background-color: {Colors.BG};
            color: {Colors.TEXT};
        }}
    """,

    "title_bar": f"""
        QFrame {{
            background-color: {Colors.PANEL};
            border-radius: 6px;
        }}
    """,

    "title_text": f"""
        color: {Colors.ACCENT_GREEN};
        font-weight: bold;
        font-size: 13px;
        font-family: 'Segoe UI', Arial, sans-serif;
    """,

    "close_btn": f"""
        QPushButton {{
            background-color: {Colors.ACCENT_BLUE};
            color: {Colors.TEXT};
            border-radius: 11px;
            border: none;
            font-size: 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{ background-color: #cc4444; }}
    """,

    "status": f"""
        color: {Colors.ACCENT_GREEN};
        font-size: 11px;
        padding: 2px 2px;
        font-family: monospace;
    """,

    "client_frame": f"""
        QFrame {{
            background-color: {Colors.ACCENT_BLUE};
            border-radius: 5px;
        }}
    """,

    "client_name": f"""
        color: {Colors.TEXT};
        font-weight: bold;
        font-size: 12px;
    """,

    "meta_dim": f"""
        color: {Colors.TEXT_DIM};
        font-size: 10px;
    """,

    "meta_accent": f"""
        color: {Colors.ACCENT_GREEN};
        font-size: 10px;
    """,

    "section_header": f"""
        color: {Colors.TEXT_DIM};
        font-size: 9px;
        font-weight: bold;
        letter-spacing: 1px;
    """,

    "message_box": f"""
        QTextEdit {{
            background-color: {Colors.PANEL};
            color: {Colors.TEXT};
            border: 1px solid {Colors.BORDER};
            border-radius: 4px;
            padding: 5px;
            font-size: 11px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
    """,

    "response_box": f"""
        QTextEdit {{
            background-color: {Colors.PANEL};
            color: {Colors.TEXT};
            border: 1px solid {Colors.ACCENT_GREEN};
            border-radius: 4px;
            padding: 5px;
            font-size: 11px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QTextEdit:focus {{
            border: 1px solid #6effd8;
        }}
    """,

    "btn_send": f"""
        QPushButton {{
            background-color: {Colors.BTN_SEND};
            color: white;
            font-weight: bold;
            font-size: 12px;
            border-radius: 5px;
            padding: 6px 14px;
            border: none;
        }}
        QPushButton:hover {{ background-color: {Colors.BTN_SEND_HOVER}; }}
        QPushButton:pressed {{ background-color: {Colors.BTN_SEND_PRESSED}; }}
        QPushButton:disabled {{ background-color: #334433; color: #666; }}
    """,

    "btn_skip": f"""
        QPushButton {{
            background-color: {Colors.ACCENT_BLUE};
            color: {Colors.TEXT_DIM};
            font-size: 11px;
            border-radius: 5px;
            padding: 6px 12px;
            border: 1px solid {Colors.BORDER};
        }}
        QPushButton:hover {{
            background-color: {Colors.ACCENT_BLUE_HOVER};
            color: {Colors.TEXT};
        }}
        QPushButton:disabled {{ color: #444; }}
    """,

    "counter": f"""
        color: {Colors.TEXT_DIM};
        font-size: 9px;
    """,

    "idle": f"""
        color: {Colors.TEXT_DIM};
        font-size: 10px;
        padding: 4px 0;
    """,
}
