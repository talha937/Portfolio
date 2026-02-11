"""
UPDATE & DEPLOY SCRIPT
──────────────────────
After editing config.json (or adding images to static/),
just run this script to rebuild and redeploy:

    python update.py
"""
import subprocess, sys, os, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def run(cmd, label):
    print(f"\n  [{label}] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  [ERROR] {result.stderr.strip()}")
        return False
    print(f"  [{label}] Done!")
    return True

print("=" * 55)
print("   PORTFOLIO UPDATE & DEPLOY")
print("=" * 55)

# Step 1: Rebuild static site from config.json
python = sys.executable
if not run(f'"{python}" build.py', "BUILD"):
    print("\n  Build failed. Fix config.json and try again.")
    sys.exit(1)

# Step 2: Git commit
run('git add .', "GIT")
run('git commit -m "Update portfolio"', "GIT")
run('git push', "GIT")

# Step 3: Deploy to Vercel
if not run("vercel --prod --yes", "VERCEL"):
    print("\n  Vercel deploy failed. Run 'vercel login' if auth expired.")
    sys.exit(1)

print("\n" + "=" * 55)
print("   ALL DONE! Your portfolio is updated & live.")
print("=" * 55 + "\n")
