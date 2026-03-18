"""
build.py  —  Static site builder for the Data Science Portfolio Template.

Usage:
    uv run python build.py

What this script does:
  1. Reads portfolio_config.yaml (theme, student file, project list).
  2. Loads the student profile YAML and all project YAMLs.
  3. Renders templates/index.html via Jinja2 into docs/index.html.
  4. Copies static/ assets (CSS, images) into docs/ unchanged.

After running this script, open docs/index.html in a browser or run
  uv run python serve.py
to preview the site locally.
"""

import shutil
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent          # repo root
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR    = ROOT / "static"
DOCS_DIR      = ROOT / "docs"
CONFIG_FILE   = ROOT / "portfolio_config.yaml"


# ── Helpers ────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    """Read a YAML file and return its contents as a Python dictionary."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def copy_static_assets(src: Path, dest: Path) -> None:
    """
    Copy everything under src/ into dest/, preserving subdirectory structure.
    Existing files in dest/ are overwritten; extra files are left alone.
    """
    if not src.exists():
        print(f"  [warn] Static directory not found: {src} — skipping.")
        return

    for item in src.rglob("*"):
        if item.is_file():
            relative = item.relative_to(src)
            target = dest / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            print(f"  copied  static/{relative}")


# ── Main build ─────────────────────────────────────────────────────────────

def build() -> None:
    print("=" * 55)
    print("  Building portfolio site → docs/")
    print("=" * 55)

    # ── 1. Load config ──────────────────────────────────────────────────
    if not CONFIG_FILE.exists():
        sys.exit(f"Error: {CONFIG_FILE} not found. Are you running from the repo root?")

    config = load_yaml(CONFIG_FILE)
    print(f"\n[1/5] Loaded config:  {CONFIG_FILE.name}")

    theme       = config.get("theme", "light")
    site_title  = config.get("site_title", "My Portfolio")
    student_rel = config.get("student_file", "content/example_student.yaml")
    project_rel = config.get("projects", [])
    blog_rel = config.get("blog_posts", [])

    # ── 2. Load student profile ─────────────────────────────────────────
    student_path = ROOT / student_rel
    if not student_path.exists():
        sys.exit(f"Error: student file '{student_rel}' not found.")

    student = load_yaml(student_path)
    # Convert the about field from Markdown to HTML so students can use
    # standard Markdown syntax: blank lines for paragraphs, *italic*, **bold**, etc.
    if student.get("about"):
        student["about"] = markdown.markdown(student["about"])
    print(f"[2/5] Loaded student: {student_path.name}  ({student.get('name', '?')})")

    # ── 3. Load project files ───────────────────────────────────────────
    projects = []
    for rel in project_rel:
        p = ROOT / rel
        if not p.exists():
            print(f"  [warn] Project file not found, skipping: {rel}")
            continue
        projects.append(load_yaml(p))
        print(f"       project: {p.name}")

    print(f"[3/5] Loaded {len(projects)} project(s).")


     # ── 4. Load blog files ──────────────────────────────────────────────
    blog_posts = []
    for rel in blog_rel:
        p = ROOT / rel
        if not p.exists():
            print(f"  [warn] Blog file not found, skipping: {rel}")
            continue

        post = load_yaml(p)

        # convert markdown to HTML for content
        if post.get("content"):
            post["content"] = markdown.markdown(post["content"])

        blog_posts.append(post)
        print(f"       blog:    {p.name}")

    # ── 5. Render HTML ──────────────────────────────────────────────────
    DOCS_DIR.mkdir(exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )

    template = env.get_template("index.html")
    rendered = template.render(
        site_title=site_title,
        theme=theme,
        student=student,
        projects=projects,
        blog_posts=blog_posts,
    )

    output_path = DOCS_DIR / "index.html"
    output_path.write_text(rendered, encoding="utf-8")
    print(f"[5/5] Rendered → {output_path.relative_to(ROOT)}")

    # ── 6. Copy static assets ───────────────────────────────────────────
    print("\n      Copying static assets …")
    copy_static_assets(STATIC_DIR, DOCS_DIR)

    print("\n✓  Build complete.  Open docs/index.html or run: uv run python serve.py")
    print("=" * 55)


if __name__ == "__main__":
    build()
