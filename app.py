import os
import requests
from io import BytesIO
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from utils import generate_image, create_pdf, save_story
from gtts import gTTS
import io



# ----------------------------
# CONFIG
# ----------------------------

load_dotenv()

os.makedirs("generated", exist_ok=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not OPENROUTER_API_KEY:
    st.error("OpenRouter API Key not found!")
    st.stop()

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# ----------------------------
# PAGE SETTINGS
# ----------------------------

st.set_page_config(
    page_title="AI Kids Content Studio",
    page_icon="📚",
    layout="wide"
)
st.markdown("""
<style>

div.stButton > button {
    background: linear-gradient(90deg,#4F46E5,#7C3AED,#EC4899);
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 15px;
    border: none;
    height: 60px;
    width: 100%;
}

div.stButton > button:hover {
    box-shadow: 0 0 20px rgba(236,72,153,0.6);
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.title("🤖 AI Kids Content Studio")

st.sidebar.info("""
### ✨ Features

📖 Story Generator

🖼 Image Prompt

🎬 Video Prompt

🎤 Voice Over

❓ Quiz

---

👩‍💻 Developed by

**Deeksha M D**
""")


# ----------------------------
# TITLE
# ----------------------------


# ----------------------------
# HERO SECTION
# ----------------------------

st.markdown("""
<style>

.hero {
    background: linear-gradient(90deg,#4F46E5,#7C3AED,#EC4899);
    padding:25px;
    border-radius:18px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.hero h1{
    font-size:42px;
    margin-bottom:10px;
}

.hero p{
    font-size:18px;
}

</style>

<div class="hero">

<h1>📚 AI Kids Content Studio</h1>

<p>
Create magical stories, AI images, voice narration,
video prompts and quizzes for children ✨
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.feature-card{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    box-shadow:0 4px 12px rgba(0,0,0,0.3);
}

.feature-card h2{
    margin-bottom:10px;
}

.feature-card p{
    color:#cbd5e1;
    font-size:15px;
}

</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>📖</h2>
        <h3>Stories</h3>
        <p>Unlimited AI Stories</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>🎨</h2>
        <h3>Image Styles</h3>
        <p>8 Creative Styles</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>🌍</h2>
        <h3>Languages</h3>
        <p>5 Supported Languages</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h2>🎤</h2>
        <h3>Voice</h3>
        <p>MP3 Playback & Download</p>
    </div>
    """, unsafe_allow_html=True)



# ----------------------------
# INPUTS
# ----------------------------
st.markdown("## ✨ Create Your Story")
st.info("Fill in the details below and let AI create an amazing story for your child.")
     
topic = st.text_input("📖 Story Topic")
     
     

col1, col2 = st.columns(2)

with col1:
    age = st.selectbox(
        "👶 Child Age",
        [2, 3, 4, 5, 6, 7, 8]
    )

    image_style = st.selectbox(
        "🎨 Image Style",
        [
            "Pixar",
            "Disney",
            "Cartoon",
            "Anime",
            "Watercolor",
            "Storybook",
            "3D Render",
            "Realistic"
        ]
    )

with col2:
    length = st.selectbox(
        "📏 Story Length",
        ["Short", "Medium", "Long"]
    )

    language = st.selectbox(
        "🌍 Story Language",
        [
            "English",
            "Hindi",
            "Kannada",
            "Tamil",
            "Telugu"
        ]
    )


     
# ----------------------------
# IMAGE GENERATION
# ----------------------------

# ----------------------------
# PDF CREATION
# ----------------------------




# ----------------------------
# GENERATE BUTTON
# ----------------------------

generate = st.button(
    "🚀 Generate AI Content",
    use_container_width=True
)
if generate:

    prompt = f"""
You are an expert children's storyteller.

Create content for a {age}-year-old child.

Generate the STORY, VOICE_OVER, and QUIZ in {language}.

The IMAGE_PROMPT should always be written in English, but describe the scene in a {image_style} style suitable for children.

Topic:
{topic}

Length:
{length}

Return ONLY in this format.

STORY:
(write story)

IMAGE_PROMPT:
(write the prompt in English for a {image_style} style children's illustration)

VIDEO_PROMPT:
(write cinematic video prompt)

VOICE_OVER:
(write narration)

QUIZ:
(write 5 simple questions)
"""

    with st.spinner("Generating AI Content..."):

        progress = st.progress(0)
        status = st.empty()

        status.write("📖 Creating Story...")
        progress.progress(20)

        response = client.chat.completions.create(
            model="tencent/hy3:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
           ]
        )

        status.write("🎨 Generating Image...")
        progress.progress(50)

        status.write("🎤 Creating Voice...")
        progress.progress(75)

        status.write("📄 Preparing PDF...")
        progress.progress(90)

        status.write("✅ Done!")
        progress.progress(100)
    result = response.choices[0].message.content

    story = ""
    image_prompt = ""
    video_prompt = ""
    voice_over = ""
    quiz = ""

    try:

        story = result.split("IMAGE_PROMPT:")[0].replace("STORY:", "").strip()

        temp = result.split("IMAGE_PROMPT:")[1]

        image_prompt = temp.split("VIDEO_PROMPT:")[0].strip()

        temp = temp.split("VIDEO_PROMPT:")[1]

        video_prompt = temp.split("VOICE_OVER:")[0].strip()

        temp = temp.split("VOICE_OVER:")[1]

        voice_over = temp.split("QUIZ:")[0].strip()

        quiz = temp.split("QUIZ:")[1].strip()

    except:

        story = result

    st.balloons()

    st.success("🎉 Your magical story is ready!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_story(
        timestamp,
        story,
        image_prompt,
        video_prompt,
        voice_over,
        quiz
    )


    image = generate_image(image_prompt)
    
    image_path = None
    
    if image is not None:
        image_path = f"generated/image_{timestamp}.png"
        image.save(image_path)

    pdf_path = create_pdf(
        story,
        image_prompt,
        video_prompt,
        voice_over,
        quiz,
        image_path
    )

    st.balloons()
    st.divider()

    st.markdown("## 📚 Your Generated Content")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Story",
        "🖼 Image",
        "🎬 Video Prompt",
        "🎤 Voice Over",
        "❓ Quiz"
    ])
    with tab1:
        st.subheader("📖 Story")

        st.info("Enjoy your AI-generated story!")

        st.markdown(f"""
        <div style="
        background:#1e293b;
        padding:20px;
        border-radius:15px;
        border:1px solid #334155;
        line-height:1.8;
        font-size:17px;">
        {story}
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Story",
            story,
            file_name="story.txt"
        )

        with open(pdf_path, "rb") as pdf:
            st.download_button(
                "📄 Download Complete PDF",
                pdf,
                file_name="AI_Kids_Content.pdf",
                mime="application/pdf"
            )


    with tab2:
        st.subheader("🖼 AI Image")
        st.info("Your AI-generated illustration")

        image = generate_image(image_prompt)

        if image is not None:
            st.image(
                image,
                caption="AI Genrated Illusration",
                use_container_width=True
            )

            image_path = f"generated/image_{timestamp}.png"
            image.save(image_path)

            with open(image_path, "rb") as img:
                st.download_button(
                    "🖼 Download Image",
                    img,
                    file_name="AI_Image.png",
                    mime="image/png"
                )

        else:
            st.info("Image generation is currently unavailable.")

        st.markdown("### 📝 Image Prompt")
        st.code(image_prompt)

        st.download_button(
            "⬇ Download Image Prompt",
            image_prompt,
            file_name="image_prompt.txt"
        )


    with tab3:
        st.subheader("🎬 Video Prompt")

        st.write(video_prompt)

        st.download_button(
            "⬇ Download Video Prompt",
            video_prompt,
            file_name="video_prompt.txt"
        )


    with tab4:
        st.subheader("🎤 Voice Over")

        st.write(voice_over)

        language_codes = {
            "English": "en",
            "Hindi": "hi",
            "Kannada": "kn",
            "Tamil": "ta",
            "Telugu": "te"
        }

        tts = gTTS(
            text=voice_over,
            lang=language_codes[language]
        )

        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        st.audio(audio_buffer, format="audio/mp3")

        st.download_button(
           "⬇ Download MP3",
           data=audio_buffer.getvalue(),
           file_name="voice_over.mp3",
           mime="audio/mpeg"
    )

        st.download_button(
            "⬇ Download Voice Over Text",
             voice_over,
             file_name="voice_over.txt"
    )


    with tab5:
        st.subheader("❓ Quiz")

        st.write(quiz)

        st.download_button(
            "⬇ Download Quiz",
            quiz,
            file_name="quiz.txt"
        )