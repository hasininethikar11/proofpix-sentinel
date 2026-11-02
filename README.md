# PROOFPIX SENTINEL (prototype)

An opt-in Chrome Manifest V3 extension prototype that checks a link before navigating and explains why a URL may deserve caution. A local FastAPI service performs heuristic analysis. It is an educational prototype, **not** a guaranteed malware/phishing detector.

## Privacy and limitations
- Checking is enabled only on a tab when you click the extension's toolbar button.
- URLs checked by the extension are sent to the local service at `127.0.0.1:8000`; do not use this prototype with sensitive URLs.
- No external threat-intelligence service is contacted.
- `example.com`, `example.net`, and `example.org` are reserved documentation domains and are not treated as malicious. The `malware-test.example.com` fixture uses the reserved `example.com` documentation domain is a demonstration-only synthetic result, not a real threat verdict.
- Heuristics can miss threats and flag harmless URLs. A “no known threat” result is not a guarantee of safety.
- Browser extension code has not undergone an independent security audit.

## Requirements
- Python 3.10+ (Python 3.11 or 3.12 recommended)
- Google Chrome or Chromium
- VS Code is optional

## Start the local backend on Windows
Easiest method: double-click `setup_windows.bat` in the project root. It creates a virtual environment, installs dependencies, and runs the backend tests. Once it finishes, double-click `run_backend.bat` to start the local API.

Manual method: open PowerShell in the `backend` folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If PowerShell blocks activation, use this command for the current terminal only, then activate again:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

Keep the terminal running. Open `http://127.0.0.1:8000/health` to check the service.

## Load the extension
1. Open `chrome://extensions` in Chrome.
2. Turn on **Developer mode**.
3. Choose **Load unpacked** and select the `extension` folder in this project.
4. Pin PROOFPIX SENTINEL if desired.
5. Visit a page with links, then click the extension toolbar button to enable checking on that tab.
6. Click a link on that tab. The extension pauses navigation while the local service checks it.

The extension requires the local backend to be running. If the backend cannot be reached, the extension shows an “analysis unavailable” warning rather than silently treating the URL as safe.

## API
- `GET /health` — service health
- `POST /analyze` with `{"url":"https://example.org"}` — heuristic result

## Test fixture
`https://malware-test.example.com/` is a synthetic fixture on the reserved `example.com` documentation domain that returns a demonstration-only `CONFIRMED_THREAT` result. It is **not** an actual malware test site and should never be described as one.

## Project layout
- `backend/app/` — API, URL analysis, and schemas
- `backend/tests/` — automated tests
- `extension/` — Chrome extension
- `docs/` — architecture and manual testing notes
