from enum import Enum


class DataExtensions(Enum):
    """Enum to distinguish data files by extension, used instead of hardcoding extension strings."""

    gz = "jsonl.gz"
    txt = "txt.gz"
    zst = "jsonl.zst"
