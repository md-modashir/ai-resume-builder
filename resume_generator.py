from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import os
from datetime import datetime

def split_lines(text):
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]

def split_comma(text):
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]

def build_resume_context(data, template_type="professional"):
    ctx = {
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "linkedin": data.get("linkedin", ""),
        "github": data.get("github", ""),
        "professional_summary": data.get("professional_summary", ""),
        "skills": split_comma(data.get("skills", "")),
        "projects": split_lines(data.get("projects", "")),
        "experience": split_lines(data.get("experience", "")),
        "education": split_lines(data.get("education", "")),
        "certifications": split_lines(data.get("certifications", "")),
        "languages": split_comma(data.get("languages", "")),
        "template_type": template_type,
    }

    if template_type == "basic":
        ctx["template_config"] = {
            "show_certifications": False,
            "show_languages": False,
            "max_projects": 3,
        }
    elif template_type == "moderate":
        ctx["template_config"] = {
            "show_certifications": True,
            "show_languages": True,
            "max_projects": 4,
        }
    else:  # professional
        ctx["template_config"] = {
            "show_certifications": True,
            "show_languages": True,
            "max_projects": 6,
        }
    return ctx

def generate_pdf_resume(resume_ctx, template_type):
    os.makedirs("downloads", exist_ok=True)
    filename = os.path.join(
        "downloads",
        f"{resume_ctx['name'].replace(' ', '_')}_{template_type}_{int(datetime.now().timestamp())}.pdf",
    )

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor("#222222"),
    )
    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=colors.HexColor("#555555"),
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=colors.HexColor("#2c3e50"),
    )
    text_style = ParagraphStyle(
        "Text",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_JUSTIFY,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        leftIndent=15,
    )

    story = []

    # Header
    story.append(Paragraph(resume_ctx["name"], name_style))
    contact_parts = []
    if resume_ctx["email"]:
        contact_parts.append(resume_ctx["email"])
    if resume_ctx["phone"]:
        contact_parts.append(resume_ctx["phone"])
    if resume_ctx["linkedin"]:
        contact_parts.append(resume_ctx["linkedin"])
    if resume_ctx["github"]:
        contact_parts.append(resume_ctx["github"])
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), contact_style))
    story.append(Spacer(1, 0.2 * inch))

    # Summary
    if resume_ctx["professional_summary"]:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
        story.append(Paragraph(resume_ctx["professional_summary"], text_style))
        story.append(Spacer(1, 0.15 * inch))

    # Skills
    if resume_ctx["skills"]:
        story.append(Paragraph("TECHNICAL SKILLS", section_style))
        story.append(Paragraph(", ".join(resume_ctx["skills"]), text_style))
        story.append(Spacer(1, 0.15 * inch))

    # Experience
    if resume_ctx["experience"]:
        story.append(Paragraph("EXPERIENCE", section_style))
        for exp in resume_ctx["experience"]:
            story.append(Paragraph(f"• {exp}", bullet_style))
        story.append(Spacer(1, 0.15 * inch))

    # Projects
    if resume_ctx["projects"]:
        story.append(Paragraph("PROJECTS", section_style))
        max_projects = resume_ctx["template_config"]["max_projects"]
        for proj in resume_ctx["projects"][:max_projects]:
            story.append(Paragraph(f"• {proj}", bullet_style))
        story.append(Spacer(1, 0.15 * inch))

    # Education
    if resume_ctx["education"]:
        story.append(Paragraph("EDUCATION", section_style))
        for edu in resume_ctx["education"]:
            story.append(Paragraph(f"• {edu}", bullet_style))
        story.append(Spacer(1, 0.15 * inch))

    # Certifications
    if resume_ctx["template_config"]["show_certifications"] and resume_ctx["certifications"]:
        story.append(Paragraph("CERTIFICATIONS", section_style))
        for cert in resume_ctx["certifications"]:
            story.append(Paragraph(f"• {cert}", bullet_style))
        story.append(Spacer(1, 0.15 * inch))

    # Languages
    if resume_ctx["template_config"]["show_languages"] and resume_ctx["languages"]:
        story.append(Paragraph("LANGUAGES", section_style))
        story.append(Paragraph(", ".join(resume_ctx["languages"]), text_style))

    doc.build(story)
    return filename
