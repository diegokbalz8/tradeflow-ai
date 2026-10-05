from app.embeddings import create_embedding, cosine_similarity


question = "My cargo hasn't cleared customs yet."

document_1 = """
If a shipment is delayed during the customs process,
verify the shipment status and check whether customs
has requested additional documentation.
"""

document_2 = """
A commercial invoice normally contains information
about the buyer, seller, merchandise, quantity,
value, currency, and country of origin.
"""


question_embedding = create_embedding(question)
document_1_embedding = create_embedding(document_1)
document_2_embedding = create_embedding(document_2)


similarity_1 = cosine_similarity(
    question_embedding,
    document_1_embedding
)

similarity_2 = cosine_similarity(
    question_embedding,
    document_2_embedding
)


print("Question:", question)
print()
print("Shipment document similarity:", similarity_1)
print("Commercial invoice similarity:", similarity_2)