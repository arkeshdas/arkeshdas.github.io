# Professional Portfolio

A small static portfolio generator built with Python, YAML, Jinja2, and CSS. Content lives in YAML files, templates define page sections, and `build.py` generates the deployable site in `docs/` for GitHub Pages.

## Quick Start

```bash
uv sync
uv run python build.py
uv run python serve.py
```

`serve.py` previews the generated `docs/` site locally.

The same workflow is available through `make`:

```bash
make sync
make build
make serve
```

## How It Works

```text
portfolio_config.yaml      Site config, theme, project order, writing order
content/arkesh.yaml        Profile, hero, contact, paper, featured video
content/scholarship.yaml   Research and public scholarship page
content/cv.yaml            Reverse-chronological CV / experience timeline
content/about.yaml         Longer narrative about page
content/projects/*.yaml    Project cards
content/blog/*.yaml        Writing entries and self-hosted post bodies
content/drafts/            Local-only drafts ignored by git
templates/base.html        Page shell, nav, hero, footer
templates/index.html       Home page section order
templates/*.html           Detail page and blog post templates
templates/sections/        Individual page sections
static/css/base.css        Layout, typography, responsiveness, print rules
static/css/themes/*.css    Theme colors, surfaces, borders, shadows
static/img/                Source images referenced from YAML
docs/                      Generated site for deployment
```

The build renders HTML pages, copies referenced images into `docs/`, skips dotfiles, and writes one deploy stylesheet:

```text
docs/index.html
docs/scholarship/index.html
docs/cv/index.html
docs/writing/index.html
docs/writing/<slug>/index.html
docs/about/index.html
```

```text
docs/css/site.css = static/css/base.css + selected theme
```

Do not edit files in `docs/` directly. Edit source files, then rebuild.

## Main Config

Edit `portfolio_config.yaml`:

```yaml
student_file: content/arkesh.yaml

projects:
  - content/projects/my_project.yaml

writing_posts:
  - content/blog/my_post.yaml

scholarship_file: content/scholarship.yaml
cv_file: content/cv.yaml
about_file: content/about.yaml

theme: clinical
site_title: "Your Name | Portfolio"
```

The build appends an automatic CSS fingerprint to the stylesheet URL, so browsers do not reuse stale cached styles after CSS changes.

## Profile Fields

Use `content/example_student.yaml` as the current schema reference.

Common fields:

```yaml
name:
role:
current_role:
headline:
tagline:
github:
linkedin:
email:
paper_url:
featured_video_url:
featured_video_start_seconds:
featured_video_captions:
featured_video_captions_lang:
formspree_endpoint:
headshot:
about:
```

`featured_video_url` accepts common YouTube watch or share URLs. The build converts them to a privacy-friendly embed URL. Optional video controls:

```yaml
featured_video_start_seconds: 1
featured_video_captions: true
featured_video_captions_lang: en
```

`formspree_endpoint` should be a Formspree endpoint such as:

```yaml
formspree_endpoint: https://formspree.io/f/abcdwxyz
```

## Projects

Each project YAML should include:

```yaml
title:
short_summary:
tech_stack:
problem_statement:
approach:
results_impact:
repo_url:
notebook_url:
image_path:
```

Place images in `static/img/` and reference them as:

```yaml
image_path: img/my-image.png
```

Project display order is controlled by `portfolio_config.yaml`.

## Writing

Writing entries live in `content/blog/` and use:

```yaml
title:
date:
featured:
short_summary:
slug:
has_original_post:
original_post_url:
image_path:
images:
content:
```

Writing order is controlled by `portfolio_config.yaml`. Set `featured: true` on the writing item that should receive the highlighted card treatment.

`content` is rendered as the full self-hosted post at:

```text
docs/writing/<slug>/index.html
```

If `slug` is omitted, the build uses the YAML filename. Set `has_original_post: true` and provide `original_post_url` when the post has an original external version or related PDF. Use `has_original_post: false` for writing that only lives on this site.

For local-only draft posts, put YAML files in `content/drafts/`. Drafts are ignored by git and are not published unless you move them into `content/blog/` and list them in `portfolio_config.yaml`.

Blog images can be placed in `static/img/` and referenced inside Markdown:

```markdown
![Alt text](img/example.png)
```

The build copies local images referenced by Markdown image syntax, `image_path`, or `images`.

## Themes

Source CSS is split by responsibility:

`static/css/base.css`
- layout
- spacing
- typography scale
- responsive behavior
- card structure
- form layout
- print rules

`static/css/themes/*.css`
- colors
- backgrounds
- borders
- shadows
- hover colors
- accent colors

Available themes:

```yaml
theme: clinical
theme: light
theme: dark
theme: msu-light
theme: msu-dark
```

All theme files cover the same site components, so changing `theme:` should preserve the layout.

## Build Hygiene

`build.py` cleans and regenerates `docs/` on every build. It copies only referenced image assets and warns about:

- missing theme files
- missing static assets referenced in YAML
- placeholder Formspree endpoints
- video URLs that cannot be converted to embeds

The build also validates required YAML fields, rejects content paths that point outside the repository, and computes the stylesheet cache version from the source CSS.

## Deployment

This repo is set up for GitHub Pages from `/docs`.

Typical workflow:

```bash
make build
git add .
git commit -m "update portfolio"
git push origin main
```

Then configure GitHub Pages to deploy from:

```text
main / docs
```
