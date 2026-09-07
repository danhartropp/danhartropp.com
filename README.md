# danhartropp.com

A small Flask app that renders Markdown into a static site. Netlify runs
`python freeze.py` on every push and publishes the `build/` folder, so the
Flask app itself never runs in production — it exists to generate the HTML
and to preview changes locally.

## Running it locally

There is no virtualenv in the repo (`/env/` is gitignored). The quickest way
in is `uv`, which resolves the pinned dependencies into a throwaway
environment:

```bash
uv run --no-project --with-requirements requirements.txt flask --app app run --debug --host 0.0.0.0
```

Then open <http://127.0.0.1:5000/index.html>, or reach it from another device
on the network at `http://<this machine's IP>:5000/index.html`.

`--host 0.0.0.0` binds every interface rather than loopback only, which is
what makes the site reachable from a phone or another machine. It also means
anyone on the same network can load it, so use it on a network you trust —
the Flask development server is not hardened and is not meant to face the
internet. Drop the flag to go back to localhost only.

`--debug` gives auto-reload, so editing a file under `content/` and
refreshing the page is enough — no rebuild step. `--no-project` matters:
without it `uv` sees a directory with no `pyproject.toml` and scaffolds one.

Note that `--debug` and `--host 0.0.0.0` together expose the interactive
debugger to the network. It is PIN-protected, but on an untrusted network
run one or the other, not both.

Every route is an explicit `.html` path, so `/read/` will 404. Use
`/read/index.html`.

If you would rather have a persistent environment:

```bash
python3 -m venv env && env/bin/pip install -r requirements.txt
env/bin/flask --app app run --debug --host 0.0.0.0
```

## Building the static site

This is the same command Netlify runs (see `netlify.toml`):

```bash
uv run --no-project --with-requirements requirements.txt python freeze.py
```

It writes `build/`, plus `build/sitemap.xml` and `build/_redirects`, and
prints a count of what it froze. To view the frozen output rather than the
live app:

```bash
python3 -m http.server -d build --bind 0.0.0.0 8000
```

## Adding a post

Posts are Markdown files with YAML frontmatter, one per file, in
`content/read/` (applied AI) or `content/code/` (the aphorisms). The filename
becomes the URL, so `content/read/my_post.md` is served at
`/read/my_post.html`.

```markdown
---
title: The title, rendered as the page's h1
subtitle: a lower-case line under it
date: 2026-09-07
---
The body starts here. Do not repeat the title as an `# h1` — the template
already renders it.
```

`date` drives the ordering on the section index and in the RSS feed. Without
an explicit `excerpt` in the frontmatter, the index uses the first rendered
paragraph.

Only two Markdown extensions are enabled (`tables` and `fenced_code`), so
pipe tables and fenced code work but footnotes, attribute lists and the rest
do not.

Images live under `static/img/<topic>/` and are referenced by absolute path,
which is what Frozen-Flask needs to copy them:

```markdown
![Alt text that describes the image](/static/img/micropolis/scoreboard.png)
```

Keep them small. The site loads no third-party resources and the whole page
weight budget is modest, so optimise before committing rather than after.

## Layout

```
app.py          routes, Markdown rendering, the two template filters
freeze.py       the static build: Frozen-Flask, sitemap.xml, _redirects
content/        the posts, as Markdown with frontmatter
  read/         applied AI writing
  code/         the aphorisms, moved here from /read/ (see LEGACY_READ_SLUGS)
  look/         art series, one folder per series
templates/      Jinja templates; post.html renders a single post
static/         css, images, favicons — copied verbatim into the build
build/          generated output, gitignored
```

A slug moved from `/read/` to `/code/` needs an entry in `LEGACY_READ_SLUGS`
in `freeze.py`, which mints the Netlify 301. That list is deliberately
hand-maintained rather than derived from the content folder.
