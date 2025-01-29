import streamlit as st
from supabase import create_client
import time

# Connect to Supabase (we'll add secrets later)
SUPABASE_URL = st.secrets.SUPABASE_URL  # Direct string access
SUPABASE_KEY = st.secrets.SUPABASE_KEY
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set up the app
st.title("💬 Group Chat App")

# Ask user for their name
if "user_name" not in st.session_state:
    user_name = st.text_input("Enter your name to join the chat:")
    if user_name:
        st.session_state.user_name = user_name
        st.rerun()  # Refresh to show chat

# If user has entered their name, show the chat
else:
    st.write(f"Welcome, {st.session_state.user_name}! 🎉")

    # Display messages
    def show_messages():
        messages = supabase.table("messages").select("*").order("created_at").execute()
        for msg in messages.data:
            st.write(f"👤 **{msg['user_name']}**: {msg['message']}")

    show_messages()

    # Send messages
    user_input = st.chat_input("Type a message...")
    if user_input:
        supabase.table("messages").insert({
            "user_name": st.session_state.user_name,
            "message": user_input
        }).execute()
        st.rerun()  # Refresh to show new message

    # Auto-refresh every 3 seconds
    time.sleep(3)
    st.rerun()
