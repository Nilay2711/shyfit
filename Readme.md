# 💪 ShyFit – RAG-Based AI Fitness Assistant

🚀 **Live Demo**
Frontend: https://shyfit.netlify.app
Backend API: https://shyfit.onrender.com

---

ShyFit is an AI-powered fitness assistant that generates personalized workout plans and answers fitness-related questions using a **Retrieval-Augmented Generation (RAG)** system.

---

## 🚀 Features

* 🧠 **AI Workout Generator**
  Generates structured workout plans based on user queries

* 🔍 **Semantic Search (RAG)**
  Uses FAISS + embeddings to retrieve relevant fitness data

* 🤖 **AI Coach Chatbot**
  Context-aware chatbot that answers fitness questions

* ⚡ **Fast Retrieval System**
  Precomputed embeddings for instant results

* 🎨 **Modern UI**
  Clean frontend with interactive chat experience

---

## 🏗️ Tech Stack

### Backend

* Python
* Flask
* FAISS (Vector Database)
* Sentence Transformers
* OpenAI API

### Frontend

* HTML + Tailwind CSS
* jQuery
* AJAX

---

## 🧠 How It Works

1. User enters a query (e.g., *"beginner fat loss workout"*)
2. Query is converted into embeddings
3. FAISS retrieves relevant documents from dataset
4. Results are:

   * Displayed as workout plans
   * Used as context for chatbot
5. Chatbot generates grounded responses using LLM

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/yourusername/shyfit.git
cd shyfit
```

---

### 2. Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Run backend:

```
python app.py
```

---

### 3. Frontend Setup

Simply open:

```
frontend/index.html
```

OR use Live Server in VS Code.

---

## 🌐 API Endpoints

### 🔹 Get Workout Plans

```
POST /get-workout
```

**Body:**

```
{
  "query": "fat loss workout"
}
```

---

### 🔹 Chat with Coach

```
POST /chat
```

**Body:**

```
{
  "query": "Is this workout good for beginners?"
}
```

---

## 🚀 Deployment

* Backend → Render
* Frontend → Netlify

Update API URLs in frontend after deployment.

---

## 📌 Future Improvements

* Chat memory (conversation context)
* User authentication
* Workout tracking dashboard
* Personalized recommendations

---

## 👨‍💻 Author

**Nilay Pandya**

---

## ⭐ If you like this project

Give it a star on GitHub!
