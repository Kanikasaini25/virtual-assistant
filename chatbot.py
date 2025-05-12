import os
import time
import uuid
from typing import Any, Dict, Generator, List, Union

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from openai import OpenAI

from backend.config import LLM_MODEL_ID
from backend.db import save_conversation
from backend.knowledge_base import knowledge_base

openai_client = OpenAI()

csv_agent = Agent(
    knowledge=knowledge_base,
    model=OpenAIChat(id=LLM_MODEL_ID, temperature=0.3),
    role="Indian Recipe Assistant",
    description="A friendly assistant that helps users discover and cook Indian recipes based on ingredients, cuisine, and dish type.",
    instructions="""
        You are a warm, friendly Indian Recipe Assistant. Your job is to:
        - Greet the user when they greet you, like a human would (e.g., respond to 'hi', 'hello', 'good morning').
        - Engage in light small talk when appropriate, keeping things polite and brief.
        - Primarily help users by answering their food-related questions based on the recipe dataset.
        - When a user asks about Indian recipes, search the knowledge base and provide:
            - The recipe name
            - Key ingredients
            - Step-by-step preparation method
            - Any cultural or regional notes if relevant
        - If a recipe is not found, kindly inform the user and suggest they try rephrasing.
        - Always respond in a friendly and conversational tone, like you're chatting with someone in your kitchen.
        - Format responses using markdown.
    """,
    search_knowledge=True,
    add_context=True,
    markdown=True,
    add_references=True,
    references_format="yaml",
    structured_outputs=True,
)

def generate_session_id() -> str:
    """Generate a new session ID"""
    return str(uuid.uuid4())

def count_tokens(text: str):
    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL_ID,
            messages=[{"role": "user", "content": text}],
            max_tokens=1,
        )
        return response.usage.prompt_tokens
    except Exception as e:
        print(f"Error counting tokens: {e}")
        return len(text.split())


def get_recipe_recommendation_stream(
    session_id: str, query: str, chat_history: List[Dict[str, str]]
) -> Generator[Union[str, Dict[str, Any]], None, None]:
    try:
        start = time.time()

        if not query.strip():
            yield {"message": "Error: Query cannot be empty."}
            return

        token_count = count_tokens(query)
        print(f"Token count: {token_count}")

        MAX_TOKENS = 8192
        if token_count > MAX_TOKENS:
            yield {"message": f"Error: Query exceeds {MAX_TOKENS} token limit."}
            return

        messages = [
            {"role": "system", "content": csv_agent.instructions},
            *chat_history[-2:],
            {"role": "user", "content": query},
        ]

        stream = openai_client.chat.completions.create(
            model=LLM_MODEL_ID, messages=messages, stream=True, temperature=0.3
        )

        assistant_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                assistant_response += content
                yield content

        save_conversation(session_id, query, assistant_response)
        print(f"Response generated in {time.time() - start:.2f}s")

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        yield {"message": f"Error: {str(e)}"}
