from app.retrieval import load_index, retrieve
from app.relevance import check_relevance


questions = [
    "¿Cuánto tiempo antes debo transmitir un manifiesto de ingreso marítimo?",
    "¿Qué ocurre si un viaje marítimo dura menos de 48 horas?",
    "¿Cuánto tiempo antes debe transmitirse un manifiesto de ingreso aéreo?",
    "¿Cuánto tiempo después de la salida se transmite el detalle del manifiesto marítimo?",
    "¿Qué debe hacer el transportista internacional al ingresar mercancías?",
    "¿Qué ocurre con las mercancías cuando llegan al estacionamiento transitorio?",
    "¿Qué requisitos sanitarios necesito para importar un perro a Costa Rica?",
    "¿Cuál es el precio de almacenar mercancías en un depósito fiscal?",
    "¿Cómo puedo importar un automóvil usado?",
    "¿Qué documentos necesito para una importación?"
]


index = load_index()


for number, question in enumerate(questions, start=1):

    print("\n")
    print("=" * 60)
    print(f"TEST {number}")
    print("=" * 60)

    print(f"\nPregunta:\n{question}")

    chunks = retrieve(
        question,
        index,
        top_k=10
    )

    if not chunks:
        print("\nRetrieval: NO HAY RESULTADOS")
        continue

    print("\nTop 10 resultados:")

    for position, chunk in enumerate(chunks, start=1):
        print(
            f"{position}. "
            f"Score: {chunk['score']:.4f} | "
            f"{chunk['chunk_id']} | "
            f"{chunk['title']}"
        )

    relevance = check_relevance(
        question,
        chunks
    )

    print("\nRelevance check:")
    print(relevance)
