"""The Houseplant Out-of-Office.

Writes a one-line out-of-office reply, as written by a houseplant,
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure Python standard library, no dependencies. Deterministic: the
entry text is a constant, so every run writes byte-identical output.
"""

import os
import sys

ENTRY = (
    # The \u2014 escape is an em dash; the entry reads as one plain line.
    "Thanks for your email! I'm out of the office this week \u2014 on the "
    "windowsill, photosynthesizing. Please water me on Tuesday and I'll "
    "reply once I've had some sun."
)

MIN_LENGTH = 90
MAX_LENGTH = 170


def validate(text):
    """Check the entry text against the competition's rules."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    return text


def main():
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError("written bytes differ from the entry text")
    validate(written.decode("utf-8"))
    print("wrote %s (%d characters)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
