---

Backend service for a **Conversational AI system** supporting:

* Open chat with an external LLM
* Grounded (RAG) chat over uploaded PDFs
* Persistent conversation history

---

## Tech Stack

FastAPI · PostgreSQL · Groq (Llama) · SQLAlchemy · pypdf

---

## Features

* Multi-turn conversations
* Open & document-grounded chat
* PDF upload → text extraction → chunk retrieval
* List, resume, and delete chats

---

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Environment

```env
GROQ_API_KEY=your_key
DATABASE_URL=postgresql://user:pass@localhost:5432/bot_gpt
```

---

## Notes

* Stateless REST APIs
* Simple RAG (no vector DB)
* Swagger used for testing

---

