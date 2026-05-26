"""Premium cyberpunk dark-theme design system for Miraphone Agent."""


class Colors:
    # Deep-space backgrounds
    BG         = "#08081a"
    PANEL      = "#0c0c22"
    CARD       = "#10102e"
    INPUT_BG   = "#07070f"

    # Neon accents
    CYAN       = "#00e5ff"
    CYAN_DIM   = "#007799"
    VIOLET     = "#a855f7"
    VIOLET_DIM = "#7030c8"
    GREEN      = "#00e676"
    GREEN_DIM  = "#009944"
    GREEN_DARK = "#003a1e"
    ORANGE     = "#ff9f40"
    RED        = "#ff3b3b"
    YELLOW     = "#ffd020"
    PINK       = "#ff5fa0"
    BLUE       = "#3a82ff"

    # Typography
    TEXT       = "#dce6fa"
    TEXT_DIM   = "#4a5c82"
    TEXT_MUTED = "#1e2535"

    # Structure
    BORDER     = "#14143a"

    # Buttons
    BTN_SEND   = "#0a4f2f"
    BTN_SEND_H = "#136b3f"
    BTN_SEND_P = "#07361f"
    BTN_SKIP   = "#0c0c2a"
    BTN_SKIP_H = "#161640"


# Badge colours: question_type → (text_fg, bg)
BADGE_COLORS: dict[str, tuple[str, str]] = {
    "availability": ("#00e5ff", "#001828"),
    "warranty":     ("#a855f7", "#120828"),
    "installment":  ("#ffd020", "#181500"),
    "tradein":      ("#ff9f40", "#180f00"),
    "delivery":     ("#00e676", "#001a0c"),
    "payment":      ("#3a82ff", "#060e28"),
    "technical":    ("#ff5fa0", "#18000e"),
    "objection":    ("#ff3b3b", "#180000"),
    "return":       ("#ffd020", "#181500"),
    "greeting":     ("#00e5ff", "#001828"),
    "other":        ("#4a5c82", "#0c0e1e"),
}


def source_color(source: str) -> str:
    s = source.lower()
    if "авито"    in s: return "#97ccff"
    if "вконтакт" in s: return "#4a88c8"
    if "vk"       in s: return "#4a88c8"
    if "telegram" in s: return "#229ed9"
    if "whatsapp" in s: return "#25d366"
    if "wa"       in s: return "#25d366"
    if "instagram" in s: return "#e1306c"
    return Colors.CYAN


C = Colors

STYLES: dict[str, str] = {

    "window": f"background-color: {C.BG};",

    "root": f"""
        QWidget#root {{
            background-color: {C.BG};
            color: {C.TEXT};
        }}
    """,

    "title_bar": f"""
        QFrame {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0d0d28, stop:0.5 #111132, stop:1 #0d0d28
            );
            border-bottom: 1px solid #00e5ff20;
            min-height: 38px;
            max-height: 38px;
        }}
    """,

    "title_dot": f"""
        color: {C.CYAN};
        font-size: 10px;
    """,

    "title_text": f"""
        color: {C.CYAN};
        font-weight: bold;
        font-size: 10px;
        font-family: 'Consolas', 'Courier New', monospace;
        letter-spacing: 2px;
    """,

    "title_clock": f"""
        color: {C.TEXT_DIM};
        font-size: 9px;
        font-family: 'Consolas', 'Courier New', monospace;
        padding-right: 4px;
    """,

    "window_btn": f"""
        QPushButton {{
            background: transparent;
            color: {C.TEXT_DIM};
            border: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 11px;
        }}
        QPushButton:hover {{
            background-color: {C.BTN_SKIP_H};
            color: {C.TEXT};
        }}
    """,

    "close_btn": f"""
        QPushButton {{
            background: transparent;
            color: {C.TEXT_DIM};
            border: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 11px;
        }}
        QPushButton:hover {{
            background-color: {C.RED};
            color: white;
        }}
    """,

    "stats_bar": f"""
        QFrame {{
            background-color: {C.PANEL};
            border-bottom: 1px solid {C.BORDER};
        }}
    """,

    "stats_key": f"""
        color: {C.TEXT_MUTED};
        font-size: 8px;
        font-family: 'Consolas', monospace;
        letter-spacing: 1px;
    """,

    "stats_val": f"""
        color: {C.CYAN};
        font-size: 8px;
        font-weight: bold;
        font-family: 'Consolas', monospace;
    """,

    "stats_val_warn": f"""
        color: {C.ORANGE};
        font-size: 8px;
        font-weight: bold;
        font-family: 'Consolas', monospace;
    """,

    "status_frame": f"""
        QFrame {{
            background-color: {C.PANEL};
            border-bottom: 1px solid {C.BORDER};
        }}
    """,

    "status_text": f"""
        color: {C.TEXT_DIM};
        font-size: 10px;
        font-family: 'Consolas', monospace;
    """,

    "client_frame": f"""
        QFrame {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0e1535, stop:1 #09091e
            );
            border: 1px solid #00e5ff1a;
            border-left: 2px solid #00e5ff;
            border-radius: 5px;
        }}
    """,

    "client_name": f"""
        color: {C.TEXT};
        font-weight: bold;
        font-size: 12px;
        font-family: 'Segoe UI', Arial, sans-serif;
    """,

    "response_timer": f"""
        color: {C.ORANGE};
        font-size: 9px;
        font-family: 'Consolas', monospace;
    """,

    "response_timer_urgent": f"""
        color: {C.RED};
        font-size: 9px;
        font-weight: bold;
        font-family: 'Consolas', monospace;
    """,

    "section_header": f"""
        color: {C.TEXT_MUTED};
        font-size: 8px;
        font-weight: bold;
        letter-spacing: 2px;
        font-family: 'Consolas', monospace;
        padding-top: 2px;
    """,

    "message_box": f"""
        QTextEdit {{
            background-color: {C.INPUT_BG};
            color: {C.TEXT_DIM};
            border: 1px solid {C.BORDER};
            border-radius: 4px;
            padding: 6px 8px;
            font-size: 11px;
            font-family: 'Segoe UI', Arial, sans-serif;
            selection-background-color: #00e5ff25;
        }}
    """,

    "response_box": f"""
        QTextEdit {{
            background-color: {C.INPUT_BG};
            color: {C.TEXT};
            border: 1px solid #00e5ff25;
            border-radius: 4px;
            padding: 6px 8px;
            font-size: 11px;
            font-family: 'Segoe UI', Arial, sans-serif;
            selection-background-color: #00e5ff35;
        }}
        QTextEdit:focus {{
            border: 1px solid {C.CYAN};
        }}
    """,

    "btn_send": f"""
        QPushButton {{
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {C.BTN_SEND_H}, stop:1 {C.BTN_SEND}
            );
            color: {C.GREEN};
            font-weight: bold;
            font-size: 10px;
            letter-spacing: 2px;
            border-radius: 5px;
            border: 1px solid {C.GREEN_DIM};
            padding: 7px 14px;
        }}
        QPushButton:hover {{
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #1a8848, stop:1 {C.BTN_SEND_H}
            );
            color: white;
            border-color: {C.GREEN};
        }}
        QPushButton:pressed {{ background-color: {C.BTN_SEND_P}; }}
        QPushButton:disabled {{
            background-color: #060e08;
            color: {C.TEXT_MUTED};
            border-color: {C.BORDER};
        }}
    """,

    "btn_send_auto": f"""
        QPushButton {{
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #1a4a8f, stop:1 #0d2a5a
            );
            color: {C.CYAN};
            font-weight: bold;
            font-size: 10px;
            letter-spacing: 1px;
            border-radius: 5px;
            border: 1px solid {C.CYAN_DIM};
            padding: 7px 14px;
        }}
        QPushButton:hover {{
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #2255b0, stop:1 #1a4a8f
            );
        }}
    """,

    "btn_skip": f"""
        QPushButton {{
            background-color: {C.BTN_SKIP};
            color: {C.TEXT_DIM};
            font-size: 10px;
            letter-spacing: 1px;
            border-radius: 5px;
            border: 1px solid {C.BORDER};
            padding: 7px 12px;
        }}
        QPushButton:hover {{
            background-color: {C.BTN_SKIP_H};
            color: {C.TEXT};
            border-color: #303065;
        }}
        QPushButton:disabled {{ color: {C.TEXT_MUTED}; }}
    """,

    "btn_copy": f"""
        QPushButton {{
            background: transparent;
            color: {C.TEXT_DIM};
            font-size: 9px;
            border-radius: 4px;
            border: 1px solid {C.BORDER};
            padding: 5px 10px;
        }}
        QPushButton:hover {{
            background-color: {C.BTN_SKIP};
            color: {C.TEXT};
        }}
    """,

    "idle": f"""
        color: {C.TEXT_MUTED};
        font-size: 10px;
        font-family: 'Consolas', monospace;
        letter-spacing: 1px;
    """,

    "idle_dot": f"""
        color: {C.TEXT_MUTED};
        font-size: 20px;
    """,

    "footer": f"""
        QFrame {{
            background-color: {C.PANEL};
            border-top: 1px solid {C.BORDER};
        }}
    """,

    "shortcut_hints": f"""
        color: {C.TEXT_MUTED};
        font-size: 8px;
        font-family: 'Consolas', monospace;
        letter-spacing: 1px;
    """,
}
