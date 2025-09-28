# app.py
import streamlit as st
from Bac import (
    analyze_mood,
    generate_fitness_plan,
    voice_guided_meditation,
    set_reminder,
    show_progress,
    query_gemma2,
    progress,
    check_in,
    check_out,
    attendance_log,
    classify_request,
)

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="Wellness Assistant", page_icon="💬", layout="wide")
st.title("💬 Wellness Assistant Chatbot")
st.write("Your personal assistant for mood tracking, fitness, meditation, HR requests, and reminders.")

# Sidebar
st.sidebar.title("⚡ Wellness Assistant")
st.sidebar.write("Built for CodeFusion Hackathon 2025 🎉")
st.sidebar.success("Features: Mood, Fitness, Meditation, Reminders, Attendance, HR Requests, Progress")

# Role selection
role = st.sidebar.radio("Select Role:", ["User", "Admin"])

# ----------------------------
# Session State (for chat history)
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# User Input
# ----------------------------
if role == "User":
    user_input = st.text_input("Type your message here 👇")

    if st.button("Send") and user_input:
        request_type = classify_request(user_input)

        if "mood" in user_input.lower():
            reply = analyze_mood(user_input)

        elif "fitness" in user_input.lower():
            reply = generate_fitness_plan(user_input)

        elif "meditate" in user_input.lower():
            reply, audio_file = voice_guided_meditation()
            with open(audio_file, "rb") as f:
                st.audio(f.read(), format="audio/mp3")

        elif "remind" in user_input.lower():
            reply = set_reminder("Take medicine", "8 PM")

        elif "progress" in user_input.lower():
            labels, values = show_progress()
            st.bar_chart({"Activities": values})
            reply = "📊 Here’s your progress."

        elif "check-in" in user_input.lower():
            reply = check_in("Employee")

        elif "check-out" in user_input.lower():
            reply = check_out("Employee")

        elif request_type == "leave":
            reply = "📌 Leave request recorded. Pending approval."
        elif request_type == "travel":
            reply = "✈️ Travel request noted. Please attach details."
        elif request_type == "resignation":
            reply = "⚠️ Resignation request forwarded to HR."
        elif request_type == "expense":
            reply = "💰 Expense reimbursement request logged."
        else:
            reply = query_gemma2(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", reply))

    # Display Chat History
    st.subheader("Chat History")
    for role_chat, msg in st.session_state.chat_history:
        if role_chat == "You":
            st.markdown(f"**👤 {role_chat}:** {msg}")
        else:
            st.markdown(f"**🤖 {role_chat}:** {msg}")

# ----------------------------
# Admin View
# ----------------------------
if role == "Admin":
    st.subheader("📊 Admin Dashboard")

    if attendance_log:
        st.write("### Attendance Log")
        st.table(attendance_log)
    else:
        st.info("No attendance records yet.")

    st.write("### Progress Overview")
    labels, values = show_progress()
    st.bar_chart({"Mood": [len(progress["mood"])],
                  "Fitness": [len(progress["fitness"])],
                  "Meditation": [len(progress["meditation"])]})
