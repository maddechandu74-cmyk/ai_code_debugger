import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

st.set_page_config(page_title="AI Study Buddy (Notes to Quiz)", page_icon="📚", layout="wide")

st.title("📚 AI Study Buddy (Notes to Quiz)")
st.markdown("Paste your lecture notes or study material below to generate practice quizzes, flashcards, and key takeaways.")

col1, col2 = st.columns([1, 1])

with col1:
    subject = st.text_input("Subject / Topic (Optional)", placeholder="e.g., Data Structures - Binary Trees")
    num_questions = st.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5)
    difficulty = st.radio(
        "Difficulty Level",
        ["Easy (Recall & Definitions)", "Medium (Conceptual & Application)", "Hard (Exam-Level Problem Solving)"]
    )
    notes = st.text_area(
        "Paste Your Study Notes Here",
        height=240,
        placeholder="Paste your lecture notes, textbook summary, or topic concepts here..."
    )
    generate_btn = st.button("Generate Quiz & Study Guide", type="primary")

with col2:
    st.subheader("Generated Quiz & Study Material")
    if generate_btn:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("API Key not found! Add GEMINI_API_KEY to your .env file or Streamlit Secrets.")
        elif not notes.strip():
            st.warning("Please paste some study notes first.")
        else:
            prompt = f"""You are an expert academic tutor and study buddy.
Subject/Topic: {subject if subject.strip() else "General Study Material"}
Difficulty: {difficulty}
Number of Questions: {num_questions}

Based ONLY on the following student notes, create a well-structured study guide with:
1. **Key Takeaways (Bullet Summary)**: Concise summary of the core concepts.
2. **Practice Quiz ({num_questions} Questions)**: Multiple-choice questions (A, B, C, D) tailored to {difficulty} level.
3. **Answer Key & Explanations**: Provide the correct option and a brief explanation for each question.

Student Notes:
{notes}
"""
            with st.spinner("Creating your custom quiz and study summary..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                    )
                    st.markdown(response.text)
                except errors.APIError as e:
                    st.error(f"API Error: {e.message}. Please try again in a few seconds.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")