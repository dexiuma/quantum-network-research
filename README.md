# PaperMiner — Website

This repository hosts the public landing page for **PaperMiner**, a fully-local,
multi-agent system for collecting research papers and extracting graphs, data
points, and formulas — powered entirely by locally deployed LLMs.

The application source code lives in a separate (private) repository. This repo
contains **only** the static marketing site, published via GitHub Pages.

## Contents

```
.
├── index.html                # Single-file landing page (self-contained CSS/JS)
├── assets/architecture.png   # System architecture diagram
├── robots.txt                # Opt out of search-engine indexing
└── .nojekyll                 # Serve files as-is (skip Jekyll processing)
```

## Publishing (GitHub Pages)

1. Push this repository to a **public** GitHub repo.
2. In the repo: **Settings → Pages → Build and deployment**.
3. Source: **Deploy from a branch**, Branch: **`main`**, Folder: **`/ (root)`**.
4. Save. The site goes live at `https://<user>.github.io/<repo>/`.

## Local preview

```bash
python3 -m http.server 8099
# then open http://localhost:8099
```

## Notes

- The site is intentionally excluded from search engines (`robots.txt` +
  `noindex` meta tags). Remove those if you want it indexed.
- It's a single self-contained HTML file — no build step required.
