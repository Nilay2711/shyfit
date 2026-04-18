import json
import faiss
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Lazy globals ---
_model = None
_index = None
_metadata = None

def _load():
    global _model, _index, _metadata
    if _model is not None:
        return  # Already loaded

    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings_path = os.path.join(BASE_DIR, "embeddings.npy")
    metadata_path = os.path.join(BASE_DIR, "metadata.json")

    if os.path.exists(embeddings_path) and os.path.exists(metadata_path):
        print("Loading saved embeddings...")
        embeddings = np.load(embeddings_path)
        with open(metadata_path, "r") as f:
            _metadata = json.load(f)
    else:
        print("Creating embeddings...")
        with open(os.path.join(BASE_DIR, "final_dataset.json"), "r") as f:
            data = json.load(f)

        documents = []
        _metadata = []
        for item in data:
            if item["type"] == "workout_plan":
                text = f"WORKOUT PLAN {item['goal']} {item['level']} {item['title']} {item['content']}"
            elif item["type"] == "exercise":
                text = f"EXERCISE {item['name']} {' '.join(item['muscles'])} {item['content']}"
            elif item["type"] == "fitness_knowledge":
                text = f"FITNESS KNOWLEDGE {item['topic']} {item['content']}"
            else:
                text = item.get("content", "")
            documents.append(text)
            _metadata.append(item)

        embeddings = _model.encode(documents)
        embeddings = np.array(embeddings).astype("float32")
        np.save(embeddings_path, embeddings)
        with open(metadata_path, "w") as f:
            json.dump(_metadata, f)

    embeddings = np.array(embeddings).astype("float32")
    dimensions = embeddings.shape[1]
    _index = faiss.IndexFlatL2(dimensions)
    _index.add(embeddings)
    print("Retriever ready.")


def search(query, k=5, type_filter=None):
    _load()
    query_vector = _model.encode([query])
    query_vector = np.array(query_vector).astype("float32")
    distances, indices = _index.search(query_vector, 50)

    results = []
    for idx in indices[0]:
        item = _metadata[idx]
        if type_filter and item["type"] != type_filter:
            continue
        formatted = {"type": item["type"]}
        if item["type"] == "workout_plan":
            formatted.update({"title": item["title"], "goal": item["goal"], "level": item["level"], "content": item["content"]})
        elif item["type"] == "exercise":
            formatted.update({"name": item["name"], "muscles": item["muscles"], "content": item["content"]})
        elif item["type"] == "fitness_knowledge":
            formatted.update({"topic": item["topic"], "content": item["content"]})
        results.append(formatted)
        if len(results) >= k:
            break
    return results


def search_all_types(query):
    return {
        "workouts": search(query, k=3, type_filter="workout_plan"),
        "exercises": search(query, k=3, type_filter="exercise"),
        "knowledge": search(query, k=2, type_filter="fitness_knowledge")
    }


if __name__ == "__main__":
    query = "beginner fat loss workout"
    results = search_all_types(query)
    print(json.dumps(results, indent=2))