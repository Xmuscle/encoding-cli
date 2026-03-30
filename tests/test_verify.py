from __future__ import annotations

from encoding_cli.verify import verify_roundtrip


def test_verify_roundtrip_success() -> None:
    data = "中文ABC€𠮷".encode("gb18030")
    result = verify_roundtrip(data, errors="strict")
    assert result.passed is True
    assert result.reason == "ok"


def test_verify_roundtrip_failure() -> None:
    data = b"\x81"
    result = verify_roundtrip(data, errors="strict")
    assert result.passed is False
    assert result.reason.startswith("unicode-error:")
