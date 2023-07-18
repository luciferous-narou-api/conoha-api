import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from typing import Type

from newrelic.api.log import NewRelicContextFormatter


def custom_default(obj):
    if isinstance(obj, Decimal):
        return num if obj == (num := int(obj)) else float(obj)
    if is_dataclass(obj):
        if isinstance(obj, Type):
            return str(obj)
        else:
            return asdict(obj)
    try:
        return {"type": str(type(obj)), "value": str(obj)}
    except Exception as e:
        return {"type": str(type(obj)), "error": {"type": str(type(e)), "msg": str(e)}}


class MyNewRelicContextFormatter(NewRelicContextFormatter):
    def format(self, record):
        return json.dumps(
            self.log_record_to_dict(record),
            default=custom_default,
            separators=(",", ":"),
        )
