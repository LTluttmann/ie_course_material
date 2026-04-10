"""
download_models.py — Downloads spaCy models and NLTK corpora needed for the course.

Usage:
    uv run python scripts/download_models.py
"""

import subprocess
import easyocr
import sys


def section(title: str) -> None:
    print(f"\n{'─' * 52}")
    print(f"  {title}")
    print("─" * 52)


def download_spacy_models() -> None:
    section("spaCy models")
    models = [
        "en_core_web_sm",   # small English — used throughout
        "en_core_web_md",   # medium English — word vectors from Week 3
    ]
    for model in models:
        print(f"  Downloading {model} …")
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", model],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  ✅  {model}")
        else:
            print(f"  ❌  {model} failed:\n{result.stderr}")


def download_nltk_data() -> None:
    section("NLTK corpora & models")
    import nltk

    packages = [
        "punkt",
        "punkt_tab",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
        "maxent_ne_chunker",
        "maxent_ne_chunker_tab",
        "words",
        "stopwords",
        "conll2000",
        "brown",
    ]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
            print(f"  ✅  {pkg}")
        except Exception as e:
            print(f"  ❌  {pkg}: {e}")


def download_easyocr() -> None:
    section("EasyOCR")
    try:
        print("  Downloading EasyOCR models …")
        reader = easyocr.Reader(["en"], gpu=False)  # This will download the model
        print("  ✅  EasyOCR models downloaded")
    except Exception as e:
        print(f"  ❌  EasyOCR: {e}")


def main() -> None:
    print("\n🚀  Downloading course models & data …")
    download_spacy_models()
    download_nltk_data()
    download_easyocr()
    print("\n✅  Done! Run `uv run python scripts/check_setup.py` to verify.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if "spacy" in arg:
            download_spacy_models()
        elif "nltk" in arg:
            download_nltk_data()
        elif "ocr" in arg:
            download_easyocr()
        else:
            print(f"Unknown argument: {arg}")
    else:
        main()