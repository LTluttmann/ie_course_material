# Information Extraction in Python 🐍

Course materials for the **Information Extraction in Python** seminar.

---

## 🛠️ Setup (do this once)

### 1. Install `uv`

`uv` is a fast Python package manager. Install it with one command:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal after installing, then verify:
```bash
uv --version
```

---

### 2. Clone the repository

```bash
git clone https://github.com/LTluttmann/ie_course_material.git
cd ie_course_material
```

---

### 3. Create the environment & install dependencies

```bash
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install all dependencies from `pyproject.toml`
- Install dev tools (pytest, ruff, etc.)

No need to manually `pip install` anything.

---

### 4. Download required NLP models

Run the setup script to download spaCy models and NLTK data:

```bash
uv run python scripts/download_models.py
```

---

### 5. Activate the environment (optional)

`uv run` handles this automatically, but if you want a traditional shell activation:

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

---

## 📓 Running Notebooks

```bash
uv run jupyter lab
```

Notebooks are in the `notebooks/` directory.

---

## ✅ Verify your setup

```bash
uv run python scripts/check_setup.py
```

All checks should show ✅.

---

## 🗂️ Repository Structure

```
ie_course_material/
├── pyproject.toml          # Dependencies & project config
├── notebooks/              # Lecture notebooks (01_, 02_, ...)
├── exercises/              # Starter code for exercises
├── solutions/              # Exercise solutions (released weekly)
├── src/
│   └── ie_course/          # Shared helper library
│       ├── __init__.py
│       └── utils.py
├── data/                   # data we might use
└── scripts/
    ├── check_setup.py      # Environment verification
    └── download_models.py  # Model downloader
```

---

## 🔑 API Keys (OPTIONAL)
NOTE: we are working on a solution to use LLMs running on universiy hardware.

Some exercises use LLM APIs. Set your keys as environment variables:


```bash
# macOS / Linux — add to ~/.zshrc or ~/.bashrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Or create a `.env` file in the project root (already in `.gitignore`):
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🔄 Updating dependencies

If new packages are added during the course, just run:
```bash
uv sync
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `uv: command not found` | Restart your terminal after install |
| `ModuleNotFoundError` | Run `uv sync` then `uv run python ...` |
| Jupyter kernel issues | `uv run python -m ipykernel install --user` |
| spaCy model missing | `uv run python scripts/download_models.py spacy` |
| Slow `uv sync` on first run | Normal — it's downloading ~2 GB of ML libraries |

