from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import json
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
OUTPUT_FILE = "final_dataset.json"

client = OpenAI(api_key=api_key)


def safe_parse(text):
    try:
        text = text.strip()

        # Remove markdown if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text)

    except Exception as e:
        print(f"Error Happened: {e}")
        return []
    

def save_data(data):
    try:
        with open(OUTPUT_FILE,'r') as f:
            existing = json.load(f)
    except:
        existing = []
    
    existing.extend(data)
    
    with open(OUTPUT_FILE,"w") as f2:
        json.dump(existing,f2,indent=2)


# ---------- PROMPTS ----------

workout_prompt = """
Generate 10 realistic workout plans in JSON array.

Each object must contain:
id, type, goal, level, duration, days_per_week, title, content, tags

Rules:
- Content must be detailed and day-wise
- Include exercises, sets, reps, rest time
- Goals: fat_loss, muscle_gain, strength
- Levels: beginner, intermediate, advanced
- type = "workout_plan"

Return ONLY valid JSON array.
"""

exercise_prompt = """
Generate 10 exercises in JSON array.

Each object must contain:
id, type, name, muscles, level, equipment, content, tips, mistakes

Rules:
- Practical descriptions
- Include form guidance
- Include 2-3 tips and mistakes
- type = "exercise"

Return ONLY valid JSON array.
"""

knowledge_prompt = """
Generate 10 fitness knowledge entries in JSON array.

Each object must contain:
id, type, topic, content

Rules:
- Topics: diet, recovery, fat_loss, muscle_gain, sleep
- Keep it informative but concise
- type = "fitness_knowledge"

Return ONLY valid JSON array.
"""


def generating_workout(prompt,batches,label):
    for i in range(batches):
        print(f"Generating {label} batch {i+1} / {batches}")

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            text = response.choices[0].message.content
            data = safe_parse(text)

            if(data):
                save_data(data)
                print(f"The Data is saved {len(data)} items")

            else:
                print("Skipped the batch ")

        except Exception as e:
            print(f"The Error Occured {e}")

        time.sleep(2)



if __name__ == "__main__":
    generating_workout(workout_prompt, 12, "workouts")   # 120
    generating_workout(exercise_prompt, 12, "exercises") # 120
    generating_workout(knowledge_prompt, 10, "knowledge") # 100

    print("\n🎉 Dataset generation complete!")