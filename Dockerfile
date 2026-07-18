FROM python:3.13-slim

# Small, offline-safe image. No system Chrome/Playwright is installed here: the .sy scraper
# targets are geo-blocked outside Syria anyway, so that demo is intentionally local-only.
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user (hosts like Hugging Face Spaces require it).
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8501
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "Home.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
