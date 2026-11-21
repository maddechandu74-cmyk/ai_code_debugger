import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# 1. Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Page configuration
st.set_page_config(
    page_title="AI Code Debugger & Complexity Explainer",
    page_icon="🛠️",
    layout="wide",
)

st.title("🛠️ AI Code Debugger & Complexity Explainer")
st.write("Paste your code below to catch bugs, optimize logic, and inspect Big-O time and space complexity.")

# 3. User inputs
col1, col2 = st.columns([1, 2])

with col1:
    language = st.selectbox(
        "Programming Language",
        ["Python", "C", "C++", "Java", "JavaScript", "SQL"],
    )
    focus_mode = st.radio(
        "Analysis Mode",
        [
            "Full Debug + Optimization",
            "Find Bugs Only",
            "Big-O Time & Space Complexity",
        ],
    )
    error_message = st.text_input(
        "Optional Error Message",
        placeholder="e.g., IndexError: list index out of range",
    )

with col2:
    code_input = st.text_area(
        "Paste Your Code Here",
        height=260,
        placeholder="def two_sum(nums, target):\n    for i in range(len(nums)):\n        ...",
    )

analyze_btn = st.button("Analyze Code", type="primary")

# 4. Validate and call Gemini API
if analyze_btn:
    if not api_key:
        st.error("API Key not found! Add GEMINI_API_KEY to your .env file.")
    elif not code_input.strip():
        st.warning("Please paste a code snippet before clicking Analyze Code.")
    else:
        with st.spinner("Inspecting syntax, edge cases, and time complexity..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                Act as a senior software engineer and competitive programming mentor.
                Analyze the following {language} code.
                - Requested Mode: {focus_mode}
                - Error Message Provided: {error_message if error_message.strip() else "None"}

                Code:
                ```{language.lower()}
                {code_input}
                ```

                Respond clearly using Markdown with these sections:
                1. **Issues & Edge Cases Found**: Bullet points explaining any syntax errors, logical bugs, or failing edge cases (or confirm if the code is already bug-free).
                2. **Corrected / Optimized Code**: Provide the clean, working {language} code block with brief inline comments.
                3. **Complexity Breakdown**: State the **Time Complexity** and **Space Complexity** in Big-O notation with a 1–2 sentence explanation of why.
                """

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )

                st.success("Analysis Complete!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")