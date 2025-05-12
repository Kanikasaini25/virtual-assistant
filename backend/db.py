from datetime import datetime
from typing import Dict, List

from backend.config import mongo_client

db = mongo_client.get_database("chat_history")
conversations = db.conversations  # Only for saving conversations
def save_conversation(session_id: str, user_query: str, bot_response: str):
    """Save conversation to MongoDB"""
    conversation_data = {
        "session_id": session_id,
        "user_query": user_query,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow(),
        "title": " ".join(user_query.split()[:4]),  # First 4 words as title
    }
    conversations.insert_one(conversation_data)
