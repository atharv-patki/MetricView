# config/style_config.py

ALERT_COLORS = {
    "success": "#28a745",  # Green
    "warning": "#ffc107",  # Yellow
    "danger":  "#dc3545",  # Red
    "neutral": "#6c757d"   # Grey
}

GAUGE_THRESHOLDS = {
    "RSI": {"min": 0, "max": 100},
    "Productivity": {"min": 0, "max": 100},
    "Attendance": {"min": 0, "max": 100},
    "Conversion Rate (%)": {"min": 0, "max": 100},
}
