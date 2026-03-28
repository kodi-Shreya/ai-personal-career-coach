import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import io

# 🔑 Add your API key here
client = OpenAI(api_key="YOUR_APIKEY")

st.set_page_config(page_title="AI Career Coach", layout="wide")

st.title("🚀 AI Personal Career Coach")

# 📄 Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

def extract_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# 🧠 Resume Section
if uploaded_file:
    pdf_file = io.BytesIO(uploaded_file.read())
    resume_text = extract_text(pdf_file)

    st.subheader("📄 Extracted Resume Text")
    st.text_area("", resume_text, height=200)

    # Resume Analysis
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            prompt = f"""
            Analyze this resume:
            - Strengths
            - Weaknesses
            - Missing skills
            - Suggestions

            Resume:
            {resume_text}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            st.subheader("🧠 Analysis")
            st.write(response.choices[0].message.content)

    # Improve Resume
    if st.button("Improve Resume"):
        with st.spinner("Improving..."):
            prompt = f"""
            Rewrite this resume in a professional ATS-friendly format:

            {resume_text}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            st.subheader("✨ Improved Resume")
            st.write(response.choices[0].message.content)

# 🎤 Mock Interview
st.subheader("🎤 Mock Interview")

role = st.text_input("Enter Role (e.g., Data Analyst)")

if st.button("Generate Questions"):
    with st.spinner("Generating..."):
        prompt = f"Ask 5 interview questions for {role}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)

# 🗺️ Roadmap Generator
st.subheader("🗺️ Career Roadmap")

target_role = st.text_input("Enter Target Role")

if st.button("Generate Roadmap"):
    with st.spinner("Creating roadmap..."):
        prompt = f"""
        Create a 3-month roadmap to become a {target_role}.
        Include weekly goals and resources.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)