# Quantum Network Research — Website

Public landing page for an integrated, fully-local **quantum-network research
platform** that unites three components:

1. **Quantum Network Survey & Research** — the literature survey and error-type
   taxonomy that anchors the project.
2. **QuantumPaperMiner** — a multi-agent system for mining quantum-science papers
   (graphs, data points, equations) and generating new data, powered by local LLMs.
3. **Quantum Network Simulator** — a Qiskit-based simulator modelling network
   *nodes* (calibrated from real superconducting QPUs) and *links* (photonic
   fiber / wireless channels) with custom error models.

The application source code lives in separate (private) repositories. This repo
contains **only** the static marketing site, published via GitHub Pages.

## Contents

```
.
├── index.html                # Single-file landing page (self-contained CSS/JS)
├── assets/architecture.png   # QuantumPaperMiner system architecture diagram
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
