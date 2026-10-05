def select_sources(
    retrieved_chunks,
    max_sources=3
):
    """
    Select the most relevant sources to use
    for the final answer.
    """

    selected = []

    seen = set()

    for chunk in retrieved_chunks:

        key = (
            chunk["source_file"],
            chunk["title"]
        )

        if key in seen:
            continue

        seen.add(key)

        selected.append(chunk)

        if len(selected) >= max_sources:
            break

    return selected