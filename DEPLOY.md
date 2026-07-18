# Deploying the Data Lab

The app is self-contained and offline-safe. Three ways to make it reachable by an audience.

## 1. Streamlit Community Cloud (easiest, free)
1. Push to GitHub (done).
2. Go to https://share.streamlit.io → **New app** → pick this repo, branch `main`, file `Home.py`.
3. Deploy. You get a public `https://…streamlit.app` URL.
4. Open the in-app **Share (QR)** page, paste that URL, and project the QR for the room to scan.

## 2. Docker (self-host)
```bash
docker build -t data-lab .
docker run -p 8501:8501 data-lab
```
Then serve it behind your own domain/reverse proxy.

## 3. Local network (workshop laptop)
```bash
./run.sh
```
Streamlit prints a **Network URL** (e.g. `http://10.0.0.5:8501`) — anyone on the same Wi-Fi can
open it. Paste that into the Share (QR) page for the room.

> The `.sy` scraper targets only resolve from inside Syria; run locally on a Syrian connection
> for those. Everything else works anywhere.
