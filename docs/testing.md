# Testing checklist

## Automated tests
From the `backend` directory with the virtual environment active: `python -m pytest -q`.

## API smoke test
Start the API with `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`, then visit `http://127.0.0.1:8000/health`. Expected JSON includes `"status":"ok"`.

PowerShell request example:
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/analyze -ContentType 'application/json' -Body '{"url":"https://example.org"}'
```

## Manual extension tests
1. Load the `extension` folder using `chrome://extensions` → Developer mode → Load unpacked.
2. Start the backend first.
3. Open a page containing ordinary links and click the extension action. It should report that checking is enabled for this tab.
4. Click a normal HTTPS link; the extension should check it before navigating.
5. Check `https://malware-test.example.com/`; it should show the synthetic demonstration warning.
6. Stop the backend and click a link; an analysis-unavailable warning should appear rather than silently passing it through.
7. Try keyboard/middle-click behavior, downloads, links opened by scripts, redirects, and browser-specific cases. These may not be intercepted by this prototype and are not covered by automated browser tests.

Do not test using real malware, credential theft pages, or private URLs.
