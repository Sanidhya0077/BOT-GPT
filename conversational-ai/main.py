from fastapi import FastAPI, Depends,HTTPException, status
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, Conversation, Message, DocumentChunk
from llm import call_llm
from rag import chunk_text, retrieve_chunks
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pypdf.errors import PdfReadError


Base.metadata.create_all(bind=engine)

app = FastAPI(title="BOT GPT Backend")

origins = [
    "http://localhost:5173",   
    "http://localhost:3000",   
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# function to launch the db instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Depends creates a Callable function while defining a logic inside a route
# Session
@app.post("/conversations")
def create_conversation(mode: str, db: Session = Depends(get_db)):
    convo = Conversation(mode=mode)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return {"conversation_id": convo.id}

@app.post("/conversations/{cid}/messages")
def send_message(cid: int, message: str, db: Session = Depends(get_db)):
    convo = db.query(Conversation).filter_by(id=cid).first()
    if not convo:
        return {"error": "Conversation not found"}

    db.add(Message(conversation_id=cid, role="user", content=message))
    db.commit()

    history = (
    db.query(Message)
    .filter_by(conversation_id=cid)
    .order_by(Message.created_at)
    .all()
    )


    llm_messages = [{"role": m.role, "content": m.content} for m in history]

    if convo.mode == "grounded":
        chunks = db.query(DocumentChunk).filter_by(conversation_id=cid).all()
        relevant = retrieve_chunks([c.chunk_text for c in chunks], message)

        context = "\n".join(relevant)
        system_prompt = f"""
                    You are a helpful assistant.
                    Answer ONLY using the context below.
                    Context:{context}
                    """
        llm_messages.insert(0, {"role": "system", "content": system_prompt})

    reply = call_llm(llm_messages)

    db.add(Message(conversation_id=cid, role="assistant", content=reply))
    db.commit()

    return {"response": reply}

@app.get("/conversations/{cid}")
def get_conversation(cid: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter_by(conversation_id=cid).all()
    return [
        {"role": m.role, "content": m.content, "time": m.created_at}
        for m in messages
    ]

@app.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    return [
        {
            "conversation_id": c.id,
            "mode": c.mode,
            "created_at": c.created_at
        }
        for c in conversations
    ]

@app.delete("/conversations/{cid}")
def delete_conversation(cid: int, db: Session = Depends(get_db)):
    db.query(Message).filter(Message.conversation_id == cid).delete()
    db.query(DocumentChunk).filter(DocumentChunk.conversation_id == cid).delete()

    # Delete conversation
    deleted = db.query(Conversation).filter(Conversation.id == cid).delete()
    db.commit()

    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"status": "deleted"}


@app.post("/conversations/{cid}/documents")
def upload_pdf(
    cid: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    file_path = f"./{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        return {"error": "No text extracted from PDF"}

    chunks = chunk_text(text)

    for c in chunks:
        db.add(DocumentChunk(
            conversation_id=cid,
            chunk_text=c
        ))

    db.commit()
    return {"chunks_added": len(chunks)}

def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except PdfReadError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    # Log the actual error for debugging
    print(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

