from __future__ import annotations

from dataclasses import dataclass

from .convert import to_gbk_bytes, to_utf8_bytes
from .detect import classify_ambiguity, is_gbk_bytes, is_utf8_bytes


@dataclass(frozen=True)
class VerifyResult:
    passed: bool
    is_utf8: bool
    is_gbk: bool
    reason: str
    ambiguity: str | None = None


def verify_roundtrip(data: bytes, *, errors: str) -> VerifyResult:
    utf8 = is_utf8_bytes(data)
    gbk = is_gbk_bytes(data)
    ambiguity = classify_ambiguity(data)

    try:
        utf8_bytes = to_utf8_bytes(data, errors=errors)
        roundtrip_bytes = to_gbk_bytes(utf8_bytes, errors=errors)
    except UnicodeError as exc:
        return VerifyResult(
            passed=False,
            is_utf8=utf8.matched,
            is_gbk=gbk.matched,
            reason=f"unicode-error: {exc}",
            ambiguity=ambiguity,
        )

    if roundtrip_bytes != data:
        return VerifyResult(
            passed=False,
            is_utf8=utf8.matched,
            is_gbk=gbk.matched,
            reason="roundtrip-bytes-differ",
            ambiguity=ambiguity,
        )

    return VerifyResult(
        passed=True,
        is_utf8=utf8.matched,
        is_gbk=gbk.matched,
        reason="ok",
        ambiguity=ambiguity,
    )
