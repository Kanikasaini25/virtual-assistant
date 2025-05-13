from datetime import datetime
from backend.config import mongo_client
from typing import List,Dict

db = mongo_client.get_database("chat_history")
conversations = db.conversations  # Only for saving conversations


def save_conversation(session_id: str, user_query: str, bot_response: str):
    """Save conversation to MongoDB"""
    conversation_data = {
        "session_id": session_id,
        "user_query": user_query,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow(),
        "title": " ".join(user_query.split()[:4]),
    }
    conversations.insert_one(conversation_data)

def get_conversation_history(session_id: str, limit: int = 20) -> List[Dict[str, str]]:
    """Retrieve conversation history for a session"""
    if session_id not in conversations:
        return []

    return conversations[session_id]["messages"][-limit:]