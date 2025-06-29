from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import together
from together import Together

print("Starting...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # Load model
# Create Pinecone client

together.api_key = ""
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
        top_k=2,
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

def query_together_ai(results, user_query):
    # Build context from metadata
    context = ""
    for match in results:
        metadata = match.get("metadata", {})
        context_piece = metadata.get("text", "")
        context += f"- {context_piece}\n"

    if not context.strip():
        context = "No relevant information found."

    prompt = f"""You are an enthusiastic and helpful AI assistant. When a user asks about a product or topic, your job is to respond in an engaging, concise, and informative way.
📝 **Instructions**:
- Use only the information provided in the context below to answer the question.
- If relevant information exists in the context, briefly present it in a helpful tone.
- If the answer is not found in the context, politely say you don't have enough information and do not make anything up.
- Your response **must be in Markdown format**.
- Avoid including any data that are not present in the context.
- At the end, ask if the user would like to know more or explore another topic.

📚 **Context**:
---------
{context}

❓ **Question**:{user_query}

💬 **Your Answer**:"""

    # Send request to Together AI
    response = together.Complete.create(
        prompt=prompt,
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=200,
        temperature=0.7
    )

    # Debug full response
    print("Together AI response:", response)

    # Parse result safely
    try:
        choices = response.get("choices", [])
        if choices and "text" in choices[0]:
            raw_text = choices[0]["text"].strip()
            html_text = raw_text.replace("\n", "<br>")
            html_text = raw_text.replace("/", "<br>")
            return html_text
        else:
            return "Sorry, I couldn't find a valid answer in the response."
    except Exception as e:
        print("Error parsing Together AI response:", e)
        return "Error: Could not get a valid response from Together AI."
