import json
import re

from app.embeddings import create_embedding, cosine_similarity


def load_index():
    with open(
        "knowledge_base/index.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def extract_article_number(question):
    """
    Detect an explicit article number in the question.

    Examples:
    'según el artículo 1' -> 1
    'artículo 5' -> 5
    'articulo 138' -> 138
    """

    match = re.search(
        r"\bart[íi]culo\s+(\d+)",
        question,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


def retrieve(question, index, top_k=3):
    """
    Find the most relevant chunks for a user's question.
    """

    question_embedding = create_embedding(question)

    article_number = extract_article_number(question)

    results = []

    for item in index:

        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        # Give a small boost when the question
        # explicitly refers to an article.
        if article_number is not None:

            title = item["title"]

            article_match = re.search(
                r"\bart[íi]culo\s+(\d+)",
                title,
                re.IGNORECASE
            )

            if (
                article_match
                and int(article_match.group(1)) == article_number
            ):
                score += 0.20

        results.append({
            "chunk_id": item["chunk_id"],
            "source_file": item["source_file"],
            "document_title": item["document_title"],
            "source": item["source"],
            "document_type": item["document_type"],
            "institution": item["institution"],
            "status": item["status"],
            "level_2": item["level_2"],
            "level_3": item["level_3"],
            "level_4": item["level_4"],
            "title": item["title"],
            "text": item["text"],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":
    index = load_index()

    question = (
        "¿Con cuánto tiempo de anticipación debe transmitirse "
        "el manifiesto de ingreso por vía marítima?"
    )

    results = retrieve(
        question,
        index,
        top_k=3
    )

    for result in results:
        print("\n--- RESULTADO ---")
        print("Chunk:", result["chunk_id"])
        print("Archivo:", result["source_file"])
        print("Tipo:", result["document_type"])
        print("Institución:", result["institution"])
        print("Estado:", result["status"])
        print("Título:", result["title"])
        print("Score:", result["score"])
        print("\nTexto:")
        print(result["text"])