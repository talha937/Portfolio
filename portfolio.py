"""
╔══════════════════════════════════════════════════════════════╗
║            PROFESSIONAL PORTFOLIO — Flask App                ║
║  Designed to impress recruiters at Google, Meta, Microsoft   ║
║  Edit config.json to update all content & theming.           ║
╚══════════════════════════════════════════════════════════════╝
"""
import json, os, webbrowser, threading
from flask import Flask, render_template_string, send_from_directory, jsonify

# ─── Load config ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

app = Flask(__name__)

# ─── Serve uploaded images from /static folder ──────────────
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

# ─── API endpoint to reload config (live refresh) ───────────
@app.route("/api/config")
def api_config():
    return jsonify(load_config())

# ─── Main page ──────────────────────────────────────────────
@app.route("/")
def index():
    cfg = load_config()
    # Pre-compute values that are tricky in Jinja2
    total_tech = sum(len(s["items"]) for s in cfg.get("skills", []))
    project_categories = list(dict.fromkeys(p["category"] for p in cfg.get("projects", [])))
    return render_template_string(
        HTML_TEMPLATE, cfg=cfg, json_data=json.dumps(cfg),
        total_tech=total_tech, project_categories=project_categories
    )


# ═══════════════════════════════════════════════════════════
#  FULL HTML / CSS / JS TEMPLATE
# ═══════════════════════════════════════════════════════════

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ cfg.meta.title }}</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{{ cfg.meta.favicon }}</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family={{ cfg.theme.font_heading }}:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        /* ════════════════ CSS VARIABLES (from config) ════════════════ */
        :root {
            --primary: {{ cfg.theme.primary_color }};
            --secondary: {{ cfg.theme.secondary_color }};
            --accent: {{ cfg.theme.accent_color }};
            --dark-bg: {{ cfg.theme.dark_bg }};
            --card-bg: {{ cfg.theme.card_bg }};
            --text: {{ cfg.theme.text_color }};
            --heading: {{ cfg.theme.heading_color }};
            --grad-start: {{ cfg.theme.gradient_start }};
            --grad-end: {{ cfg.theme.gradient_end }};
            --font: '{{ cfg.theme.font_heading }}', system-ui, -apple-system, sans-serif;
            --radius: 16px;
            --transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        /* ════════════════ RESET & BASE ════════════════ */
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        html { scroll-behavior: smooth; scroll-padding-top: 80px; }
        body {
            font-family: var(--font);
            background: var(--dark-bg);
            color: var(--text);
            line-height: 1.7;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }
        ::selection { background: var(--primary); color: #fff; }
        a { color: inherit; text-decoration: none; }
        img { max-width: 100%; display: block; }

        /* ════════════════ ANIMATED BACKGROUND ════════════════ */
        .bg-grid {
            position: fixed; inset: 0; z-index: -2;
            background-image:
                radial-gradient(circle at 1px 1px, rgba(255,255,255,0.03) 1px, transparent 0);
            background-size: 40px 40px;
        }
        .bg-glow {
            position: fixed; z-index: -1; border-radius: 50%;
            filter: blur(120px); opacity: 0.15; pointer-events: none;
        }
        .bg-glow-1 { width:600px; height:600px; top:-100px; left:-100px; background:var(--primary); animation: float 20s ease-in-out infinite; }
        .bg-glow-2 { width:500px; height:500px; bottom:-50px; right:-100px; background:var(--secondary); animation: float 25s ease-in-out infinite reverse; }
        .bg-glow-3 { width:400px; height:400px; top:50%; left:50%; transform:translate(-50%,-50%); background:var(--accent); animation: float 30s ease-in-out infinite; }
        @keyframes float {
            0%,100% { transform: translate(0,0) scale(1); }
            25% { transform: translate(30px,-40px) scale(1.05); }
            50% { transform: translate(-20px,30px) scale(0.95); }
            75% { transform: translate(40px,20px) scale(1.03); }
        }

        /* ════════════════ CURSOR FOLLOWER ════════════════ */
        .cursor-glow {
            position: fixed; width:300px; height:300px; border-radius:50%;
            background: radial-gradient(circle, rgba(108,99,255,0.08), transparent 70%);
            pointer-events:none; z-index:0; transition: transform 0.15s ease-out;
            transform: translate(-50%,-50%);
        }

        /* ════════════════ NAVBAR ════════════════ */
        .navbar {
            position: fixed; top:0; left:0; right:0; z-index:1000;
            padding: 0 40px; height: 72px;
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(10,10,26,0.7);
            backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid rgba(255,255,255,0.06);
            transition: var(--transition);
        }
        .navbar.scrolled { background: rgba(10,10,26,0.95); box-shadow: 0 4px 30px rgba(0,0,0,0.3); }
        .nav-logo {
            font-size: 1.4rem; font-weight: 800;
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .nav-links { display:flex; gap:8px; align-items:center; }
        .nav-links a {
            padding: 8px 16px; border-radius: 8px; font-size: 0.88rem;
            font-weight: 500; color: var(--text); transition: var(--transition);
            position: relative;
        }
        .nav-links a:hover, .nav-links a.active {
            color: var(--primary); background: rgba(108,99,255,0.1);
        }
        .nav-cta {
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end)) !important;
            color: #fff !important; font-weight: 600 !important;
            padding: 10px 24px !important; border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(108,99,255,0.3);
        }
        .nav-cta:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(108,99,255,0.4); }
        .hamburger { display:none; flex-direction:column; gap:5px; cursor:pointer; padding:10px; }
        .hamburger span { width:24px; height:2px; background:var(--text); transition:var(--transition); border-radius:2px; }
        .hamburger.active span:nth-child(1) { transform: rotate(45deg) translate(5px,5px); }
        .hamburger.active span:nth-child(2) { opacity:0; }
        .hamburger.active span:nth-child(3) { transform: rotate(-45deg) translate(5px,-5px); }

        /* ════════════════ HERO ════════════════ */
        .hero {
            min-height: 100vh; display: flex; align-items: center;
            padding: 120px 40px 80px;
            position: relative;
        }
        .hero-content { max-width: 1200px; margin: 0 auto; width: 100%; }
        .hero-badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 8px 20px; border-radius: 50px;
            background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.2);
            font-size: 0.85rem; font-weight: 500; color: var(--primary);
            margin-bottom: 24px; animation: fadeInUp 0.8s ease;
        }
        .hero-badge .pulse { width:8px; height:8px; border-radius:50%; background:#4ade80; animation: pulse 2s ease-in-out infinite; }
        @keyframes pulse { 0%,100%{ opacity:1; transform:scale(1); } 50%{ opacity:0.5; transform:scale(1.5); }}
        .hero h1 {
            font-size: clamp(2.8rem, 6vw, 5rem); font-weight: 800;
            line-height: 1.1; color: var(--heading);
            margin-bottom: 8px; letter-spacing: -2px;
            animation: fadeInUp 0.8s ease 0.1s both;
        }
        .hero .gradient-text {
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end), var(--secondary));
            background-size: 200% 200%; animation: gradientShift 5s ease infinite;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        @keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
        .hero-subtitle {
            font-size: clamp(1rem,2vw,1.25rem); color: var(--text);
            max-width: 600px; margin: 20px 0 36px; opacity: 0.8;
            animation: fadeInUp 0.8s ease 0.2s both;
        }
        .hero-actions {
            display: flex; gap: 16px; flex-wrap: wrap;
            animation: fadeInUp 0.8s ease 0.3s both;
        }
        .btn {
            padding: 14px 32px; border-radius: 12px; font-size: 0.95rem;
            font-weight: 600; cursor: pointer; border: none;
            display: inline-flex; align-items: center; gap: 10px;
            transition: var(--transition); font-family: var(--font);
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end));
            color: #fff; box-shadow: 0 4px 20px rgba(108,99,255,0.3);
        }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(108,99,255,0.45); }
        .btn-outline {
            background: transparent; color: var(--text);
            border: 1.5px solid rgba(255,255,255,0.15);
        }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); background: rgba(108,99,255,0.05); }
        .hero-stats {
            display: flex; gap: 48px; margin-top: 60px;
            animation: fadeInUp 0.8s ease 0.4s both;
        }
        .stat-item { text-align: left; }
        .stat-number {
            font-size: 2rem; font-weight: 800; color: var(--heading);
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .stat-label { font-size: 0.85rem; color: var(--text); opacity: 0.6; margin-top: 4px; }
        .hero-scroll {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            display: flex; flex-direction: column; align-items: center; gap: 8px;
            color: var(--text); opacity: 0.4; font-size: 0.8rem;
            animation: bounce 2s ease-in-out infinite;
        }
        @keyframes bounce { 0%,100%{transform:translateX(-50%) translateY(0)} 50%{transform:translateX(-50%) translateY(10px)} }

        /* ════════════════ SECTIONS ════════════════ */
        section { padding: 100px 40px; max-width: 1200px; margin: 0 auto; }
        .section-header { text-align:center; margin-bottom:64px; }
        .section-label {
            display: inline-block; padding: 6px 16px; border-radius: 50px;
            background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.15);
            font-size: 0.8rem; font-weight: 600; color: var(--primary);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px;
        }
        .section-title {
            font-size: clamp(2rem,4vw,2.8rem); font-weight: 800;
            color: var(--heading); letter-spacing: -1px; margin-bottom: 16px;
        }
        .section-desc { color: var(--text); opacity:0.7; max-width:600px; margin:0 auto; font-size:1.05rem; }

        /* ════════════════ ABOUT ════════════════ */
        .about-grid { display:grid; grid-template-columns:1fr 1fr; gap:64px; align-items:center; }
        .about-image-wrapper {
            position:relative; display:flex; justify-content:center; align-items:center;
        }
        .about-image-frame {
            width:350px; height:350px; border-radius: 24px; overflow:hidden;
            border: 2px solid rgba(108,99,255,0.2);
            background: linear-gradient(135deg, rgba(108,99,255,0.1), rgba(0,210,255,0.1));
            display:flex; align-items:center; justify-content:center;
            position:relative;
        }
        .about-image-frame::before {
            content:''; position:absolute; inset:-2px; border-radius:26px;
            background: linear-gradient(135deg, var(--grad-start), var(--grad-end));
            z-index:-1; opacity:0.5;
        }
        .about-image-placeholder {
            font-size: 8rem; opacity: 0.3;
        }
        .about-image-frame img { width:100%; height:100%; object-fit:cover; }
        .about-text h3 { font-size:1.6rem; font-weight:700; color:var(--heading); margin-bottom:20px; }
        .about-text p { margin-bottom:24px; opacity:0.8; font-size:1.05rem; }
        .about-tags { display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }
        .about-tag {
            padding:6px 16px; border-radius:50px;
            background:rgba(108,99,255,0.08); border:1px solid rgba(108,99,255,0.15);
            font-size:0.82rem; font-weight:500; color:var(--primary);
        }

        /* ════════════════ SKILLS ════════════════ */
        .skills-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:24px; }
        .skill-card {
            padding:32px; border-radius:var(--radius);
            background: var(--card-bg);
            border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px);
            transition: var(--transition);
        }
        .skill-card:hover {
            border-color:rgba(108,99,255,0.2);
            transform:translateY(-4px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .skill-card-header { display:flex; align-items:center; gap:12px; margin-bottom:24px; }
        .skill-card-icon { font-size:1.8rem; }
        .skill-card-title { font-size:1.1rem; font-weight:700; color:var(--heading); }
        .skill-item { margin-bottom:16px; }
        .skill-info { display:flex; justify-content:space-between; margin-bottom:6px; }
        .skill-name { font-size:0.9rem; font-weight:500; }
        .skill-pct { font-size:0.82rem; color:var(--primary); font-weight:600; }
        .skill-bar { height:6px; border-radius:3px; background:rgba(255,255,255,0.06); overflow:hidden; }
        .skill-fill {
            height:100%; border-radius:3px;
            background:linear-gradient(90deg,var(--grad-start),var(--grad-end));
            width:0%; transition: width 1.5s cubic-bezier(0.25,0.46,0.45,0.94);
        }

        /* ════════════════ EXPERIENCE ════════════════ */
        .timeline { position:relative; padding-left:40px; }
        .timeline::before {
            content:''; position:absolute; left:15px; top:0; bottom:0; width:2px;
            background:linear-gradient(180deg,var(--primary),var(--accent),transparent);
        }
        .timeline-item {
            position:relative; margin-bottom:48px;
            padding:32px; border-radius:var(--radius);
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
        }
        .timeline-item:hover { border-color:rgba(108,99,255,0.2); transform:translateX(8px); }
        .timeline-dot {
            position:absolute; left:-33px; top:38px; width:12px; height:12px;
            border-radius:50%; background:var(--primary);
            border:3px solid var(--dark-bg);
            box-shadow: 0 0 0 3px rgba(108,99,255,0.3);
        }
        .timeline-header { display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:16px; }
        .timeline-company { font-size:1.2rem; font-weight:700; color:var(--heading); }
        .timeline-role { font-size:0.95rem; color:var(--primary); font-weight:500; margin-top:4px; }
        .timeline-meta { text-align:right; }
        .timeline-duration { font-size:0.85rem; opacity:0.7; }
        .timeline-location { font-size:0.82rem; opacity:0.5; }
        .timeline-type {
            display:inline-block; padding:3px 10px; border-radius:50px;
            background:rgba(108,99,255,0.1); font-size:0.75rem; color:var(--primary);
            font-weight:500; margin-top:4px;
        }
        .timeline-desc { list-style:none; padding:0; margin: 12px 0; }
        .timeline-desc li {
            padding: 6px 0 6px 20px; position:relative; font-size:0.92rem; opacity:0.8;
        }
        .timeline-desc li::before {
            content:'▹'; position:absolute; left:0; color:var(--primary); font-weight:700;
        }
        .timeline-tech { display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }
        .timeline-tech span {
            padding:4px 12px; border-radius:6px; font-size:0.78rem;
            background:rgba(108,99,255,0.08); color:var(--primary); font-weight:500;
        }

        /* ════════════════ PROJECTS ════════════════ */
        .project-filters {
            display:flex; justify-content:center; gap:8px; margin-bottom:48px; flex-wrap:wrap;
        }
        .filter-btn {
            padding:8px 20px; border-radius:50px; border:1px solid rgba(255,255,255,0.1);
            background:transparent; color:var(--text); font-size:0.85rem;
            font-weight:500; cursor:pointer; transition:var(--transition); font-family:var(--font);
        }
        .filter-btn.active, .filter-btn:hover {
            background:var(--primary); color:#fff; border-color:var(--primary);
        }
        .projects-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(360px,1fr)); gap:24px; }
        .project-card {
            border-radius:var(--radius); overflow:hidden;
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
            display:flex; flex-direction:column;
        }
        .project-card:hover {
            border-color:rgba(108,99,255,0.2); transform:translateY(-6px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }
        .project-image {
            height:200px; position:relative; overflow:hidden;
            background:linear-gradient(135deg, rgba(108,99,255,0.15), rgba(0,210,255,0.15));
            display:flex; align-items:center; justify-content:center;
        }
        .project-image img { width:100%; height:100%; object-fit:cover; }
        .project-image-placeholder { font-size:3rem; opacity:0.3; }
        .featured-badge {
            position:absolute; top:12px; right:12px; padding:4px 12px;
            border-radius:50px; background:var(--secondary); color:#fff;
            font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;
        }
        .project-body { padding:28px; flex:1; display:flex; flex-direction:column; }
        .project-category { font-size:0.78rem; color:var(--primary); font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
        .project-title { font-size:1.2rem; font-weight:700; color:var(--heading); margin-bottom:12px; }
        .project-desc { font-size:0.9rem; opacity:0.7; margin-bottom:20px; flex:1; }
        .project-tech { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:20px; }
        .project-tech span {
            padding:3px 10px; border-radius:6px; font-size:0.75rem;
            background:rgba(108,99,255,0.08); color:var(--primary); font-weight:500;
        }
        .project-links { display:flex; gap:12px; }
        .project-link {
            padding:8px 18px; border-radius:8px; font-size:0.82rem;
            font-weight:500; transition:var(--transition);
            display:inline-flex; align-items:center; gap:6px;
        }
        .project-link-code { background:rgba(255,255,255,0.06); color:var(--text); }
        .project-link-code:hover { background:rgba(108,99,255,0.15); color:var(--primary); }
        .project-link-live {
            background:linear-gradient(135deg,var(--grad-start),var(--grad-end)); color:#fff;
        }
        .project-link-live:hover { transform:translateY(-2px); box-shadow:0 4px 15px rgba(108,99,255,0.3); }

        /* ════════════════ EDUCATION ════════════════ */
        .edu-card {
            padding:40px; border-radius:var(--radius);
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); max-width:800px; margin:0 auto;
        }
        .edu-header { margin-bottom:24px; }
        .edu-institution { font-size:1.4rem; font-weight:700; color:var(--heading); }
        .edu-degree { font-size:1rem; color:var(--primary); margin-top:4px; }
        .edu-meta { display:flex; gap:20px; margin-top:8px; font-size:0.88rem; opacity:0.6; }
        .edu-section-title { font-size:0.9rem; font-weight:600; color:var(--heading); margin:20px 0 12px; text-transform:uppercase; letter-spacing:1px; }
        .edu-list { display:flex; flex-wrap:wrap; gap:8px; }
        .edu-chip {
            padding:5px 14px; border-radius:8px;
            background:rgba(108,99,255,0.08); font-size:0.82rem; color:var(--primary); font-weight:500;
        }
        .edu-achievement {
            padding:8px 0 8px 20px; position:relative; font-size:0.9rem; opacity:0.8;
        }
        .edu-achievement::before { content:'▹'; position:absolute; left:0; color:var(--primary); font-weight:700; }

        /* ════════════════ CERTIFICATIONS ════════════════ */
        .cert-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; margin-top:48px; }
        .cert-card {
            padding:24px; border-radius:var(--radius);
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
            text-align:center;
        }
        .cert-card:hover { border-color:rgba(108,99,255,0.2); transform:translateY(-4px); }
        .cert-icon { font-size:2.5rem; margin-bottom:12px; }
        .cert-name { font-size:1rem; font-weight:600; color:var(--heading); margin-bottom:4px; }
        .cert-issuer { font-size:0.85rem; opacity:0.6; margin-bottom:4px; }
        .cert-date { font-size:0.8rem; color:var(--primary); font-weight:500; }

        /* ════════════════ ACHIEVEMENTS ════════════════ */
        .achieve-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:20px; }
        .achieve-card {
            padding:28px; border-radius:var(--radius); text-align:center;
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
        }
        .achieve-card:hover { border-color:rgba(108,99,255,0.2); transform:translateY(-4px); }
        .achieve-icon { font-size:2.5rem; margin-bottom:12px; }
        .achieve-title { font-size:1rem; font-weight:600; color:var(--heading); margin-bottom:8px; }
        .achieve-desc { font-size:0.88rem; opacity:0.6; }

        /* ════════════════ TESTIMONIALS ════════════════ */
        .testimonials-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(400px,1fr)); gap:24px; }
        .testimonial-card {
            padding:36px; border-radius:var(--radius);
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
            position:relative;
        }
        .testimonial-card:hover { border-color:rgba(108,99,255,0.2); }
        .testimonial-quote { font-size:3rem; color:var(--primary); opacity:0.3; position:absolute; top:16px; left:24px; line-height:1; font-family:Georgia,serif; }
        .testimonial-text { font-size:1rem; opacity:0.8; margin-bottom:20px; padding-top:20px; font-style:italic; }
        .testimonial-author { display:flex; align-items:center; gap:12px; }
        .testimonial-avatar {
            width:48px; height:48px; border-radius:50%;
            background:linear-gradient(135deg,var(--grad-start),var(--grad-end));
            display:flex; align-items:center; justify-content:center;
            font-size:1.2rem; color:#fff; font-weight:600;
        }
        .testimonial-name { font-size:0.95rem; font-weight:600; color:var(--heading); }
        .testimonial-role { font-size:0.82rem; opacity:0.6; }

        /* ════════════════ CONTACT ════════════════ */
        .contact-content { max-width:700px; margin:0 auto; text-align:center; }
        .contact-content h2 { font-size:2.4rem; font-weight:800; color:var(--heading); margin-bottom:16px; }
        .contact-content p { font-size:1.05rem; opacity:0.7; margin-bottom:40px; }
        .contact-links { display:flex; flex-wrap:wrap; justify-content:center; gap:16px; margin-bottom:40px; }
        .contact-link {
            display:flex; align-items:center; gap:10px;
            padding:14px 28px; border-radius:12px;
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            backdrop-filter:blur(10px); transition:var(--transition);
            font-size:0.92rem;
        }
        .contact-link:hover { border-color:var(--primary); transform:translateY(-3px); }
        .contact-link i { color:var(--primary); font-size:1.1rem; }
        .social-links { display:flex; justify-content:center; gap:16px; }
        .social-link {
            width:52px; height:52px; border-radius:14px;
            background:var(--card-bg); border:1px solid rgba(255,255,255,0.06);
            display:flex; align-items:center; justify-content:center;
            font-size:1.3rem; color:var(--text); transition:var(--transition);
        }
        .social-link:hover {
            background:var(--primary); color:#fff; border-color:var(--primary);
            transform:translateY(-4px); box-shadow:0 8px 25px rgba(108,99,255,0.3);
        }

        /* ════════════════ FOOTER ════════════════ */
        footer {
            text-align:center; padding:40px;
            border-top:1px solid rgba(255,255,255,0.06);
            font-size:0.85rem; opacity:0.5;
        }

        /* ════════════════ SCROLL REVEAL ════════════════ */
        .reveal { opacity:0; transform:translateY(30px); transition: all 0.8s cubic-bezier(0.25,0.46,0.45,0.94); }
        .reveal.visible { opacity:1; transform:translateY(0); }

        /* ════════════════ RESPONSIVE ════════════════ */
        @media (max-width:900px) {
            .navbar { padding:0 20px; }
            .nav-links {
                position:fixed; top:72px; left:0; right:0; bottom:0;
                background:rgba(10,10,26,0.98); flex-direction:column;
                padding:40px 20px; gap:8px;
                transform:translateX(100%); transition:var(--transition);
            }
            .nav-links.open { transform:translateX(0); }
            .hamburger { display:flex; }
            section { padding:60px 20px; }
            .hero { padding:100px 20px 60px; }
            .hero-stats { gap:24px; flex-wrap:wrap; }
            .about-grid { grid-template-columns:1fr; gap:40px; }
            .about-image-wrapper { order:-1; }
            .skills-grid { grid-template-columns:1fr; }
            .projects-grid { grid-template-columns:1fr; }
            .testimonials-grid { grid-template-columns:1fr; }
            .timeline { padding-left:30px; }
        }
        @media (max-width:480px) {
            .hero h1 { font-size:2.2rem; letter-spacing:-1px; }
            .hero-actions { flex-direction:column; }
            .btn { width:100%; justify-content:center; }
            .contact-links { flex-direction:column; }
        }

        /* ════════════════ ANIMATIONS ════════════════ */
        @keyframes fadeInUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
        @keyframes fadeInLeft { from{opacity:0;transform:translateX(-30px)} to{opacity:1;transform:translateX(0)} }
        @keyframes fadeInRight { from{opacity:0;transform:translateX(30px)} to{opacity:1;transform:translateX(0)} }
        .delay-1 { animation-delay:0.1s; }
        .delay-2 { animation-delay:0.2s; }
        .delay-3 { animation-delay:0.3s; }
        .delay-4 { animation-delay:0.4s; }

        /* ════════════════ TYPING ANIMATION ════════════════ */
        .typing-container { display:inline; }
        .typing-text { border-right:2px solid var(--primary); padding-right:4px; animation: blink 1s step-end infinite; }
        @keyframes blink { 50%{border-color:transparent} }
    </style>
</head>
<body>
    <!-- Background effects -->
    <div class="bg-grid"></div>
    <div class="bg-glow bg-glow-1"></div>
    <div class="bg-glow bg-glow-2"></div>
    <div class="bg-glow bg-glow-3"></div>
    <div class="cursor-glow" id="cursorGlow"></div>

    <!-- ═══════ NAVBAR ═══════ -->
    <nav class="navbar" id="navbar">
        <a href="#" class="nav-logo">&lt;{{ cfg.personal.name.split()[0] }} /&gt;</a>
        <div class="nav-links" id="navLinks">
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#experience">Experience</a>
            <a href="#projects">Projects</a>
            <a href="#education">Education</a>
            <a href="#contact" class="nav-cta">Contact</a>
        </div>
        <div class="hamburger" id="hamburger" onclick="toggleMenu()">
            <span></span><span></span><span></span>
        </div>
    </nav>

    <!-- ═══════ HERO ═══════ -->
    <section class="hero" id="hero">
        <div class="hero-content">
            {% if cfg.personal.available_for_hire %}
            <div class="hero-badge">
                <span class="pulse"></span> Available for opportunities
            </div>
            {% endif %}
            <h1>Hi, I'm <span class="gradient-text">{{ cfg.personal.name }}</span></h1>
            <h1 style="font-size:clamp(1.5rem,3vw,2.5rem);font-weight:600;color:var(--text);opacity:0.7;animation:fadeInUp 0.8s ease 0.15s both;">
                <span class="typing-container"><span class="typing-text" id="typingText"></span></span>
            </h1>
            <p class="hero-subtitle">{{ cfg.personal.tagline }}</p>
            <div class="hero-actions">
                <a href="#projects" class="btn btn-primary">
                    <i class="fas fa-rocket"></i> View My Work
                </a>
                <a href="{{ cfg.personal.resume_link }}" class="btn btn-outline" target="_blank">
                    <i class="fas fa-download"></i> Download Resume
                </a>
                <a href="#contact" class="btn btn-outline">
                    <i class="fas fa-paper-plane"></i> Get in Touch
                </a>
            </div>
            <div class="hero-stats">
                <div class="stat-item">
                    <div class="stat-number" data-count="{{ cfg.experience|length }}">0+</div>
                    <div class="stat-label">Years Experience</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" data-count="{{ cfg.projects|length }}">0+</div>
                    <div class="stat-label">Projects Built</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" data-count="{{ total_tech }}">0+</div>
                    <div class="stat-label">Technologies</div>
                </div>
            </div>
        </div>
        <div class="hero-scroll">
            <span>Scroll Down</span>
            <i class="fas fa-chevron-down"></i>
        </div>
    </section>

    <!-- ═══════ ABOUT ═══════ -->
    <section id="about">
        <div class="section-header reveal">
            <span class="section-label">About Me</span>
            <h2 class="section-title">Get to know me</h2>
        </div>
        <div class="about-grid">
            <div class="about-image-wrapper reveal">
                <div class="about-image-frame">
                    {% if cfg.personal.profile_image %}
                    <img src="{{ cfg.personal.profile_image }}" alt="{{ cfg.personal.name }}">
                    {% else %}
                    <div class="about-image-placeholder">👨‍💻</div>
                    {% endif %}
                </div>
            </div>
            <div class="about-text reveal">
                <h3>A passionate engineer who loves building things</h3>
                <p>{{ cfg.personal.bio }}</p>
                <div class="about-tags">
                    <span class="about-tag">🎯 Problem Solver</span>
                    <span class="about-tag">🚀 Fast Learner</span>
                    <span class="about-tag">🤝 Team Player</span>
                    <span class="about-tag">📐 Clean Code Advocate</span>
                    <span class="about-tag">🌍 Open Source Enthusiast</span>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════ SKILLS ═══════ -->
    <section id="skills">
        <div class="section-header reveal">
            <span class="section-label">Skills</span>
            <h2 class="section-title">Technologies I work with</h2>
            <p class="section-desc">Crafting solutions with the right tools for each challenge</p>
        </div>
        <div class="skills-grid">
            {% for skill_group in cfg.skills %}
            <div class="skill-card reveal">
                <div class="skill-card-header">
                    <span class="skill-card-icon">{{ skill_group.icon }}</span>
                    <span class="skill-card-title">{{ skill_group.category }}</span>
                </div>
                {% for item in skill_group['items'] %}
                <div class="skill-item">
                    <div class="skill-info">
                        <span class="skill-name">{{ item.name }}</span>
                        <span class="skill-pct">{{ item.level }}%</span>
                    </div>
                    <div class="skill-bar">
                        <div class="skill-fill" data-width="{{ item.level }}"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- ═══════ EXPERIENCE ═══════ -->
    <section id="experience">
        <div class="section-header reveal">
            <span class="section-label">Experience</span>
            <h2 class="section-title">Where I've worked</h2>
            <p class="section-desc">My professional journey and contributions</p>
        </div>
        <div class="timeline">
            {% for exp in cfg.experience %}
            <div class="timeline-item reveal">
                <div class="timeline-dot"></div>
                <div class="timeline-header">
                    <div>
                        <div class="timeline-company">{{ exp.company }}</div>
                        <div class="timeline-role">{{ exp.role }}</div>
                    </div>
                    <div class="timeline-meta">
                        <div class="timeline-duration">{{ exp.duration }}</div>
                        <div class="timeline-location">📍 {{ exp.location }}</div>
                        <span class="timeline-type">{{ exp.type }}</span>
                    </div>
                </div>
                <ul class="timeline-desc">
                    {% for point in exp.description %}
                    <li>{{ point }}</li>
                    {% endfor %}
                </ul>
                <div class="timeline-tech">
                    {% for t in exp.tech %}
                    <span>{{ t }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- ═══════ PROJECTS ═══════ -->
    <section id="projects">
        <div class="section-header reveal">
            <span class="section-label">Projects</span>
            <h2 class="section-title">Things I've built</h2>
            <p class="section-desc">A selection of projects that showcase my skills</p>
        </div>
        <div class="project-filters reveal">
            <button class="filter-btn active" onclick="filterProjects('all')">All</button>
            {% for cat in project_categories %}
            <button class="filter-btn" onclick="filterProjects('{{ cat }}')">{{ cat }}</button>
            {% endfor %}
        </div>
        <div class="projects-grid" id="projectsGrid">
            {% for proj in cfg.projects %}
            <div class="project-card reveal" data-category="{{ proj.category }}">
                <div class="project-image">
                    {% if proj.image %}
                    <img src="{{ proj.image }}" alt="{{ proj.title }}">
                    {% else %}
                    <div class="project-image-placeholder">🔧</div>
                    {% endif %}
                    {% if proj.featured %}
                    <span class="featured-badge">⭐ Featured</span>
                    {% endif %}
                </div>
                <div class="project-body">
                    <div class="project-category">{{ proj.category }}</div>
                    <div class="project-title">{{ proj.title }}</div>
                    <div class="project-desc">{{ proj.description }}</div>
                    <div class="project-tech">
                        {% for t in proj.tech %}
                        <span>{{ t }}</span>
                        {% endfor %}
                    </div>
                    <div class="project-links">
                        {% if proj.github %}
                        <a href="{{ proj.github }}" class="project-link project-link-code" target="_blank">
                            <i class="fab fa-github"></i> Code
                        </a>
                        {% endif %}
                        {% if proj.live %}
                        <a href="{{ proj.live }}" class="project-link project-link-live" target="_blank">
                            <i class="fas fa-external-link-alt"></i> Live
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- ═══════ EDUCATION & CERTS ═══════ -->
    <section id="education">
        <div class="section-header reveal">
            <span class="section-label">Education</span>
            <h2 class="section-title">Academic Background</h2>
        </div>
        {% for edu in cfg.education %}
        <div class="edu-card reveal">
            <div class="edu-header">
                <div class="edu-institution">🎓 {{ edu.institution }}</div>
                <div class="edu-degree">{{ edu.degree }}</div>
                <div class="edu-meta">
                    <span>📅 {{ edu.duration }}</span>
                    <span>📊 GPA: {{ edu.gpa }}</span>
                </div>
            </div>
            {% if edu.coursework %}
            <div class="edu-section-title">Key Coursework</div>
            <div class="edu-list">
                {% for course in edu.coursework %}
                <span class="edu-chip">{{ course }}</span>
                {% endfor %}
            </div>
            {% endif %}
            {% if edu.achievements %}
            <div class="edu-section-title">Achievements</div>
            {% for ach in edu.achievements %}
            <div class="edu-achievement">{{ ach }}</div>
            {% endfor %}
            {% endif %}
        </div>
        {% endfor %}
        {% if cfg.certifications %}
        <div class="cert-grid">
            {% for cert in cfg.certifications %}
            <a href="{{ cert.link }}" class="cert-card reveal" target="_blank">
                <div class="cert-icon">🏅</div>
                <div class="cert-name">{{ cert.name }}</div>
                <div class="cert-issuer">{{ cert.issuer }}</div>
                <div class="cert-date">{{ cert.date }}</div>
            </a>
            {% endfor %}
        </div>
        {% endif %}
    </section>

    <!-- ═══════ ACHIEVEMENTS ═══════ -->
    {% if cfg.achievements %}
    <section id="achievements">
        <div class="section-header reveal">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">Milestones & Recognition</h2>
        </div>
        <div class="achieve-grid">
            {% for ach in cfg.achievements %}
            <div class="achieve-card reveal">
                <div class="achieve-icon">{{ ach.icon }}</div>
                <div class="achieve-title">{{ ach.title }}</div>
                <div class="achieve-desc">{{ ach.description }}</div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- ═══════ TESTIMONIALS ═══════ -->
    {% if cfg.testimonials %}
    <section id="testimonials">
        <div class="section-header reveal">
            <span class="section-label">Testimonials</span>
            <h2 class="section-title">What people say</h2>
        </div>
        <div class="testimonials-grid">
            {% for test in cfg.testimonials %}
            <div class="testimonial-card reveal">
                <div class="testimonial-quote">"</div>
                <div class="testimonial-text">{{ test.text }}</div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">{{ test.name[0] }}</div>
                    <div>
                        <div class="testimonial-name">{{ test.name }}</div>
                        <div class="testimonial-role">{{ test.role }}</div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    <!-- ═══════ CONTACT ═══════ -->
    <section id="contact">
        <div class="contact-content reveal">
            <span class="section-label">Contact</span>
            <h2>Let's Build Something<br><span class="gradient-text">Amazing Together</span></h2>
            <p>I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.</p>
            <div class="contact-links">
                <a href="mailto:{{ cfg.personal.email }}" class="contact-link">
                    <i class="fas fa-envelope"></i> {{ cfg.personal.email }}
                </a>
                {% if cfg.personal.phone %}
                <a href="tel:{{ cfg.personal.phone }}" class="contact-link">
                    <i class="fas fa-phone"></i> {{ cfg.personal.phone }}
                </a>
                {% endif %}
                {% if cfg.personal.location %}
                <div class="contact-link">
                    <i class="fas fa-map-marker-alt"></i> {{ cfg.personal.location }}
                </div>
                {% endif %}
            </div>
            <div class="social-links">
                {% if cfg.social.github %}
                <a href="{{ cfg.social.github }}" class="social-link" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                {% endif %}
                {% if cfg.social.linkedin %}
                <a href="{{ cfg.social.linkedin }}" class="social-link" target="_blank" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                {% endif %}
                {% if cfg.social.twitter %}
                <a href="{{ cfg.social.twitter }}" class="social-link" target="_blank" title="Twitter"><i class="fab fa-twitter"></i></a>
                {% endif %}
                {% if cfg.social.leetcode %}
                <a href="{{ cfg.social.leetcode }}" class="social-link" target="_blank" title="LeetCode"><i class="fas fa-code"></i></a>
                {% endif %}
                {% if cfg.social.devto %}
                <a href="{{ cfg.social.devto }}" class="social-link" target="_blank" title="Dev.to"><i class="fab fa-dev"></i></a>
                {% endif %}
                {% if cfg.social.medium %}
                <a href="{{ cfg.social.medium }}" class="social-link" target="_blank" title="Medium"><i class="fab fa-medium"></i></a>
                {% endif %}
                {% if cfg.social.stackoverflow %}
                <a href="{{ cfg.social.stackoverflow }}" class="social-link" target="_blank" title="StackOverflow"><i class="fab fa-stack-overflow"></i></a>
                {% endif %}
            </div>
        </div>
    </section>

    <!-- ═══════ FOOTER ═══════ -->
    <footer>
        <p>© {{ cfg.footer.copyright }} {{ cfg.personal.name }}. {{ cfg.footer.tagline }}</p>
    </footer>

    <!-- ═══════ JAVASCRIPT ═══════ -->
    <script>
        // ── Cursor follower ──
        document.addEventListener('mousemove', e => {
            const glow = document.getElementById('cursorGlow');
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });

        // ── Navbar scroll effect ──
        window.addEventListener('scroll', () => {
            document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
        });

        // ── Mobile menu ──
        function toggleMenu() {
            document.getElementById('navLinks').classList.toggle('open');
            document.getElementById('hamburger').classList.toggle('active');
        }
        document.querySelectorAll('.nav-links a').forEach(a => {
            a.addEventListener('click', () => {
                document.getElementById('navLinks').classList.remove('open');
                document.getElementById('hamburger').classList.remove('active');
            });
        });

        // ── Active nav link highlight ──
        const sections = document.querySelectorAll('section[id]');
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY + 100;
            sections.forEach(sec => {
                const top = sec.offsetTop, height = sec.offsetHeight, id = sec.getAttribute('id');
                const link = document.querySelector(`.nav-links a[href="#${id}"]`);
                if (link) link.classList.toggle('active', scrollY >= top && scrollY < top + height);
            });
        });

        // ── Typing animation ──
        const titles = [
            "{{ cfg.personal.title }}",
            {% for sg in cfg.skills %}"{{ sg.category }} Expert",{% endfor %}
            "Problem Solver"
        ];
        let titleIdx = 0, charIdx = 0, deleting = false;
        const typingEl = document.getElementById('typingText');
        function typeEffect() {
            const current = titles[titleIdx];
            typingEl.textContent = current.substring(0, charIdx);
            if (!deleting) {
                charIdx++;
                if (charIdx > current.length) { deleting = true; setTimeout(typeEffect, 2000); return; }
            } else {
                charIdx--;
                if (charIdx < 0) { deleting = false; titleIdx = (titleIdx + 1) % titles.length; charIdx = 0; }
            }
            setTimeout(typeEffect, deleting ? 40 : 80);
        }
        typeEffect();

        // ── Scroll reveal ──
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Animate skill bars
                    entry.target.querySelectorAll('.skill-fill').forEach(bar => {
                        bar.style.width = bar.dataset.width + '%';
                    });
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

        // ── Counter animation ──
        function animateCounters() {
            document.querySelectorAll('.stat-number').forEach(counter => {
                const target = parseInt(counter.dataset.count) || 0;
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                const update = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.ceil(current) + '+';
                        requestAnimationFrame(update);
                    } else {
                        counter.textContent = target + '+';
                    }
                };
                update();
            });
        }
        animateCounters();

        // ── Project filter ──
        function filterProjects(category) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            document.querySelectorAll('.project-card').forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = '';
                    card.style.animation = 'fadeInUp 0.5s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        // ── Smooth scroll for all anchor links ──
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    </script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════
#  RUN SERVER
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    PORT = 5000
    print("\n" + "=" * 60)
    print("  >>  PORTFOLIO SERVER RUNNING")
    print(f"  ->  Open: http://localhost:{PORT}")
    print("  ->  Edit config.json & refresh to update content")
    print("  ->  Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    # Auto-open browser
    threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    app.run(debug=True, port=PORT, use_reloader=True)
