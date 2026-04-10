"""
ie_course.utils — Shared helpers used across notebooks and exercises.
"""

from __future__ import annotations

import cv2
import re
from pathlib import Path
from typing import Any


# ── Text helpers ───────────────────────────────────────────────────────────

def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace (including newlines) to a single space."""
    return re.sub(r"\s+", " ", text).strip()


def sentence_tokenize(text: str) -> list[str]:
    """Split text into sentences using NLTK's Punkt tokenizer."""
    import nltk
    return nltk.sent_tokenize(text)


def load_text(path: str | Path) -> str:
    """Read a plain-text file, normalizing line endings."""
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


# ── NER helpers ────────────────────────────────────────────────────────────

def ents_to_dict(doc: Any) -> dict[str, list[str]]:
    """Convert a spaCy Doc's entities to a label→[surface forms] dict."""
    result: dict[str, list[str]] = {}
    for ent in doc.ents:
        result.setdefault(ent.label_, []).append(ent.text)
    return result


# ── Evaluation ─────────────────────────────────────────────────────────────

def span_f1(
    gold: list[tuple[int, int, str]],
    pred: list[tuple[int, int, str]],
) -> dict[str, float]:
    """
    Token-level span F1 for NER.

    Args:
        gold: list of (start, end, label) tuples
        pred: list of (start, end, label) tuples

    Returns:
        {"precision": ..., "recall": ..., "f1": ...}
    """
    gold_set = set(gold)
    pred_set = set(pred)
    tp = len(gold_set & pred_set)
    precision = tp / len(pred_set) if pred_set else 0.0
    recall = tp / len(gold_set) if gold_set else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


# ── Pretty printing ────────────────────────────────────────────────────────

def print_ents(doc: Any) -> None:
    """Pretty-print entities from a spaCy Doc using Rich."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Named Entities", show_lines=True)
    table.add_column("Text", style="cyan")
    table.add_column("Label", style="magenta")
    table.add_column("Start", justify="right")
    table.add_column("End", justify="right")
    for ent in doc.ents:
        table.add_row(ent.text, ent.label_, str(ent.start_char), str(ent.end_char))
    console.print(table)


def load_image(path: str | Path, min_dim: int = None, max_dim: int = None) -> Any:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Could not load image from {path}")
    if max_dim is not None or min_dim is not None:
        image = resize_with_min_max(image, max_dim=max_dim, min_dim=min_dim)
    return image

def load_rgb_image(path: str | Path, min_dim: int = None, max_dim: int = None) -> Any:
    image = load_image(path, min_dim=min_dim, max_dim=max_dim)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def resize_with_min_max(image, max_dim=None, min_dim=None):
    if min_dim is None and max_dim is None:
        return image
    if min_dim is not None and max_dim is not None and min_dim > max_dim:
        raise ValueError("min_dim cannot be greater than max_dim")

    h, w = image.shape[:2]    
    if max_dim is not None:
        # Determine scaling factor
        max_scale = max_dim / max(h, w)

        # Only resize if the image is larger than max_dim
        if max_scale < 1:
            new_w = int(w * max_scale)
            new_h = int(h * max_scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    if min_dim is not None:
        # Determine scaling factor
        min_scale = min_dim / min(h, w)

        # Only resize if the image is smaller than min_dim
        if min_scale > 1:
            new_w = int(w * min_scale)
            new_h = int(h * min_scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    return image