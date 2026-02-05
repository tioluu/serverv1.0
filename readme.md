# URL Shortener (Mini Demo)

A tiny URL shortener demo built with Python’s built-in HTTP server and a small HTML/CSS/JS frontend.

## What It Does
- Serves a simple form at `/` for submitting a URL
- Sends `POST /shorten` to an external shortener API and returns the JSON response
- Displays the short link on the page via JavaScript

## Run It
```bash
pip install -r requirements.txt
python3 server.py
```

Then open:
- `http://localhost:8080/`

## Environment
Create a `.env` file and set your API key:
```bash
SPOO_API_KEY=your_key_here
```

## Files
- `server.py` — HTTP server and API proxy
- `src/index.html` — landing page + form
- `src/style.css` — page styles
- `src/script.js` — client-side form handling and rendering
- `run.sh` — convenience script to run the server
