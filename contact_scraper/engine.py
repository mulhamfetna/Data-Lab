import shutil

import requests

CHROME_PATH = shutil.which("google-chrome") or "/usr/bin/google-chrome"
_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


class FetchError(Exception):
    pass


def fetch_html(url: str, *, timeout: int = 20) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": _UA}, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException as exc:
        raise FetchError(str(exc)) from exc


_SCROLL_JS = """async () => {
  await new Promise((resolve) => {
    let y = 0;
    const step = 700;
    const timer = setInterval(() => {
      window.scrollBy(0, step);
      y += step;
      if (y >= document.body.scrollHeight) { clearInterval(timer); resolve(); }
    }, 120);
  });
}"""


def screenshot(url: str, *, timeout: int = 60_000, full_page: bool = True,
               wait_selector: str | None = None) -> bytes | None:
    """Render a fully-loaded page and return a PNG (None on any failure).

    Some sites (e.g. Safierr) serve a JS "Loading…" interstitial that navigates to the
    real page once a challenge passes. Passing `wait_selector` (a CSS selector for real
    content) makes the capture wait for that content before shooting, so it never catches
    the interstitial or a skeleton. Then it scrolls to pull in lazy images and settles.
    """
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=CHROME_PATH)
            page = browser.new_context(
                user_agent=_UA, viewport={"width": 1366, "height": 900}).new_page()
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=timeout, state="attached")
                except Exception:
                    pass  # fall back to time-based settling below
            try:
                page.wait_for_load_state("networkidle", timeout=15_000)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            try:
                page.evaluate(_SCROLL_JS)      # pull lazy images into view
                page.wait_for_timeout(2000)    # let them finish decoding
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(500)
            except Exception:
                pass  # navigation mid-scroll — capture what we have
            png = page.screenshot(full_page=full_page)
            browser.close()
            return png
    except Exception:
        return None
