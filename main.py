import streamlit as st
import uuid
from user_choice import get_user_selection_ui
from chatbot import generate_conversation_streamlit
from database import create_new_chat_table, get_all_sessions, delete_all_chat_history
from report import download_pdf_report

st.set_page_config(page_title="Language Tutor AI", layout="wide")
st.title("🧑‍🏫Language Learning Chatbot")

# Session management
if "session_id" not in st.session_state or st.button("🆕 New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.chat_started = False
    create_new_chat_table(st.session_state.session_id)

# History Button
if st.sidebar.button("View Chat History"):
    sessions = get_all_sessions()
    for session in sessions:
        with st.sidebar.expander(f"Session: {session[0]}"):
            st.write(session[1:])
            # You may replace session[1] with a custom topic if you're storing it
            topic_name = session[1] if len(session) > 1 else "chat_report"
            download_pdf_report(session_id=session[0], topic_name=topic_name)
            
if st.sidebar.checkbox("Confirm Delete All History"):
    if st.sidebar.button("Delete All History"):
        delete_all_chat_history()
        st.success("All chat history deleted.")

# User preferences selection
user_preferences = get_user_selection_ui()

# Start chat button (persists state)
if st.sidebar.button("Start Chat"):
    st.session_state.chat_started = True

# Launch chatbot if started
if st.session_state.get("chat_started"):
    generate_conversation_streamlit(user_preferences, st.session_state.session_id)
else:
    st.info("Use the **Start Chat** button in the sidebar to begin.")
