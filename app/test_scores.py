from app.retrieval import load_index, retrieve


questions = [
    "¿Cuánto tiempo antes debo transmitir un manifiesto de ingreso marítimo?",
    "¿Cuánto tiempo tengo para transmitir el detalle del manifiesto de salida marítimo?",
    "¿Qué requisitos sanitarios necesito para importar un perro a Costa Rica?"
]


index = load_index()


for question in questions:

    print("\n==============================")
    print("PREGUNTA")
    print("==============================")
    print(question)

    results = retrieve(
        question,
        index,
        top_k=3
    )

    print("\nRESULTADOS:")

    for result in results:
        print(
            f"- Score: {result['score']:.4f} | "
            f"{result['chunk_id']} | "
            f"{result['title']}"
        )