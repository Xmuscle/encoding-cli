from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .convert import CHUNK_SIZE, ConversionError, convert_file
from .detect import is_gbk_bytes, is_utf8_bytes
from .verify import verify_roundtrip


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="encoding-cli",
        description="Convert between pseudo-GB2312/GB18030 byte streams and UTF-8.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help="streaming chunk size in bytes (default: %(default)s)",
    )
    parser.add_argument(
        "--errors",
        choices=["strict", "ignore", "replace", "surrogateescape"],
        default="surrogateescape",
        help="codec error strategy (default: %(default)s)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    to_utf8 = subparsers.add_parser(
        "to_utf8",
        help="decode pseudo-GB2312 bytes with GB18030 and emit UTF-8 bytes",
    )
    to_utf8.add_argument("-i", "--input", help="input file, or - for stdin")
    to_utf8.add_argument("-o", "--output", help="output file, or - for stdout")

    to_gbk = subparsers.add_parser(
        "to_gbk",
        help="decode UTF-8 bytes and emit GB18030 bytes as pseudo-GB2312",
    )
    to_gbk.add_argument("-i", "--input", help="input file, or - for stdin")
    to_gbk.add_argument("-o", "--output", help="output file, or - for stdout")

    verify = subparsers.add_parser(
        "verify",
        help="validate GB18030 -> UTF-8 -> GB18030 roundtrip for one input",
    )
    verify.add_argument("-i", "--input", help="input file, or - for stdin")

    is_utf8 = subparsers.add_parser(
        "is_utf8",
        help="check whether input bytes decode as utf-8",
    )
    is_utf8.add_argument("-i", "--input", help="input file, or - for stdin")

    is_gbk = subparsers.add_parser(
        "is_gbk",
        help="check whether input bytes decode as gb18030",
    )
    is_gbk.add_argument("-i", "--input", help="input file, or - for stdin")

    return parser


def _read_input_bytes(path: str | None) -> bytes:
    if not path or path == "-":
        return sys.stdin.buffer.read()
    return Path(path).read_bytes()


def _print_detection(result: bool, reason: str) -> int:
    print("true" if result else "false")
    if reason:
        print(reason, file=sys.stderr)
    return 0 if result else 1


def _run_conversion(command: str, args: argparse.Namespace) -> int:
    source_encoding = "gb18030" if command == "to_utf8" else "utf-8"
    target_encoding = "utf-8" if command == "to_utf8" else "gb18030"

    try:
        convert_file(
            input_path=args.input,
            output_path=args.output,
            source_encoding=source_encoding,
            target_encoding=target_encoding,
            errors=args.errors,
            chunk_size=args.chunk_size,
        )
        return 0
    except ConversionError as exc:
        print(f"encoding conversion failed: {exc}", file=sys.stderr)
        return 1


def _run_verify(args: argparse.Namespace) -> int:
    data = _read_input_bytes(args.input)
    result = verify_roundtrip(data, errors=args.errors)

    print(f"passed={str(result.passed).lower()}")
    print(f"is_utf8={str(result.is_utf8).lower()}")
    print(f"is_gbk={str(result.is_gbk).lower()}")
    print(f"reason={result.reason}")
    if result.ambiguity:
        print(f"ambiguity={result.ambiguity}")

    return 0 if result.passed else 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.chunk_size <= 0:
        parser.error("--chunk-size must be a positive integer")

    if args.command in {"to_utf8", "to_gbk"}:
        return _run_conversion(args.command, args)

    if args.command == "verify":
        return _run_verify(args)

    data = _read_input_bytes(args.input)
    if args.command == "is_utf8":
        result = is_utf8_bytes(data)
        return _print_detection(result.matched, result.reason)

    if args.command == "is_gbk":
        result = is_gbk_bytes(data)
        return _print_detection(result.matched, result.reason)

    parser.error(f"unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
