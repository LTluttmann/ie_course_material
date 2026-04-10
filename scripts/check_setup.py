"""
check_setup.py — Run this to verify your environment is correctly configured.

Usage:
    uv run python scripts/check_setup.py
"""

import importlib
import os
import sys
from ie_course.utils import load_rgb_image


FILEDIR = os.path.dirname(os.path.abspath(__file__))


def check(label: str, ok: bool, hint: str = "") -> bool:
    status = "✅" if ok else "❌"
    print(f"  {status}  {label}")
    if not ok and hint:
        print(f"       → {hint}")
    return ok


def import_ok(module: str) -> bool:
    try:
        importlib.import_module(module)
        return True
    except ImportError:
        return False


def main() -> None:
    all_ok = True
    print("\n── Python ──────────────────────────────────────────")
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 11
    all_ok &= check(
        f"Python {v.major}.{v.minor}.{v.micro}",
        ok,
        "Python 3.11+ required — use `uv python install 3.11`",
    )

    print("\n── Core NLP ────────────────────────────────────────")
    for pkg, hint in [
        ("spacy", "run `uv sync`"),
        ("cv2", "run `uv sync`"),
        ("nltk", "run `uv sync`"),
        ("easyocr", "run `uv sync`"),
        ("transformers", "run `uv sync`"),
        ("datasets", "run `uv sync`"),
    ]:
        all_ok &= check(pkg, import_ok(pkg), hint)

    print("\n── ML / Data ───────────────────────────────────────")
    for pkg in ["torch", "sklearn", "numpy", "pandas"]:
        all_ok &= check(pkg, import_ok(pkg), "run `uv sync`")

    print("\n── Extraction Utilities ────────────────────────────")
    for pkg in ["pydantic", "bs4", "lxml", "pypdf", "docx"]:
        all_ok &= check(pkg, import_ok(pkg), "run `uv sync`")

    print("\n── LLM Clients ─────────────────────────────────────")
    for pkg in ["openai", "anthropic", "instructor"]:
        all_ok &= check(pkg, import_ok(pkg), "run `uv sync`")

    print("\n── Notebooks ───────────────────────────────────────")
    all_ok &= check("jupyter", import_ok("jupyter"), "run `uv sync`")
    all_ok &= check("ipywidgets", import_ok("ipywidgets"), "run `uv sync`")

    print("\n── spaCy models ────────────────────────────────────")
    try:
        import spacy
        spacy.load("en_core_web_sm")
        all_ok &= check("en_core_web_sm", True)
    except OSError:
        all_ok &= check(
            "en_core_web_sm",
            False,
            "run `uv run python scripts/download_models.py spacy`",
        )

    print("\n── NLTK data ───────────────────────────────────────")
    try:
        import nltk
        nltk.data.find("tokenizers/punkt")
        all_ok &= check("punkt tokenizer", True)
    except LookupError:
        all_ok &= check(
            "punkt tokenizer",
            False,
            "run `uv run python scripts/download_models.py nltk`",
        )


    print("\n── EasyOCR data ───────────────────────────────────────")
    try:
        import easyocr
        reader = easyocr.Reader(["en"], gpu=False)  # This will check if the model is available
        img = load_rgb_image(os.path.join(FILEDIR, "../data/gemini_generated_invoice.png"), max_dim=800)
        reader.readtext(img)
        all_ok &= check("EasyOCR models", True)
    except Exception as e:
        print(f"  ❌  EasyOCR test failed: {e}")
        all_ok &= check(
            "EasyOCR models",
            False,
            "run `uv run python scripts/download_models.py ocr`",
        )

    # print("\n── Environment variables ───────────────────────────")
    # has_openai = bool(os.getenv("OPENAI_API_KEY"))
    # has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    # check("OPENAI_API_KEY set", has_openai, "needed from Week 5 — not required yet")
    # check("ANTHROPIC_API_KEY set", has_anthropic, "needed from Week 5 — not required yet")

    print("\n" + "─" * 52)
    if all_ok:
        print("🎉  All checks passed — you're ready to go!\n")
    else:
        print("⚠️   Some checks failed. See hints above and re-run.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
