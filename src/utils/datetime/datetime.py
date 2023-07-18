from datetime import datetime, timedelta, timezone


def get_jst_timezone() -> timezone:
    return timezone(timedelta(hours=+9), "JST")


def now() -> datetime:
    return datetime.now(get_jst_timezone())
