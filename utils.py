import os
import requests
from io import BytesIO
from PIL import Image

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet


# ----------------------------
# Save Story
# ----------------------------

def save_story(timestamp, story, image_prompt, video_prompt, voice_over, quiz):

    os.makedirs("generated", exist_ok=True)

    filename = f"generated/story_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:

        file.write("STORY\n\n")
        file.write(story)

        file.write("\n\n--------------------------\n\n")

        file.write("IMAGE PROMPT\n\n")
        file.write(image_prompt)

        file.write("\n\n--------------------------\n\n")

        file.write("VIDEO PROMPT\n\n")
        file.write(video_prompt)

        file.write("\n\n--------------------------\n\n")

        file.write("VOICE OVER\n\n")
        file.write(voice_over)

        file.write("\n\n--------------------------\n\n")

        file.write("QUIZ\n\n")
        file.write(quiz)

    return filename


# ----------------------------
# PDF
# ----------------------------

def create_pdf(story, image_prompt, video_prompt, voice_over, quiz, image_path=None):

    pdf_path = "generated/AI_Kids_Content.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    # Story
    content.append(Paragraph("<b>Story</b>", styles["Heading1"]))
    content.append(Paragraph(story.replace("\n", "<br/>"), styles["BodyText"]))

    # AI Image
    if image_path and os.path.exists(image_path):
        content.append(Paragraph("<b>Generated AI Image</b>", styles["Heading1"]))
        img = Image(image_path, width=350, height=350)
        content.append(img)

    # Image Prompt
    content.append(Paragraph("<b>Image Prompt</b>", styles["Heading1"]))
    content.append(Paragraph(image_prompt.replace("\n", "<br/>"), styles["BodyText"]))

    # Video Prompt
    content.append(Paragraph("<b>Video Prompt</b>", styles["Heading1"]))
    content.append(Paragraph(video_prompt.replace("\n", "<br/>"), styles["BodyText"]))

    # Voice Over
    content.append(Paragraph("<b>Voice Over</b>", styles["Heading1"]))
    content.append(Paragraph(voice_over.replace("\n", "<br/>"), styles["BodyText"]))

    # Quiz
    content.append(Paragraph("<b>Quiz</b>", styles["Heading1"]))
    content.append(Paragraph(quiz.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(content)

    return pdf_path


# ----------------------------
# Image Generation
# ----------------------------


def generate_image(prompt, api_token=None):
    print("******** generate_image() called ********")
    import requests
    from PIL import Image
    from io import BytesIO
    from urllib.parse import quote

    try:
        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        print("Request URL:", url)

        response = requests.get(url, timeout=120)

        print("Status Code:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.load()
            print("Image loaded successfully!")
            return image

        print("Response text:", response.text)
        return None

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None