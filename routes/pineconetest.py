from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

print("Starting...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # Load model
# Create Pinecone client
pc = Pinecone(api_key="pcsk_ihwQL_E17W62oEwcD99DsUM8GZ5GwCZzm3Yux1iatpfb39NTuhUtXiKGd228GmxYrXhKx",
              environment='aped-4627-b74a')
# Connect to index
index = pc.Index("ind384")

# ************** Fetching the similarities from the created embeddings ********************✅
# Input text
def vector_db_query(query_text):
    query_embedding = model.encode(query_text).tolist()
    response = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True,
        namespace="ns1")
    # Return only the serializable parts
    results = []
    for match in response['matches']: # type: ignore
        results.append({
            "id": match['id'],
            "score": match['score'],
            "metadata": match.get('metadata', {})
        })
    return results

print("Successfull")
