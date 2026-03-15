def generate_summary(data):
    name = data.get("name", "The candidate")
    role = data.get("target_role", "software engineer")
    skills_text = data.get("skills", "")

    skills = [s.strip() for s in skills_text.split(",") if s.strip()]
    top_skills = ", ".join(skills[:3]) if skills else "relevant technologies"

    return (
        f"{name} is an aspiring {role} with hands-on experience in {top_skills}. "
        f"Focused on building real-world projects, writing clean and maintainable code, "
        f"and continuously learning new tools and technologies."
    )

def generate_bullets(data):
    role = data.get("target_role", "desired role")
    skills_text = data.get("skills", "")
    skills = [s.strip() for s in skills_text.split(",") if s.strip()]

    bullets = []

    if skills:
        bullets.append(
            f"Developed projects using {', '.join(skills[:3])}, aligning solutions with {role} responsibilities."
        )

    bullets.append("Implemented best practices in version control, documentation, and testing.")
    bullets.append("Collaborated with peers to plan, build, and deliver features within deadlines.")
    bullets.append("Adapted quickly to new tools and frameworks to meet project requirements.")
    bullets.append("Focused on writing clean, readable, and reusable code for long-term maintainability.")

    return bullets
