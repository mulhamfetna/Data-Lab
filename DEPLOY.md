# Deploying the Data Lab

The app is self-contained and offline-safe. This repo is prepared for **four** ways to run it,
from zero-setup to full control. Pick one — the app code is identical across all of them.

## Two things that apply to every host

- **GenAI keys (optional).** The GenAI demos call a real model only when a free provider key is
  present — `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `HF_TOKEN`, or a local `OLLAMA_HOST`. With none
  set they run a clearly-labeled **offline simulation** and the app still works fully. Key names
  and format are in [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example). The app
  reads them from either the environment or `st.secrets` (bridged automatically).
- **The `.sy` scraper targets are local-only.** They're geo-blocked outside Syria and need
  system Chrome/Playwright, which the cloud images don't ship. Run the app **locally on a Syrian
  connection** for those specific sites; every other demo works on any host.

---

## 1. Streamlit Community Cloud — easiest, free  ⭐ recommended

Auto-redeploys on every push to `main`, and gives a public `*.streamlit.app` URL.

1. https://share.streamlit.io → sign in with GitHub → authorize.
2. **New app** → repo `mulhamfetna/Data-Lab`, branch `main`, main file `Home.py` → **Deploy**.
3. App → **Settings → Secrets** → paste a key, e.g. `GROQ_API_KEY = "gsk_..."`.
4. Open the in-app **Share (QR)** page, paste the `*.streamlit.app` URL, project the QR.

## 2. Hugging Face Spaces — free, container-based, auto-deployed

The Space runs this repo's `Dockerfile` and **auto-updates on every push to `main`** via the
[`sync-to-hf-space`](.github/workflows/sync-to-hf-space.yml) workflow.

One-time setup:

1. Create the Space: <https://huggingface.co/new-space> → owner `mulhamfetna`, name `Data-Lab`,
   **SDK: Docker**, public. (Leave it empty — the workflow pushes the code.)
2. Create a Hugging Face token with **write** access:
   <https://huggingface.co/settings/tokens>
3. Add it to GitHub as a repo secret named **`HF_TOKEN`**:
   *Settings → Secrets and variables → Actions → New repository secret.*
4. Push to `main` (or run the workflow manually) — the Space builds and goes live.

To enable the **live GenAI demos** on the Space, also add a token in the Space itself:
*Space → Settings → Variables and secrets → New secret* → `HF_TOKEN`. The app detects it and
prefers **Hugging Face Inference Providers** while running on a Space, using
`openai/gpt-oss-20b:cheapest` (open weights, routed to the cheapest provider). Free accounts get
a limited monthly inference quota — with no token, the demos fall back to the labelled offline
simulation and everything else still works.

The Space's `README.md` (front-matter that Spaces requires) is generated from
[`docs/deploy/hf-space-README.md`](docs/deploy/hf-space-README.md) — edit it there, not on the Space.

## 3. Docker / VPS — full control

```bash
docker compose up -d          # → http://<host>:8501
# or, without compose:
docker build -t data-lab .
docker run -p 8501:8501 --env-file .env data-lab
```

Put any GenAI keys in a `.env` file next to `docker-compose.yml` (names as in the secrets
example). Serve behind your own domain/reverse proxy. A VPS **inside Syria** is also the only
cloud option that can reach the `.sy` scraper targets.

### Fly.io

```bash
fly launch --copy-config --now      # uses the bundled fly.toml + Dockerfile
fly secrets set GROQ_API_KEY=gsk_... # keys as secrets, not baked into the image
```

## 4. Local network — the workshop laptop

```bash
./run.sh
```

Streamlit prints a **Network URL** (e.g. `http://10.0.0.5:8501`); anyone on the same Wi-Fi can
open it. Paste that into the **Share (QR)** page for the room. This is the setup that can also
run the `.sy` scraper demo (on a Syrian connection).
