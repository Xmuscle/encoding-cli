from __future__ import annotations

from encoding_cli.detect import classify_ambiguity, is_gbk_bytes, is_utf8_bytes


def test_ascii_is_ambiguous() -> None:
    data = b"hello"
    assert is_utf8_bytes(data).matched is True
    assert is_gbk_bytes(data).matched is True
    assert classify_ambiguity(data) is not None


def test_invalid_utf8_detection() -> None:
    data = "中文".encode("gb18030")
    assert is_utf8_bytes(data).matched is False
    assert is_gbk_bytes(data).matched is True
