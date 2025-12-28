Developer setup

This project uses a local virtual environment created in the project root (`conversational-ai`).

Quick start (PowerShell):

1. Activate the venv:

   .\Scripts\Activate.ps1

2. Install dependencies (already listed in `requirements.txt`):

   .\Scripts\pip.exe install -r requirements.txt

3. Run the FastAPI app (from project root):

   .\Scripts\python.exe -m uvicorn main:app --reload

Notes

- If your editor (e.g. VS Code) doesn't resolve imports, point the Python interpreter to:
  `c:\Users\pc\Downloads\Bot-consulting-Assignment\conversational-ai\Scripts\python.exe`.
- The `requirements.txt` contains the packages the project expects (fastapi, uvicorn, python-dotenv, sqlalchemy, groq, pydantic).
- `llm.py` expects the `GROQ_API_KEY` environment variable; add it to your system env or a `.env` file in the project root.
