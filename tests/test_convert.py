from __future__ import annotations

from encoding_cli.convert import to_gbk_bytes, to_utf8_bytes


def test_utf8_to_gbk_roundtrip_bytes() -> None:
    text = "中文ABC€𠮷"
    utf8_bytes = text.encode("utf-8")
    gbk_bytes = to_gbk_bytes(utf8_bytes, errors="strict")
    assert to_utf8_bytes(gbk_bytes, errors="strict") == utf8_bytes


def test_invalid_utf8_raises() -> None:
    invalid = b"\xff\xfe\xfd"
    try:
        to_gbk_bytes(invalid, errors="strict")
    except UnicodeError:
        return
    raise AssertionError("expected UnicodeError")
