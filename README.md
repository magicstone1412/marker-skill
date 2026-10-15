# marker-pdf

A [Pi coding agent](https://pi.dev) skill that converts PDFs, images, and office documents (DOCX, PPTX, XLSX, EPUB, HTML) to Markdown/JSON/HTML using a self-hosted [Marker](https://github.com/datalab-to/marker) API.

Repo: [magicstone1412/ai-skill](https://github.com/magicstone1412/ai-skill) — skill lives in `marker-pdf/`.

---

## Install

> **For an AI agent installing this skill:** run every command in this section in order, top to bottom, without skipping steps. Stop and report the error if any command exits non-zero. Do not invent an API key — auth is disabled by default (see Configuration).
>
> **Do not use `~/.bashrc` / `export` for config.** Agents typically run each command in a fresh non-interactive shell, which does not source `~/.bashrc` — a variable exported in one command will not exist in the next. This skill reads its config from a `.env` file instead, which works the same regardless of shell session.

### Agent install prompt

⚠️ **For humans only:** A ready-to-copy version lives in [`docs/installation-agent-prompt.md`](docs/installation-agent-prompt.md) (kept out of this README on purpose, so it isn't picked up by tools that auto-fetch `README.md`). Open that file, copy its content, and paste it as your own message to any agent with bash access.

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

# 5. Create the config file from the template (no API key by default)
cp .env.example .env
```

`.env` already defaults to `MARKER_API_URL=http://localhost:8001` with `MARKER_API_KEY` commented out (no auth). Only edit `.env` if your server runs on a different URL or has auth enabled — see Configuration.

**Project-local install** (scoped to one project instead of global) — replace step 2 with:
```bash
mkdir -p .pi/skills
cp -r /tmp/ai-skill/marker-pdf .pi/skills/marker-pdf
```

---

## Verify (manual checklist)

Run each check and confirm the expected result before considering the install done. Every command below is self-contained — none of them depend on shell state from a previous command, so they're safe to run in separate sessions.

- [ ] **Skill directory exists**
  ```bash
  ls ~/.pi/agent/skills/marker-pdf
  ```
  Expected: `SKILL.md`, `scripts/`, `requirements.txt`, `.env`, `.venv/`

- [ ] **venv has dependencies installed**
  ```bash
  ~/.pi/agent/skills/marker-pdf/.venv/bin/pip list | grep -E "requests|dotenv"
  ```
  Expected: both `requests` and `python-dotenv` listed

- [ ] **`.env` exists and has `MARKER_API_URL` set**
  ```bash
  cat ~/.pi/agent/skills/marker-pdf/.env
  ```
  Expected: a line like `MARKER_API_URL=http://localhost:8001`

- [ ] **Marker API server is reachable** (reads the URL straight from `.env`, no shell env needed)
  ```bash
  URL=$(grep MARKER_API_URL ~/.pi/agent/skills/marker-pdf/.env | cut -d= -f2)
  curl -sf "$URL/health" && echo OK
  ```
  Expected: `OK` printed, no connection error

- [ ] **Client script runs end-to-end** (replace with a real PDF path)
  ```bash
  ~/.pi/agent/skills/marker-pdf/.venv/bin/python \
    ~/.pi/agent/skills/marker-pdf/scripts/marker_client.py \
    /path/to/sample.pdf --format markdown
  ```
  Expected: JSON output with `"success": true`. The script loads `.env` itself — no need to export anything first.

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

Config lives in `marker-pdf/.env` (copied from `.env.example` during install), not in shell environment variables. The client script (`scripts/marker_client.py`) loads it automatically via `python-dotenv`.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MARKER_API_URL` | yes | `http://localhost:8001` | Base URL of your self-hosted Marker API |
| `MARKER_API_KEY` | no | *(commented out)* | Only needed if your Marker server has auth enabled. **This skill assumes no API key by default** — leave it commented out unless you explicitly enabled `MARKER_API_KEY` on the server side. |

To change a value:
```bash
nano ~/.pi/agent/skills/marker-pdf/.env
```

If the agent (not Marker) runs inside its own container separate from where Marker's Docker container runs, `localhost` in `.env` won't reach it — use the Docker Compose service name (e.g. `http://marker-api:8001`) or the host's real IP instead.

Real shell environment variables (`MARKER_API_URL`, `MARKER_API_KEY` exported in the current shell) still take precedence over `.env` if both are set — useful for one-off overrides.

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

No shell profile cleanup needed — all config lived in the skill's own `.env` file, which is removed along with the skill directory.