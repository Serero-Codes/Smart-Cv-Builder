from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import uuid

def build_cv(data):

    filename = f"cv_{uuid.uuid4().hex}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(data.get("name", "No Name"), styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("PROFESSIONAL SUMMARY", styles["Heading2"]))
    story.append(Paragraph("Generated CV content here...", styles["BodyText"]))

    doc.build(story)

    return filename