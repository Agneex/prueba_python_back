from datetime import UTC, datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now_formatted() -> str:
    return datetime.now(UTC).strftime(DATETIME_FORMAT)
