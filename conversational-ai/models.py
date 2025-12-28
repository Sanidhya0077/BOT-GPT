from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime,Index
from sqlalchemy.sql import func
from db import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    mode = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String) 
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer)
    chunk_text = Column(Text)

Index("idx_conversation_id", Message.conversation_id)
Index("idx_document_conversation", DocumentChunk.conversation_id)