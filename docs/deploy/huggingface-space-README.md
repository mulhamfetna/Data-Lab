# Hugging Face Spaces — template

Spaces builds from a repo whose `README.md` starts with a YAML front-matter block. Create a
new Space (**SDK: Docker**), then make its `README.md` begin with exactly this, and push this
project's files into the Space repo (or mirror this GitHub repo into it):

```markdown
---
title: Data Lab
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
license: agpl-3.0
---

# Data to Decisions — Interactive Data-Literacy Workshop Platform
See https://github.com/mulhamfetna/Data-Lab
```

Notes:

- **SDK: docker** makes Spaces build this project's `Dockerfile` (which already runs as a
  non-root user, as Spaces requires) and serve it on `app_port` 8501.
- **GenAI keys:** Space → **Settings → Variables and secrets** → add e.g. `GROQ_API_KEY`.
  The app's `st.secrets` bridge picks them up automatically.
- The `.sy` scraper targets remain unreachable from Spaces (geo-blocked, no system Chrome) —
  that demo stays local-only, as documented in `DEPLOY.md`.
