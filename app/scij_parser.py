import re

from bs4 import BeautifulSoup


def clean_text(text):
    """
    Clean whitespace from extracted legal text.
    """

    text = text.replace("\xa0", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_scij_html(html):
    """
    Extract readable legal text from SCIJ HTML.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup.find_all(
        ["style", "script", "input", "button"]
    ):
        tag.decompose()

    lines = []

    for paragraph in soup.find_all("p"):

        text = clean_text(
            paragraph.get_text(
                " ",
                strip=True
            )
        )

        if not text:
            continue

        lines.append(text)

    return lines

def convert_to_markdown(lines, metadata=None):
    """
    Convert extracted SCIJ lines into Markdown.

    Metadata is stored at the beginning of the document
    using YAML front matter.
    """

    markdown = []

    # Add document metadata
    if metadata:

        markdown.append("---")

        for key, value in metadata.items():

            markdown.append(
                f"{key}: {value}"
            )

        markdown.append("---")
        markdown.append("")

    current_title = None
    current_chapter = None

    skip_lines = {
        "NÂ° 7557",
        "LEY GENERAL DE ADUANAS",
        "LA ASAMBLEA LEGISLATIVA DE LA REPÃšBLICA DE COSTA RICA",
        "DECRETA:"
    }

    i = 0

    while i < len(lines):

        line = lines[i]

        # Ignore document introduction
        if line in skip_lines:
            i += 1
            continue

        # TITULO
        if re.fullmatch(
            r"TITULO\s+[IVXLCDM]+",
            line,
            re.IGNORECASE
        ):

            current_title = line

            title_name = ""

            if i + 1 < len(lines):
                next_line = lines[i + 1]

                if not re.match(
                    r"^(TITULO|CAPITULO|ARTICULO|ARTÍCULO|ArtÃ­culo)",
                    next_line,
                    re.IGNORECASE
                ):
                    title_name = next_line
                    i += 1

            if title_name:
                markdown.append(
                    f"## {current_title} — {title_name}"
                )
            else:
                markdown.append(
                    f"## {current_title}"
                )

            i += 1
            continue

        # CAPITULO
        if re.fullmatch(
            r"CAPITULO\s+.*",
            line,
            re.IGNORECASE
        ):

            current_chapter = line

            chapter_name = ""

            if i + 1 < len(lines):
                next_line = lines[i + 1]

                if not re.match(
                    r"^(TITULO|CAPITULO|ARTICULO|ARTÍCULO|ArtÃ­culo)",
                    next_line,
                    re.IGNORECASE
                ):
                    chapter_name = next_line
                    i += 1

            if chapter_name:
                markdown.append(
                    f"### {current_chapter} — {chapter_name}"
                )
            else:
                markdown.append(
                    f"### {current_chapter}"
                )

            i += 1
            continue

        # ARTICLE
        if re.match(
            r"^(ARTICULO|ARTÍCULO|Artículo|ArtÃ­culo)\s+\d",
            line,
            re.IGNORECASE
        ):

            markdown.append(
                f"#### {line}"
            )

            i += 1
            continue

        markdown.append(line)

        i += 1

    return "\n\n".join(markdown)


if __name__ == "__main__":

    with open(
        "knowledge_base/scij_ley_7557.html",
        "r",
        encoding="utf-8"
    ) as file:
        html = file.read()

    lines = parse_scij_html(html)

    print(
        f"Extraídas {len(lines)} líneas."
    )

    markdown = convert_to_markdown(lines)

    output_file = (
        "knowledge_base/Ley_General_Aduanas.md"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(markdown)

    print(
        f"Markdown creado: {output_file}"
    )

    print("\n=== PRIMERAS 1000 CARACTERES ===\n")
    print(markdown[:1000])