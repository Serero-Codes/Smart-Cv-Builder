import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors

def generate_ats_cv(data):
    buffer = io.BytesIO()
    
    # Professional Margins (0.5 inch)
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    # Elite Typography Styles
    name_style = ParagraphStyle('Name', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, alignment=TA_CENTER, spaceAfter=2)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=TA_CENTER, spaceAfter=10, textColor=colors.darkgrey)
    section_heading = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=4, spaceBefore=12, textTransform='uppercase')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, spaceAfter=4, leading=14)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=10, spaceAfter=4, leading=14, leftIndent=15, firstLineIndent=-10)
    
    # Helper for bolding text
    def bold(text): return f"<b>{text}</b>" if text else ""
    def italic(text): return f"<i>{text}</i>" if text else ""

    flowables = []

    # --- 1. HEADER ---
    flowables.append(Paragraph(str(data.get('name', 'NAME NOT PROVIDED')).upper(), name_style))
    
    contact_info = []
    if data.get('email'): contact_info.append(data.get('email'))
    if data.get('phone'): contact_info.append(data.get('phone'))
    if data.get('links'): contact_info.append(data.get('links'))
    flowables.append(Paragraph(" | ".join(contact_info), contact_style))

    def add_section_header(title):
        flowables.append(Paragraph(title, section_heading))
        flowables.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8, spaceBefore=2))

    # --- 2. SUMMARY ---
    if data.get('summary'):
        add_section_header("Professional Summary")
        flowables.append(Paragraph(str(data.get('summary')), body_style))

    # --- 3. SKILLS ---
    if data.get('skills'):
        add_section_header("Technical Skills")
        flowables.append(Paragraph(str(data.get('skills')), body_style))

    # --- 4. EXPERIENCE ---
    experience = data.get('experience', [])
    if experience and isinstance(experience, list):
        add_section_header("Professional Experience")
        for exp in experience:
            # Table for Role (Left) and Date (Right)
            role_company = f"{bold(exp.get('role'))} | {exp.get('company')}"
            date_str = exp.get('duration', '')
            
            tbl_data = [[Paragraph(role_company, body_style), Paragraph(date_str, ParagraphStyle('Right', parent=body_style, alignment=TA_RIGHT))]]
            tbl = Table(tbl_data, colWidths=[doc.width - 100, 100])
            tbl.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 0), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
            flowables.append(tbl)
            
            # Bullets
            bullets = exp.get('bullets', [])
            if isinstance(bullets, list):
                for bullet in bullets:
                    flowables.append(Paragraph(f"• {bullet}", bullet_style))
            flowables.append(Spacer(1, 6))

    # --- 5. PROJECTS ---
    projects = data.get('projects', [])
    if projects and isinstance(projects, list):
        add_section_header("Technical Projects")
        for proj in projects:
            proj_header = f"{bold(proj.get('name'))} | <i>{proj.get('tech', '')}</i>"
            flowables.append(Paragraph(proj_header, body_style))
            
            bullets = proj.get('bullets', [])
            if isinstance(bullets, list):
                for bullet in bullets:
                    flowables.append(Paragraph(f"• {bullet}", bullet_style))
            flowables.append(Spacer(1, 6))

    # --- 6. EDUCATION ---
    education = data.get('education', [])
    if education and isinstance(education, list):
        add_section_header("Education")
        for edu in education:
            edu_left = f"{bold(edu.get('degree'))} - {edu.get('school')}"
            edu_right = edu.get('year', '')
            
            tbl_data = [[Paragraph(edu_left, body_style), Paragraph(edu_right, ParagraphStyle('Right', parent=body_style, alignment=TA_RIGHT))]]
            tbl = Table(tbl_data, colWidths=[doc.width - 100, 100])
            tbl.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 0), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
            flowables.append(tbl)

    doc.build(flowables)
    buffer.seek(0)
    return buffer