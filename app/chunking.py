from pathlib import Path
import re


def load_markdown(file_path):
    return Path(file_path).read_text(encoding="utf-8")


def clean_pdf_artifacts(text):
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Remove standalone page numbers
        if re.fullmatch(r"\d+", stripped):
            continue

        # Remove repeated PDF headers
        if "Dirección de Gestión Técnica" in stripped:
            continue

        if "Departamento de Procesos Aduaneros" in stripped:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def split_by_headings(text):
    pattern = r"^(#{2,4}) (.+)$"

    matches = list(re.finditer(pattern, text, re.MULTILINE))

    sections = []

    current_level_2 = None
    current_level_3 = None
    current_level_4 = None

    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        content = text[start:end].strip()

        # Update the heading hierarchy
        if level == 2:
            current_level_2 = title
            current_level_3 = None
            current_level_4 = None

        elif level == 3:
            current_level_3 = title
            current_level_4 = None

        elif level == 4:
            current_level_4 = title

        sections.append({
            "level": level,
            "title": title,
            "level_2": current_level_2,
            "level_3": current_level_3,
            "level_4": current_level_4,
            "content": content
        })

    return sections


def split_large_section(section, max_words=600):
    content = section["content"]
    original_word_count = len(content.split())

    # If the section is already small enough, keep it intact
    if original_word_count <= max_words:
        chunk = section.copy()
        chunk["word_count"] = original_word_count
        return [chunk]

    # Split the content into paragraphs
    paragraphs = re.split(r"\n\s*\n", content)

    chunks = []
    current_paragraphs = []
    current_word_count = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        paragraph_word_count = len(paragraph.split())

        # If adding this paragraph would exceed the limit,
        # save the current chunk first.
        if (
            current_paragraphs
            and current_word_count + paragraph_word_count > max_words
        ):
            chunk = section.copy()
            chunk["content"] = "\n\n".join(current_paragraphs)
            chunk["word_count"] = current_word_count

            chunks.append(chunk)

            current_paragraphs = []
            current_word_count = 0

        current_paragraphs.append(paragraph)
        current_word_count += paragraph_word_count

    # Save the final chunk
    if current_paragraphs:
        chunk = section.copy()
        chunk["content"] = "\n\n".join(current_paragraphs)
        chunk["word_count"] = current_word_count

        chunks.append(chunk)

    return chunks


def create_chunks(sections, max_words=600, file_path=None):
    chunks = []

    for section in sections:
        if not section["content"].strip():
            continue

        section_chunks = split_large_section(
            section,
            max_words=max_words
        )

        for chunk in section_chunks:
            chunk["text_for_embedding"] = build_embedding_text(chunk)

            if file_path:
                chunk = add_metadata(chunk, file_path)

            chunks.append(chunk)

    return chunks


def build_embedding_text(chunk):
    parts = []

    if chunk["level_2"]:
        parts.append(chunk["level_2"])

    if chunk["level_3"]:
        parts.append(chunk["level_3"])

    if chunk["level_4"]:
        parts.append(chunk["level_4"])

    parts.append(chunk["content"])

    return "\n\n".join(parts)


def add_metadata(chunk, file_path):
    chunk["source"] = "Ministerio de Hacienda - Dirección General de Aduanas"
    chunk["source_file"] = file_path.name

    return chunk


def add_chunk_id(chunk, index, document_name):
    chunk["chunk_id"] = f"{document_name}_{index:04d}"

    return chunk




if __name__ == "__main__":
    file_path = "knowledge_base/IngresoSalida.md"

    text = load_markdown(file_path)

    text = clean_pdf_artifacts(text)

    sections = split_by_headings(text)

    chunks = create_chunks(sections, max_words=600)

    print()
    print("CHUNKING SUMMARY")
    print("=" * 80)

    print(f"Sections detected: {len(sections)}")
    print(f"Chunks created: {len(chunks)}")

    print()
    print("EMBEDDING TEXT EXAMPLE")
    print("=" * 80)

    # Find the first chunk that has a Level 3 heading
    for i, chunk in enumerate(chunks, start=1):
        if chunk["level_3"]:
            embedding_text = build_embedding_text(chunk)

            print(f"Chunk {i}")
            print("-" * 80)
            print(embedding_text[:2000])
            print("-" * 80)

            break

    print()
    print("METADATA EXAMPLE")
    print("=" * 80)

    chunk = chunks[8]

    print(f"Source: {chunk['source']}")
    print(f"Document: {chunk['document']}")
    print(f"Procedure: {chunk['procedure']}")
    print(f"Level 2: {chunk['level_2']}")
    print(f"Level 3: {chunk['level_3']}")
    print(f"Word count: {chunk['word_count']}")

    print()
    print("CHUNK ID EXAMPLE")
    print("=" * 80)

    for chunk in chunks[:5]:
        print(
            f"{chunk['chunk_id']} | "
            f"{chunk['word_count']} words | "
            f"{chunk['title']}"
        )