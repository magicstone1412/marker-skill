---
name: marker-pdf
description: "Parse PDFs, images, and documents (DOCX, PPTX, XLSX, EPUB, HTML) to Markdown, JSON, or HTML using a self-hosted Marker API. Use when the user asks to extract text, OCR, or convert a document to markdown."
---

# Marker PDF Skill

Convert PDFs, images, or office documents to Markdown/JSON/HTML using a self-hosted Marker API server.

## When to Use

- Parse a PDF to text / markdown
- OCR a scanned document
- Extract tables, equations, or structured text from a document
- Convert images, DOCX, PPTX, XLSX, EPUB, or HTML to markdown

## Prerequisites

A self-hosted Marker API must be running (see the marker repo's `docker-compose.yml`). Config lives in `{baseDir}/.env`, not shell environment variables (non-interactive agent shells don't source `~/.bashrc`, so exported vars don't persist between commands). Create it once during setup:

```bash
cp {baseDir}/.env.example {baseDir}/.env
```

Defaults to `MARKER_API_URL=http://localhost:8001` with no API key. Edit `{baseDir}/.env` directly if your server URL differs or has auth enabled.

## Setup (once)

```bash
cd {baseDir}
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## How to Use

Always call the client script through the skill's own venv interpreter — do not use system `python3`:

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/marker_client.py /path/to/file.pdf --format markdown
```

Options:

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/marker_client.py /path/to/file.pdf \
  --format markdown \
  --force-ocr \
  --paginate \
  --page-range 0,5-10,20 \
  --timeout 300
```

Output is printed to stdout as JSON:

```json
{
  "format": "markdown",
  "output": "# Extracted text...",
  "images": {},
  "metadata": {...},
  "success": true
}
```

Parse the `output` field for the converted content.

## Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--format` | string | `markdown` | `markdown`, `json`, `html`, `chunks` |
| `--force-ocr` | flag | off | Force OCR on all pages |
| `--paginate` | flag | off | Add page separators |
| `--page-range` | string | none | Page range, e.g. `0,5-10,20` |

## Error Handling

- If `MARKER_API_URL` is missing, the script raises immediately — tell the user to set it.
- If `MARKER_API_KEY` is required by the server but missing, the request returns 401 — check the server's auth setting.
- Non-2xx responses surface the server's error message; report it back to the user.
- Large files can take a while — the default timeout is 300s; raise `--timeout` for big scans.

## Security

- Never print or log `MARKER_API_KEY`.
- Prefer reading it from the environment rather than hardcoding it in commands.
