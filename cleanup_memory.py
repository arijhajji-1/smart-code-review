import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="code_reviews")

# See everything currently in memory
results = collection.get()
print("Current IDs in memory:")
for id in results["ids"]:
    print(f"  - {id}")

# Delete test.py entries
ids_to_delete = [id for id in results["ids"] if "test" in id.lower()]
if ids_to_delete:
    collection.delete(ids=ids_to_delete)
    print(f"\n🗑️ Deleted: {ids_to_delete}")
else:
    print("\n✅ Nothing to delete")