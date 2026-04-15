from flask import Flask, request, jsonify
from retriever import search_all_types, search
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@app.route('/')
def home():
    return {"msg":"ShyFit is Up !"}

@app.route('/get-workout', methods=['POST'])
def get_workout():
    data = request.get_json()
    query = data.get('query',"")
    if not query:
        return {"status": 400,"msg": "Query is required"}
    results = search_all_types(query)
    return jsonify(results)

@app.route('/chat',methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get("query","")

    if not query:
        return {"status": 400, "msg": "Query is Required"}

    retrived = search(query)
    context_text = ""

    for item in retrived:
        if item["type"] == "workout_plan":
            context_text += f"\nWorkout Plan: {item['title']} - {item['content']}\n"

        elif item["type"] == "exercise":
            context_text += f"\nExercise: {item['name']} - {item['content']}\n"

        elif item["type"] == "fitness_knowledge":
            context_text += f"\nTip: {item['content']}\n"

    prompt = f"""
        You are a professional fitness coach.

        Answer the user using ONLY the context below.
        If answer is not in context, say "I don't know".

        Context:
        {context_text}

        User Question:
        {query}
        """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )

    answer = response.choices[0].message.content

    return jsonify({
        "query" : query,
        "answer" : answer
    })



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)