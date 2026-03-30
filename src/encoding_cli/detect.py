from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionResult:
    matched: bool
    encoding: str
    reason: str


def _can_decode(data: bytes, encoding: str, *, errors: str = "strict") -> bool:
    try:
        data.decode(encoding, errors=errors)
        return True
    except UnicodeError:
        return False


def is_utf8_bytes(data: bytes) -> DetectionResult:
    matched = _can_decode(data, "utf-8")
    if matched:
        return DetectionResult(True, "utf-8", "input decodes as utf-8")
    return DetectionResult(False, "utf-8", "input does not decode as utf-8")


def is_gbk_bytes(data: bytes) -> DetectionResult:
    matched = _can_decode(data, "gb18030")
    if matched:
        return DetectionResult(True, "gb18030", "input decodes as gb18030")
    return DetectionResult(False, "gb18030", "input does not decode as gb18030")


def classify_ambiguity(data: bytes) -> str | None:
    utf8 = _can_decode(data, "utf-8")
    gbk = _can_decode(data, "gb18030")
    if utf8 and gbk:
        return "ambiguous: input is valid as both utf-8 and gb18030"
    return None
