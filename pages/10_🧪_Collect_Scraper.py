import concurrent.futures as cf
import time
from datetime import date
from pathlib import Path

import streamlit as st

from contact_scraper import engine, exporters, photos
from contact_scraper.sites.registry import SITES
from workshop import ui

PREVIEW_DIR = Path(__file__).resolve().parent.parent / "assets" / "previews"

st.set_page_config(page_title="Scraper", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Web Scraper — your data can come from any website",
    "Public web pages are a giant, free data source. A scraper reads a page the way a "
    "person would and turns it into a structured list you can actually use — here, real "
    "people directories exported straight to phone contacts.",
)


def _slug(label: str) -> str:
    return label.lower().replace(" — ", "-").replace(" ", "-")


def _pick_folder() -> str | None:
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory()
        root.destroy()
        return folder or None
    except Exception:
        return None


labels = [s.label for s in SITES]
choice = st.selectbox("Site", labels)
site = next(s for s in SITES if s.label == choice)

if st.session_state.get("scraped_for") != choice:
    st.session_state.scraped = None


def _enrich_and_photo(person):
    if site.enrich and person.source_url:
        try:
            site.enrich(engine.fetch_html(person.source_url), person)
        except engine.FetchError:
            pass
    if person.photo_url:
        person.photo_b64 = photos.embed(person.photo_url)
    person.category = site.tag
    return person


if st.button("⬇️ Scrape Now", type="primary", use_container_width=True):
    try:
        with st.spinner(f"Fetching {choice}…"):
            people = site.adapter(engine.fetch_html(site.url), site.url)
    except engine.FetchError as exc:
        st.error(f"Could not fetch the page: {exc}")
        people = []

    if not people:
        st.warning("0 people found — the site's markup may have changed.")
    else:
        progress = st.progress(0.0, text="Starting…")
        log_area = st.empty()
        logs: list[str] = []
        started = time.time()
        total = len(people)
        done = 0
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(_enrich_and_photo, p): p for p in people}
            for future in cf.as_completed(futures):
                person = futures[future]
                done += 1
                try:
                    future.result()
                    extras = "📧" if person.email else ""
                    logs.append(f"✓ {done}/{total}  {person.name} {extras}")
                except Exception as exc:
                    logs.append(f"✗ {done}/{total}  {person.name} — {exc}")
                elapsed = time.time() - started
                eta = (elapsed / done) * (total - done)
                progress.progress(done / total,
                                  text=f"{done}/{total} · ETA {int(eta // 60)}:{int(eta % 60):02d}")
                log_area.code("\n".join(logs[-15:]))
        st.session_state.scraped = people
        st.session_state.scraped_for = choice
        st.success(f"Built {total} contacts, tagged “{site.tag}”.")

scraped = st.session_state.get("scraped")
if scraped:
    st.subheader("Export")
    fmt = st.selectbox("Format", list(exporters.EXPORTERS))
    export = exporters.EXPORTERS[fmt](scraped)

    default_path = str(Path("contacts") / f"{_slug(choice)}-{date.today().isoformat()}.{export.ext}")
    saved = st.session_state.get("save_dir")
    default = str(Path(saved) / Path(default_path).name) if saved else default_path
    path = st.text_input("Save path", value=default, key=f"path_{export.ext}")

    col1, col2 = st.columns(2)
    if col1.button("📁 Browse…", use_container_width=True):
        folder = _pick_folder()
        if folder:
            st.session_state.save_dir = folder
            st.rerun()
        else:
            st.caption("Folder dialog unavailable — type a path above.")
    if col2.button("💾 Save file", use_container_width=True):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(export.data)
        st.success(f"Saved {len(scraped)} contacts to {path}")

    st.download_button(f"Download {fmt}", export.data,
                       file_name=Path(default_path).name, mime=export.mime,
                       use_container_width=True)

_matches = list(PREVIEW_DIR.glob(f"{_slug(choice)}.*"))
with st.expander("🖼️ Page preview", expanded=not scraped):
    if _matches:
        st.image(str(_matches[0]), caption=f"Preview · {site.url}", use_container_width=True)
    else:
        st.info("No local preview image for this site.")
