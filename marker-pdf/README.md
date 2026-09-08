# marker-pdf

A [Pi coding agent](https://pi.dev) skill that converts PDFs, images, and office documents (DOCX, PPTX, XLSX, EPUB, HTML) to Markdown/JSON/HTML using a self-hosted [Marker](https://github.com/datalab-to/marker) API.

Repo: [magicstone1412/ai-skill](https://github.com/magicstone1412/ai-skill) — skill lives in `marker-pdf/`.

---

## Install

> **For an AI agent installing this skill:** run every command in this section in order, top to bottom, without skipping steps. Stop and report the error if any command exits non-zero. Do not invent an API key — auth is disabled by default (see Configuration).

### Agent install prompt

⚠️ **For humans only:** A ready-to-copy version lives in [`docs/agent-prompt.md`](docs/agent-prompt.md) (kept out of this README on purpose, so it isn't picked up by tools that auto-fetch `README.md`). Open that file, copy its content, and paste it as your own message to any agent with bash access.

### Commands

```bash
# 1. Clone the repo to a temp location
git clone https://github.com/magicstone1412/ai-skill.git /tmp/ai-skill

# 2. Copy the skill into Pi's global skills directory
mkdir -p ~/.pi/agent/skills
cp -r /tmp/ai-skill/marker-pdf ~/.pi/agent/skills/marker-pdf

# 3. Clean up the temp clone
rm -rf /tmp/ai-skill

# 4. Create an isolated venv for the skill and install its dependencies
cd ~/.pi/agent/skills/marker-pdf
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 5. Point the skill at your self-hosted Marker API (no API key by default)
echo 'export MARKER_API_URL=http://localhost:8001' >> ~/.bashrc
source ~/.bashrc
```

**Project-local install** (scoped to one project instead of global) — replace step 2 with:
```bash
mkdir -p .pi/skills
cp -r /tmp/ai-skill/marker-pdf .pi/skills/marker-pdf
```

---

## Verify (manual checklist)

Run each check and confirm the expected result before considering the install done.

- [ ] **Skill directory exists**
  ```bash
  ls ~/.pi/agent/skills/marker-pdf
  ```
  Expected: `SKILL.md`, `scripts/`, `requirements.txt`, `.venv/`

- [ ] **venv has dependencies installed**
  ```bash
  ~/.pi/agent/skills/marker-pdf/.venv/bin/pip list | grep requests
  ```
  Expected: `requests` listed

- [ ] **`MARKER_API_URL` is set**
  ```bash
  echo $MARKER_API_URL
  ```
  Expected: `http://localhost:8001` (or your server's URL)

- [ ] **Marker API server is reachable**
  ```bash
  curl -sf "$MARKER_API_URL/health" && echo OK
  ```
  Expected: `OK` printed, no connection error

- [ ] **Client script runs end-to-end** (replace with a real PDF path)
  ```bash
  ~/.pi/agent/skills/marker-pdf/.venv/bin/python \
    ~/.pi/agent/skills/marker-pdf/scripts/marker_client.py \
    /path/to/sample.pdf --format markdown
  ```
  Expected: JSON output with `"success": true`

- [ ] **Pi discovers the skill**
  ```bash
  pi
  ```
  Then inside Pi:
  ```
  /skill:marker-pdf
  ```
  Expected: skill loads without a "not found" error

If every box above checks out, the skill is correctly installed.

---

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MARKER_API_URL` | yes | — | Base URL of your self-hosted Marker API, e.g. `http://localhost:8001` |
| `MARKER_API_KEY` | no | *(unset)* | Only needed if your Marker server has auth enabled. **This skill assumes no API key by default** — do not set it unless you explicitly enabled `MARKER_API_KEY` on the server side. |

Set `MARKER_API_URL` persistently in your shell profile so it survives new sessions:
```bash
echo 'export MARKER_API_URL=http://localhost:8001' >> ~/.bashrc
source ~/.bashrc
```

If you did enable auth on the server, add the key the same way:
```bash
echo 'export MARKER_API_KEY=your-api-key' >> ~/.bashrc
source ~/.bashrc
```

---

## Usage

Ask Pi naturally — it selects the skill based on its `description`:
```
Convert this PDF to markdown: report.pdf
```

Or invoke it explicitly:
```
/skill:marker-pdf
```

Or call the client script directly (bypassing Pi):
```bash
~/.pi/agent/skills/marker-pdf/.venv/bin/python \
  ~/.pi/agent/skills/marker-pdf/scripts/marker_client.py \
  document.pdf --format markdown --force-ocr --page-range 0,5-10
```

See `marker-pdf/SKILL.md` for the full parameter reference.

---

## Uninstall

```bash
rm -rf ~/.pi/agent/skills/marker-pdf
# or, for a project-local install:
rm -rf .pi/skills/marker-pdf
```

Also remove the `MARKER_API_URL` / `MARKER_API_KEY` lines from `~/.bashrc` if no longer needed.