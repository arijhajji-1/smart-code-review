import chromadb
from datetime import datetime

# Create a local ChromaDB (saves to disk automatically)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="code_reviews")


# --- SAVE a report to the vector DB ---
def save_review(filename, ai_feedback, flake8_output, complexity_output):
    # Combine everything into one searchable document
    full_report = f"""
    FILE: {filename}
    DATE: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    FLAKE8:
    {flake8_output}

    COMPLEXITY:
    {complexity_output}

    AI FEEDBACK:
    {ai_feedback}
    """

    # Save with a unique ID
    doc_id = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    collection.add(
        documents=[full_report],
        metadatas=[{"filename": filename, "date": datetime.now().strftime("%Y-%m-%d")}],
        ids=[doc_id]
    )

    print(f"💾 Saved to memory: {doc_id}")


# --- SEARCH reports by meaning ---
def search_reviews(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if not results["documents"][0]:
        return "No matching reviews found."

    output = []
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        output.append(f"--- Match {i+1}: {metadata['filename']} ({metadata['date']}) ---\n{doc}")

    return "\n\n".join(output)

# --- TEST ---
if __name__ == "__main__":
    # Save a fake report
    save_review(
        filename="test.py",
        ai_feedback="Found a hardcoded password on line 12. Security risk.",
        flake8_output="test.py:12:1 E501 line too long",
        complexity_output="F 5:0 calculate - B (7)"
    )

    # Search for it
    print("\n🔍 Searching for 'security issues'...\n")
    results = search_reviews("security issues")
    print(results)