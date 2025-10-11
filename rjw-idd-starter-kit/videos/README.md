# Video Tutorial Guidance

This directory should contain short tutorial videos and accompanying metadata for the RJW-IDD starter kit and its tutorials. The starter kit includes written tutorials under `tutorials/`. Adding short video explainers to the README and a `videos/` folder helps newcomers learn faster.

Hosting options

- External (recommended)
  - Host videos on YouTube (unlisted for private sharing) or a company Vimeo/Cloud provider and embed links in README files. This keeps the repository small.
  - Store captions and small thumbnails in the repo if needed.

- Internal (not recommended unless required)
  - Committing video binaries into the repository is discouraged — large files bloat the repo. Use Git LFS if you must store video files in Git.

Embedding best practice

- Add an optional badge/thumbnail in the `rjw-idd-starter-kit/README.md` that links to the video landing page.
- Include a 30–60s intro clip for the methodology and short 2–5 minute clips for tutorial walkthroughs.

Example YouTube embed (markdown):

[![Intro to RJW-IDD](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

Metadata

- Keep a `videos.yml` in this folder listing video IDs, titles, durations, and short descriptions. This file can be used by scripts to build an index in the README or landing page.

Sample videos.yml (YAML)

---
# videos.yml
- id: "VIDEO_ID"
  title: "Intro to RJW-IDD"
  duration: "0:45"
  description: "Short overview of the intelligence-driven methodology and how to use the starter kit."
---

Checklist for adding videos

1. Host video externally (YouTube/Vimeo/Cloud).
2. Add a small thumbnail and the `videos.yml` entry.
3. Add embed links in `rjw-idd-starter-kit/README.md` under "Tutorials & Video Resources".

Legal & Access

- Ensure you have rights to share the video publicly or set appropriate privacy settings on your host. Include a short credit or license note if needed.