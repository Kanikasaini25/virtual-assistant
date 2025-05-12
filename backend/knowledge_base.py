import os

from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector
from backend.config import PDF_PATH, PG_DB_URL, TABLE_NAME
def initialize_knowledge_base():
    """Initialize and return the knowledge base"""
    embedder = OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"))

    return PDFKnowledgeBase(
        path=PDF_PATH,
        vector_db=PgVector(
            table_name=TABLE_NAME,
            db_url=PG_DB_URL,
        ),
        embedding_model=embedder,
    )



knowledge_base = initialize_knowledge_base()
knowledge_base.load(upsert=False)
