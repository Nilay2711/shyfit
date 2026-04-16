import json
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "final_dataset.json"), "r") as f:
    data = json.load(f)

documents = []
metadata = []

for item in data:
    text = ""

    if item["type"] == "workout_plan":
        text = f"WORKOUT PLAN {item['goal']} {item['level']} {item['title']} {item['content']}"

    elif item["type"] == "exercise":
        text = f"EXERCISE {item['name']} {' '.join(item['muscles'])} {item['content']}"
    elif item["type"] == "fitness_knowledge":
        text = f"FITNESS KNOWLEDGE {item['topic']} {item['content']}"

    documents.append(text)
    metadata.append(item)




if os.path.exists("embeddings.npy"):
    print("Loading saved embeddings...")
    embeddings = np.load("embeddings.npy")

    with open("metadata.json", "r") as f:
        metadata = json.load(f)

else:
    print("Creating embeddings...")
    embeddings = model.encode(documents)
    embeddings = np.array(embeddings).astype("float32")

    np.save("embeddings.npy", embeddings)

    with open("metadata.json", "w") as f:
        json.dump(metadata, f)


embeddings = np.array(embeddings).astype("float32")

np.save("embeddings.npy", embeddings)

with open("metadata.json", "w") as f:
    json.dump(metadata, f)

dimensions = embeddings.shape[1]

index = faiss.IndexFlatL2(dimensions)

index.add(embeddings)

def search_all_types(query):
    return {
        "workouts": search(query, k=3, type_filter="workout_plan"),
        "exercises": search(query, k=3, type_filter="exercise"),
        "knowledge": search(query, k=2, type_filter="fitness_knowledge")
    }


def search(query, k=5, type_filter=None):
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(query_vector, 50)

    results = []

    for idx in indices[0]:
        item = metadata[idx]

        if type_filter and item["type"] != type_filter:
            continue

        # Format response
        formatted = {
            "type": item["type"]
        }

        if item["type"] == "workout_plan":
            formatted.update({
                "title": item["title"],
                "goal": item["goal"],
                "level": item["level"],
                "content": item["content"]
            })

        elif item["type"] == "exercise":
            formatted.update({
                "name": item["name"],
                "muscles": item["muscles"],
                "content": item["content"]
            })

        elif item["type"] == "fitness_knowledge":
            formatted.update({
                "topic": item["topic"],
                "content": item["content"]
            })

        results.append(formatted)

        if len(results) >= k:
            break

    return results

if __name__ == "__main__":
    query = "beginner fat loss workout"

    results = search_all_types(query)

    print(json.dumps(results, indent=2))