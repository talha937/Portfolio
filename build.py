"""
Build script — Renders the Flask/Jinja2 template into a static index.html
for deployment on GitHub Pages (or any static host).

Usage:  python build.py
Output: docs/index.html  (GitHub Pages can serve from /docs)
"""
import json, os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from jinja2 import Environment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")

# Load config
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

# Pre-compute Jinja-unfriendly values
total_tech = sum(len(s["items"]) for s in cfg.get("skills", []))
project_categories = list(dict.fromkeys(p["category"] for p in cfg.get("projects", [])))

# Extract HTML template from portfolio.py
with open(os.path.join(BASE_DIR, "portfolio.py"), "r", encoding="utf-8") as f:
    content = f.read()

start = content.find('HTML_TEMPLATE = r"""') + len('HTML_TEMPLATE = r"""')
end = content.find('\n"""', start)
template_str = content[start:end]

# Render
env = Environment(autoescape=False)
template = env.from_string(template_str)
html = template.render(cfg=cfg, json_data=json.dumps(cfg),
                       total_tech=total_tech,
                       project_categories=project_categories)

# Write output
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] Built static site -> docs/index.html ({len(html):,} bytes)")
print(f"[OK] Ready for GitHub Pages deployment")
