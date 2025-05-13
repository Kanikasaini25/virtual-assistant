import streamlit as st

from chatbot import generate_session_id, get_recipe_recommendation_stream

st.set_page_config(page_title="Indian Recipe Recommender", layout="centered")
st.title("🍛 Indian Recipe Recommender")

# Initialize session
if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("### Options")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.session_id = generate_session_id()
        st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
query = st.chat_input("Enter ingredients or dish name...")

if query:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for chunk in get_recipe_recommendation_stream(
            st.session_state.session_id, query, st.session_state.chat_history
        ):
            if isinstance(chunk, dict) and "message" in chunk:
                st.error(chunk["message"])
                break

            full_response += chunk
            response_placeholder.markdown(full_response)

        if full_response:
            st.session_state.chat_history.append(
                {"role": "assistant", "content": full_response}
            )
