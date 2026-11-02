# Architecture

1. The user explicitly clicks the extension toolbar action to enable checking on the current tab. The extension uses `activeTab` and `scripting` permissions rather than automatically inspecting every website.
2. A content script intercepts ordinary left-clicks on HTTP(S) links in that tab and asks the extension service worker to check the destination.
3. The service worker sends the URL to the local FastAPI service at `127.0.0.1:8000`.
4. The service validates and normalizes the URL, applies transparent heuristics, and returns a category, score, and reason list.
5. Risky or unavailable results show a warning page. The user can go back or explicitly continue.

## Categories
- `CONFIRMED_THREAT`: synthetic demo fixture only; not a real external confirmation.
- `HIGH_RISK`: several strong heuristic indicators.
- `SUSPICIOUS`: one or more heuristic indicators.
- `NO_KNOWN_THREAT`: no configured heuristic fired; not proof of safety.
- `ANALYSIS_UNAVAILABLE`: local API could not be reached or did not return a valid result.

## Threat model and limitations
The system does not download page content, inspect certificates, query a reputation database, or detect all phishing/malware. URL text can be deceptive. Redirects may lead somewhere else. Some legitimate URLs may be flagged. Browser and OS security features remain necessary.
