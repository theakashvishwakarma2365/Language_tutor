from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from database import save_message
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def generate_conversation_streamlit(user_preferences, session_id):
    # Chat CSS Styling
    st.markdown("""
    <style>
    .chat-box {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        background-color: #1e1e1e;
        color: #fff;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .stChatMessage { border-radius: 10px; padding: 10px; margin: 5px 0; }
    .stChatMessage.user { background-color: #2e2e2e; color: white; }
    .stChatMessage.ai { background-color: #444; color: white; }
    </style>
    """, unsafe_allow_html=True)

    # Wait for Start Chat
    if "chat_started" not in st.session_state or not st.session_state.chat_started:
        st.info("Click on **Start Chat** from the sidebar to begin chatting.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(return_messages=True)

    memory = st.session_state.memory
    chat = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)

    # System Prompt
    system_message = SystemMessage(content=f"""
    You are a professional language tutor, friendly and engaging.
    Your role is to help the user learn **{user_preferences.get('learning_language', 'Spanish')}** from **{user_preferences.get('current_language', 'English')}** at a **{user_preferences.get('user_level', 'beginner')}** level.

    **Instructions:**
    - Ask one question at a time.
    - Follow the scenario: "{user_preferences.get('scenario', 'ordering food at a restaurant')}".
    - Keep the conversation immersive and centered around the scenario.
    - Avoid generic responses. Be engaging.
    - If the user struggles, simplify the response but stay on topic.
    - Give short hints on mistakes, but not overwhelming corrections.
    - Save detailed feedback for the report.
    - If user shows confidence, increase complexity gradually.

    **Levels:**
    - Beginner: Use simple sentences, repeat key phrases.
    - Intermediate: Ask follow-up questions, encourage longer replies.
    - Practice Mode: Speak natively and challenge the user.

    Always maintain a helpful and positive tone.
    """)

    # Render chat history
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Say something...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        human_message = HumanMessage(content=user_input)
        history = memory.chat_memory.messages

        try:
            response = chat.invoke([system_message, *history, human_message])
        except Exception as e:
            st.error(f"Model failed to respond: {e}")
            return

        ai_reply = response.content
        st.chat_message("ai").markdown(ai_reply)
        st.session_state.chat_history.append({"role": "ai", "content": ai_reply})

        memory.save_context({"human": human_message.content}, {"AI": ai_reply})

        # Correction prompt
        correction_prompt = SystemMessage(content=f"""
        The user is learning {user_preferences.get('learning_language', 'Spanish')}.
        - Analyze the user's message for grammar, vocabulary, or sentence structure issues.
        - If there's a mistake, provide a short, helpful hint.
        - If no correction is needed, return an empty response.
        """)
        correction_msg = chat.invoke([correction_prompt, human_message])

        # Save everything to DB
        save_message(session_id, user_input, ai_reply, correction_msg.content)

        # Display correction
        if correction_msg.content.strip():
            with st.expander("🔍 Corrections & Suggestions"):
                st.markdown(correction_msg.content)
