from flask import Flask, render_template, request, send_file, redirect, url_for
from resume_generator import build_resume_context, generate_pdf_resume
from ai_helpers import generate_summary, generate_bullets
import os
from datetime import datetime

app = Flask(__name__)

# simple in-memory session storage
user_sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "linkedin": request.form.get("linkedin"),
            "github": request.form.get("github"),
            "professional_summary": request.form.get("professional_summary"),
            "skills": request.form.get("skills"),
            "projects": request.form.get("projects"),
            "experience": request.form.get("experience"),
            "education": request.form.get("education"),
            "certifications": request.form.get("certifications"),
            "languages": request.form.get("languages"),
            "target_role": request.form.get("target_role"),
        }

        session_id = str(datetime.now().timestamp())
        user_sessions[session_id] = data

        # default template: professional
        return redirect(url_for("preview", session_id=session_id, template="professional"))

    return render_template("form.html")

@app.route("/preview/<session_id>")
def preview(session_id):
    if session_id not in user_sessions:
        return "Session not found", 404

    template_type = request.args.get("template", "professional")
    data = user_sessions[session_id]

    resume_ctx = build_resume_context(data, template_type)
    summary = generate_summary(data)
    bullets = generate_bullets(data)

    # inject AI summary if user did not provide
    if not resume_ctx["professional_summary"]:
        resume_ctx["professional_summary"] = summary

    return render_template(
        "preview.html",
        session_id=session_id,
        resume=resume_ctx,
        bullets=bullets,
        template_type=template_type,
    )

@app.route("/download/<session_id>")
def download(session_id):
    if session_id not in user_sessions:
        return "Session not found", 404

    template_type = request.args.get("template", "professional")
    data = user_sessions[session_id]
    resume_ctx = build_resume_context(data, template_type)
    summary = generate_summary(data)
    if not resume_ctx["professional_summary"]:
        resume_ctx["professional_summary"] = summary

    pdf_path = generate_pdf_resume(resume_ctx, template_type)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{resume_ctx['name'].replace(' ', '_')}_{template_type}.pdf",
    )

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(debug=True, port=5000)
