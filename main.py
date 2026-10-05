import os

from dotenv import load_dotenv
from openai import OpenAI

from app.retrieval import load_index, retrieve


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = load_index()

question = input("Customer: ")

results = retrieve(question, index)

relevant_information = "\n\n".join(
    result["text"]
    for result in results
)

print()
print("Retrieved information:")

for result in results:
    print(f"Similarity: {result['score']:.3f}")
    print(result["text"])
    print("---")

response = client.responses.create(
    model="gpt-5-mini",
    instructions="""
You are a customs and logistics support assistant for TradeFlow.

Answer the customer's question using the provided TradeFlow documentation.

If the documentation does not contain enough information to answer the question,
say that you do not have enough information and recommend contacting a customs specialist.
""",
    input=f"""
Relevant TradeFlow documentation:

{relevant_information}

Customer question:

{question}
"""
)

print("TradeFlow AI:")
print(response.output_text)