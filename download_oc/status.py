from enum import Enum


class Status(Enum):
    EXISTS = 0
    DOWNLOAD_SUCCESS = 1
    DOWNLOAD_FAILED = 2
    VALIDATION_FAILED = 3
