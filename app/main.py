from app.retrieval import load_index, retrieve
from app.relevance import check_relevance
from app.generation import generate_answer
from app.source_selection import select_sources


def main():
    print("\n==============================")
    print("TRADEFLOW AI")
    print("==============================")
    print("Escribe 'salir' para terminar.\n")

    index = load_index()

    while True:
        question = input("Tu pregunta: ")

        if question.lower() == "salir":
            print("\nHasta luego.")
            break

        if not question.strip():
            print("Por favor, escribe una pregunta.\n")
            continue

        retrieved_chunks = retrieve(
            question,
            index,
            top_k=10
        )

        if not retrieved_chunks:
            answer = (
                "No tengo información suficiente en mi base de conocimiento "
                "para responder esa pregunta."
            )

            selected_sources = []

        else:
            relevance = check_relevance(
                question,
                retrieved_chunks
            )

            if relevance == "RELEVANT":

                selected_sources = select_sources(
                    retrieved_chunks,
                    max_sources=3
                )

                answer = generate_answer(
                    question,
                    selected_sources
                )

            else:
                answer = (
                    "No tengo información suficiente en mi base de "
                    "conocimiento para responder esa pregunta."
                )

                selected_sources = []

        print("\nTradeFlow:")
        print(answer)

        if selected_sources:
            print("\nFuentes:")

            for chunk in selected_sources:
                print(
                    f"- {chunk['source_file']} | "
                    f"{chunk['title']}"
                )

        print()


if __name__ == "__main__":
    main()