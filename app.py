import streamlit as st
from transcript_fetcher import fetch_transcript
from summarizer import generate_summary, generate_timestamps, answer_question

st.set_page_config(page_title="BrieflyTube", layout="wide")
st.title("🎥 BrieflyTube – Summarize & Chat with YouTube Videos")

# Store summary, timestamps, and answer so they don’t vanish
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "timestamps" not in st.session_state:
    st.session_state.timestamps = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

video_url = st.text_input("Paste a YouTube Video Link:")

if video_url:
    with st.spinner("Fetching transcript..."):
        transcript = fetch_transcript(video_url)

    if "Error" in transcript or "Invalid" in transcript:
        st.error(transcript)
    else:
        st.success("Transcript fetched successfully!")

        # Summary + Timestamps Section
        if st.button("Generate Summary & Timestamps"):
            with st.spinner("Talking to Gemini..."):
                summary = generate_summary(transcript)
                timestamps = generate_timestamps(transcript)

            st.session_state.summary = summary
            st.session_state.timestamps = timestamps

        # Summary Section
        if st.session_state.summary:
            with st.expander("🧠 Summary", expanded=True):
                st.markdown(st.session_state.summary)
                if not st.session_state.summary.startswith("❌"):
                    st.download_button(
                        label="📥 Download Summary as .txt",
                        data=st.session_state.summary.encode('utf-8'),
                        file_name="video_summary.txt",
                        mime="text/plain"
                    )

        # Timestamps Section
        if st.session_state.timestamps:
            with st.expander("⏱️ Key Timestamps", expanded=False):
                st.markdown(st.session_state.timestamps)

        # Q&A Section
        with st.expander("❓ Ask a question about the video", expanded=False):
            user_question = st.text_input("Type your question here", key="user_question")

            if st.button("Get Answer"):
                if user_question.strip() == "":
                    st.warning("Please enter a question first 💡")
                else:
                    with st.spinner("Thinking..."):
                        answer = answer_question(transcript, user_question)
                    st.session_state.answer = answer

            if st.session_state.answer:
                st.success("Answer:")
                st.markdown(st.session_state.answer)
                if not st.session_state.answer.startswith("❌"):
                    st.download_button(
                        label="📥 Download Answer as .txt",
                        data=st.session_state.answer.encode('utf-8'),
                        file_name="video_answer.txt",
                        mime="text/plain"
                    )
