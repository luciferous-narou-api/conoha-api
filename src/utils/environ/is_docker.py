import os


def is_docker() -> bool:
    return os.getenv("IN_CONTAINER") == "true"
