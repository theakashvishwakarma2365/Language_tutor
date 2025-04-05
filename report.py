from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import streamlit as st
from database import get_chat

def download_pdf_report(session_id, topic_name="chat_report"):
    chat_data = get_chat(session_id)
    if not chat_data:
        st.warning("No data found for this session.")
        return

    sanitized_topic = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in topic_name)
    file_path = f"{sanitized_topic.replace(' ', '_')}.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Language Learning Chatbot Report")
    y -= 30

    c.setFont("Helvetica", 12)

    for msg in chat_data:
        user_msg = f"User: {msg[1]}"
        ai_msg = f"AI: {msg[2]}"
        correction_msg = f"Corrections: {msg[3]}"

        for line in [user_msg, ai_msg, correction_msg, "----------------------------------------"]:
            lines = split_text(line, width - 2 * margin, c)
            for sub_line in lines:
                if y < margin:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = height - margin
                c.drawString(margin, y, sub_line)
                y -= 15
        y -= 10

    c.save()

    with open(file_path, "rb") as f:
        st.download_button(
            label=f"Download '{sanitized_topic}' Report as PDF",
            data=f,
            file_name=file_path,
            mime="application/pdf",
            key=f"download_{session_id}"
)

# Helper to wrap lines
def split_text(text, max_width, canvas_obj):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + " " + word if line else word
        if canvas_obj.stringWidth(test_line, "Helvetica", 12) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines
