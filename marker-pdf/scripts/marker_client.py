#!/usr/bin/env python3
"""
Marker PDF Skill - Python client for self-hosted Marker API.

Config is read from (in order of precedence):
    1. Explicit function/CLI arguments
    2. Real environment variables (MARKER_API_URL, MARKER_API_KEY)
    3. A .env file next to this script's skill directory

Using .env avoids relying on the shell having sourced ~/.bashrc —
non-interactive shells (the kind agents typically run commands in)
do not source ~/.bashrc by default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

DEFAULT_TIMEOUT = 300


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: {name}. "
            "Set it in your shell or .env file."
        )
    return value


def parse_document(
    file_path: str | Path,
    output_format: str = "markdown",
    force_ocr: bool = False,
    disable_ocr: bool = False,
    paginate_output: bool = False,
    page_range: str | None = None,
    api_url: str | None = None,
    api_key: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    Parse a document (PDF, image, DOCX, PPTX, XLSX, EPUB, HTML) using the
    self-hosted Marker API and return the structured result.

    Args:
        file_path: Path to the file to convert.
        output_format: One of 'markdown', 'json', 'html', 'chunks'.
        force_ocr: Force OCR on all pages.
        disable_ocr: Pure text-layer extraction, no VLM/OCR at all (fastest,
            no inference server needed). Best for born-digital PDFs.
            Mutually exclusive with force_ocr.
        paginate_output: Insert page separators in the output.
        page_range: Comma-separated page range, e.g. '0,5-10,20'.
        api_url: Marker API URL (defaults to MARKER_API_URL env var).
        api_key: API key (defaults to MARKER_API_KEY env var).
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response from the API.
    """
    if force_ocr and disable_ocr:
        raise ValueError("force_ocr and disable_ocr are mutually exclusive.")

    url = (api_url or _require_env("MARKER_API_URL")).rstrip("/") + "/marker/upload"
    key = api_key or os.getenv("MARKER_API_KEY", "")

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    mime_types = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".epub": "application/epub+zip",
        ".html": "text/html",
    }
    mime_type = mime_types.get(file_path.suffix.lower(), "application/octet-stream")

    data = {
        "output_format": output_format,
        "force_ocr": str(force_ocr).lower(),
        "disable_ocr": str(disable_ocr).lower(),
        "paginate_output": str(paginate_output).lower(),
    }
    if page_range:
        data["page_range"] = page_range

    headers = {"X-API-Key": key} if key else {}

    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime_type)}
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,
            timeout=timeout,
        )

    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a document to Markdown/JSON/HTML using Marker API."
    )
    parser.add_argument("file", help="Path to the document")
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "json", "html", "chunks"],
        help="Output format",
    )
    parser.add_argument(
        "--force-ocr",
        action="store_true",
        help="Force OCR on all pages",
    )
    parser.add_argument(
        "--disable-ocr",
        action="store_true",
        help="Pure text-layer extraction, no VLM/OCR at all (no inference "
        "server needed). Use for born-digital PDFs. Mutually exclusive "
        "with --force-ocr.",
    )
    parser.add_argument(
        "--paginate",
        action="store_true",
        help="Paginate output",
    )
    parser.add_argument(
        "--page-range",
        default=None,
        help="Page range, e.g. 0,5-10,20",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )

    args = parser.parse_args()

    try:
        result = parse_document(
            file_path=args.file,
            output_format=args.format,
            force_ocr=args.force_ocr,
            disable_ocr=args.disable_ocr,
            paginate_output=args.paginate,
            page_range=args.page_range,
            timeout=args.timeout,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
