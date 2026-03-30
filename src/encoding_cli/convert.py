from __future__ import annotations

import codecs
from pathlib import Path
from typing import BinaryIO

CHUNK_SIZE = 65536


class ConversionError(Exception):
    pass


def open_input(path: str | None) -> BinaryIO:
    import sys

    if not path or path == "-":
        return sys.stdin.buffer
    return Path(path).open("rb")


def open_output(path: str | None) -> BinaryIO:
    import sys

    if not path or path == "-":
        return sys.stdout.buffer
    return Path(path).open("wb")


def transcode_stream(
    src: BinaryIO,
    dst: BinaryIO,
    *,
    source_encoding: str,
    target_encoding: str,
    errors: str,
    chunk_size: int = CHUNK_SIZE,
) -> None:
    decoder = codecs.getincrementaldecoder(source_encoding)(errors=errors)
    encoder = codecs.getincrementalencoder(target_encoding)(errors=errors)

    while True:
        chunk = src.read(chunk_size)
        if not chunk:
            break

        text = decoder.decode(chunk, final=False)
        if text:
            dst.write(encoder.encode(text, final=False))

    tail = decoder.decode(b"", final=True)
    if tail:
        dst.write(encoder.encode(tail, final=False))
    dst.write(encoder.encode("", final=True))


def transcode_bytes(
    data: bytes,
    *,
    source_encoding: str,
    target_encoding: str,
    errors: str,
) -> bytes:
    text = data.decode(source_encoding, errors=errors)
    return text.encode(target_encoding, errors=errors)


def to_utf8_bytes(data: bytes, *, errors: str) -> bytes:
    return transcode_bytes(
        data,
        source_encoding="gb18030",
        target_encoding="utf-8",
        errors=errors,
    )


def to_gbk_bytes(data: bytes, *, errors: str) -> bytes:
    return transcode_bytes(
        data,
        source_encoding="utf-8",
        target_encoding="gb18030",
        errors=errors,
    )


def convert_file(
    *,
    input_path: str | None,
    output_path: str | None,
    source_encoding: str,
    target_encoding: str,
    errors: str,
    chunk_size: int = CHUNK_SIZE,
) -> None:
    import sys

    src: BinaryIO | None = None
    dst: BinaryIO | None = None
    try:
        src = open_input(input_path)
        dst = open_output(output_path)
        transcode_stream(
            src,
            dst,
            source_encoding=source_encoding,
            target_encoding=target_encoding,
            errors=errors,
            chunk_size=chunk_size,
        )
        if dst is not sys.stdout.buffer:
            dst.flush()
    except (UnicodeError, LookupError) as exc:
        raise ConversionError(str(exc)) from exc
    finally:
        if src is not None and src is not sys.stdin.buffer:
            src.close()
        if dst is not None and dst is not sys.stdout.buffer:
            dst.close()
