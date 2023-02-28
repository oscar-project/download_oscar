from enum import Enum


class ChecksumExtensions(Enum):
    """Enum to distinguish checksum files by extension, used instead of hardcoding extension strings."""

    sha_txt = "sha256.txt"
    checksum_sha = "checksum.sha256"
