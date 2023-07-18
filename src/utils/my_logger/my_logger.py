from functools import wraps
from logging import DEBUG, ERROR, FATAL, INFO, WARNING, Logger, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from typing import Callable, Union
from uuid import uuid4

from src.utils.datetime import now

from .my_new_relic_context_formatter import MyNewRelicContextFormatter



class MyLogger:
    logger: Logger

    def __init__(self, name: str, level: int = DEBUG) -> None:
        handler = RotatingFileHandler(filename="/tmp/app.log", maxBytes=1024 * 50)
        handler.setFormatter(MyNewRelicContextFormatter())

        stm_handler = StreamHandler()
        stm_handler.setFormatter(MyNewRelicContextFormatter())

        self.logger = getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.logger.addHandler(stm_handler)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, exc_info=True, extra={"data": kwargs})

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, exc_info=True, extra={"data": kwargs})

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, exc_info=True, extra={"data": kwargs})

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, exc_info=True, extra={"data": kwargs})

    def fatal(self, msg: str, *args, **kwargs) -> None:
        self.logger.fatal(msg, *args, exc_info=True, extra={"data": kwargs})

    def logging_function(
        self,
        *,
        is_write: bool = True,
        with_args: bool = True,
        with_return: bool = False,
    ) -> Callable:
        def wrapper(func: Callable) -> Callable:
            @wraps(func)
            def process(*args, **kwargs):
                name_function = func.__name__
                id_function = str(uuid4())

                dt_before = now()
                options_start = {
                    "id": id_function,
                    "function_name": name_function,
                }
                if with_args:
                    options_start["args"] = args
                    options_start["kwargs"] = kwargs
                if is_write:
                    self.debug(
                        f"function {name_function} start ({id_function})",
                        **options_start,
                    )

                result = None
                error = None
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    error = e
                    raise
                finally:
                    delta = now() - dt_before
                    is_success = error is None
                    status = "success" if is_success else "failed"
                    options_end = {
                        "id": id_function,
                        "function_name": name_function,
                        "status": status,
                        "duration": delta,
                        "is_success": is_success,
                        "error": {
                            "type": str(type(error)),
                            "message": str(error),
                        },
                    }
                    if with_args:
                        options_end["args"] = args
                        options_end["kwargs"] = kwargs
                    if with_return:
                        options_end["return"] = result
                    if is_write or not is_success:
                        self.debug(
                            f"function {name_function} {status} ({id_function}) (Duration: {delta})",
                            **options_end,
                        )

            return process

        return wrapper
