# Euystacio-Helmi AI: Build & Run Instructions for `app.py`

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```
This will install Flask, Flask-SocketIO, eventlet, and other Python dependencies.

## 2. Set Environment Variables (Optional)

For production:
```bash
export FLASK_ENV=production
export PORT=80
```
For development:
```bash
export FLASK_ENV=development
```

## 3. Run the Backend Server

### Direct (Flask Development Server)
```bash
python app.py
```
This starts the API backend and SocketIO server on port 5000 by default.

### Production (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:80 app:app
```

## 4. Frontend/Rendering

- Place your frontend files (HTML, JS, CSS) in the `/static` or `/templates` directory.
- For dynamic rendering, Flask uses `render_template` on files in `/templates`.
- For direct serving, static files in `/static` are accessible at `http://localhost:5000/static/...`.

## 5. Health Check

You can verify the backend is running with:
```bash
curl http://localhost:5000/api/status
```
and other endpoints like `/api/data`, `/api/suggestions`.

## 6. Directory Structure Reference

```
euystacio-helmi-AI/
├── app.py                # Main Flask/SocketIO backend
├── requirements.txt      # Python dependencies
├── static/               # Static assets (css, js, images)
├── templates/            # Jinja2/Flask templates (e.g. index.html)
└── ...                   # Other project files
```

## 7. Rendering Instructions

- For REST API only: Use endpoints via HTTP requests (see `/api/status`, `/api/data`, etc.).
- For web UI: Add HTML templates to `/templates`, then use Flask’s `render_template()` in routes.
- For realtime features: Use Socket.IO in your frontend JS to connect to the backend’s WebSocket.

---

**Summary:**  
- `app.py` is started with `python app.py` (development) or `gunicorn ...` (production).
- Static files: `/static`
- Templates: `/templates`
- Integrate frontend by placing files in those directories and adding Flask route logic for rendering.