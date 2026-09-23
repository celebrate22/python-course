
"""Word frequency counter (no regex): prints the top 5 words in a paragraph."""

import string
from collections import Counter

# Punctuation to strip, but keep apostrophes so "don't" stays one word.
PUNCT_TO_STRIP = string.punctuation.replace("'", "")


def top_words(text: str, n: int = 5):
    counts = Counter()
    for raw_word in text.lower().split():
        word = raw_word.strip(PUNCT_TO_STRIP).strip("'")
        if word:
            counts[word] += 1
    # tie-break alphabetically for deterministic output
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]


def main():
    paragraph = """The quick brown fox jumps over the lazy dog. The dog barks,
    but the fox is already gone. The lazy dog just watches the fox run
    quickly into the woods, and the quick fox disappears."""

    top = top_words(paragraph, 5)

    print("Top 5 words:")
    for i, (word, count) in enumerate(top, start=1):
        print(f"{i}. {word:<10} {count}")


if __name__ == "__main__":
    main()
