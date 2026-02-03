# URL Shortener (Mini Demo)

A tiny URL shortener demo built with Python’s built-in HTTP server and a few static HTML pages.

## What It Does
- Serves a simple form at `/` for submitting a URL
- Redirects known paths (like `/about` and `/contact`) via a `POST /shorten` request
- Returns `404` for unknown URLs

## Run It
```bash
python3 server.py
```

Then open:
- `http://localhost:8080/`

## Files
- `server.py` — HTTP server and routing logic
- `src/index.html` — landing page + form
- `src/about.html` — about page
- `src/contact.html` — contact page
