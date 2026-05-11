"""
modules/filler_detector.py
Detects common filler words in interview transcripts.
"""

FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically",
    "kind of", "sort of", "right", "okay", "so",
    "actually", "literally", "honestly", "definitely",
    "i mean", "you see", "well", "just"
]


def detect_filler_words(text: str) -> int:
    """
    Returns the total count of filler word occurrences in the transcript.
    """
    text_lower = text.lower()
    total = 0

    for filler in FILLER_WORDS:
        # Use word-boundary-aware counting
        import re
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        total += len(matches)

    return total


def get_filler_breakdown(text: str) -> dict:
    """
    Returns a dict of {filler_word: count} for the most common fillers.
    """
    import re
    text_lower = text.lower()

    breakdown = {
        "um / uh":   len(re.findall(r'\b(um|uh)\b', text_lower)),
        "like":      len(re.findall(r'\blike\b', text_lower)),
        "you know":  len(re.findall(r'\byou know\b', text_lower)),
        "basically": len(re.findall(r'\bbasically\b', text_lower)),
        "kind of":   len(re.findall(r'\bkind of\b', text_lower)),
        "so":        max(0, len(re.findall(r'\bso\b', text_lower)) - 1),
    }

    return breakdown
