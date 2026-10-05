from app.retrieval import load_index, retrieve
from app.relevance import check_relevance


questions = [
    "¿Cuánto tiempo antes debo transmitir un manifiesto de ingreso marítimo?",
    "¿Qué ocurre si un viaje marítimo dura menos de 48 horas?",
    "¿Cuánto cobra un depósito fiscal por almacenar mercancías?"
]


index = load_index()


for question in questions:

    print("\n==============================")
    print("PREGUNTA")
    print("==============================")
    print(question)

    chunks = retrieve(
        question,
        index,
        top_k=10
    )

    if not chunks:
        print("\nRetrieval: NO HAY RESULTADOS")
        continue

    print("\nRETRIEVAL:")
    for chunk in chunks:
        print(
            f"- Score: {chunk['score']:.4f} | "
            f"{chunk['chunk_id']} | "
            f"{chunk['title']}"
        )

    relevance = check_relevance(
        question,
        chunks
    )

    print("\nRELEVANCE CHECK:")
    print(relevance)