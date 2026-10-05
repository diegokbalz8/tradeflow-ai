from pathlib import Path
import re
from collections import Counter


file_path = Path(
    "knowledge_base/Ley_General_Aduanas_latest.md"
)

text = file_path.read_text(
    encoding="utf-8"
)


matches = re.findall(
    r"^####\s+(?:ARTICULO|ARTÍCULO|Artículo)\s+(\d+)",
    text,
    re.MULTILINE
)


article_numbers = [
    int(number)
    for number in matches
]

unique_articles = sorted(
    set(article_numbers)
)

article_counts = Counter(
    article_numbers
)

duplicates = {
    number: count
    for number, count in article_counts.items()
    if count > 1
}


print("\n=== ARTICLE ANALYSIS ===")

print(
    f"Article headings detected: "
    f"{len(article_numbers)}"
)

print(
    f"Unique article numbers: "
    f"{len(unique_articles)}"
)


print("\nFirst 20:")

print(
    unique_articles[:20]
)


print("\nLast 20:")

print(
    unique_articles[-20:]
)


print("\n=== DUPLICATE ARTICLE NUMBERS ===")

if duplicates:

    for number, count in sorted(
        duplicates.items()
    ):
        print(
            f"Article {number}: "
            f"{count} occurrences"
        )

else:

    print("No duplicates found.")


print("\n=== POSSIBLE GAPS ===")

if unique_articles:

    minimum = min(unique_articles)
    maximum = max(unique_articles)

    missing = [
        number
        for number in range(
            minimum,
            maximum + 1
        )
        if number not in unique_articles
    ]

    print(
        f"Range: {minimum} → {maximum}"
    )

    print(
        f"Missing article numbers: "
        f"{missing}"
    )