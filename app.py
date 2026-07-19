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

st.markdown("""
# 🤖 AI Kids Content Studio

### Create AI-powered stories, image prompts, video prompts, voice-overs, and quizzes for children.

---
""")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="📖 Stories",
        value="Unlimited"
    )

with col2:
    st.metric(
        label="🖼 Image Prompts",
        value="AI Powered"
    )

with col3:
    st.metric(
        label="🎬 Video Prompts",
        value="Ready"
    )




# ----------------------------
# INPUTS
# ----------------------------

topic = st.text_input("📖 Story Topic")

age = st.selectbox(
    "👶 Child Age",
    [2, 3, 4, 5, 6, 7, 8]
)

length = st.selectbox(
    "📏 Story Length",
    ["Short", "Medium", "Long"]
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

Topic:
{topic}

Length:
{length}

Return ONLY in this format.

STORY:
(write story)

IMAGE_PROMPT:
(write a {image_style} style image prompt suitable for children)

VIDEO_PROMPT:
(write cinematic video prompt)

VOICE_OVER:
(write narration)

QUIZ:
(write 5 simple questions)
"""

    with st.spinner("Generating AI Content..."):

        response = client.chat.completions.create(
            model="tencent/hy3:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

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

    st.success("✅ Content Generated Successfully!")

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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Story",
        "🖼 Image",
        "🎬 Video Prompt",
        "🎤 Voice Over",
        "❓ Quiz"
    ])
    with tab1:
        st.subheader("📖 Story")

        st.write(story)

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

        image = generate_image(image_prompt)

        if image is not None:
            st.image(
                image,
                caption="Generated AI Image",
                width="stretch"
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
        st.write(image_prompt)

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

        st.download_button(
            "⬇ Download Voice Over",
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