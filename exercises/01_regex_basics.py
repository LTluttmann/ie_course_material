"""
Exercise 01 — Regex Basics for Information Extraction
======================================================
Complete the functions below. Run the tests with:

    uv run pytest tests/test_ex01.py -v

Do NOT modify the function signatures.
"""

import re


def extract_emails(text: str) -> list[str]:
    """
    Return all email addresses found in `text`.

    Example:
        >>> extract_emails("Contact us at hello@example.com or support@uni.de")
        ['hello@example.com', 'support@uni.de']
    """
    # TODO: implement
    raise NotImplementedError


def extract_dates(text: str) -> list[str]:
    """
    Return all dates matching DD.MM.YYYY or YYYY-MM-DD found in `text`.

    Example:
        >>> extract_dates("Born on 01.04.1990 and registered 2024-09-15.")
        ['01.04.1990', '2024-09-15']
    """
    # TODO: implement
    raise NotImplementedError


def extract_amounts(text: str) -> list[tuple[str, str]]:
    """
    Return (amount, currency) tuples for monetary values like "$1,200", "€99.99", "1 000 USD".

    Example:
        >>> extract_amounts("Price is $1,200 or €999.")
        [('1,200', 'USD'), ('999', 'EUR')]
    """
    # TODO: implement
    raise NotImplementedError
