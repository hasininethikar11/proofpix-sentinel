const API_BASE = "http://127.0.0.1:8000";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === "PROOFPIX_ANALYZE" && typeof message.url === "string") {
    analyze(message.url).then(sendResponse).catch(() => sendResponse({
      url: message.url, category: "ANALYSIS_UNAVAILABLE", score: 0,
      reasons: ["The local analysis service could not be reached. The destination was not automatically opened."]
    }));
    return true;
  }
  if (message?.type === "PROOFPIX_SHOW_WARNING" && message.result) {
    const warningId = crypto.randomUUID();
    chrome.storage.session.set({ [warningId]: message.result }).then(() => {
      chrome.tabs.create({ url: chrome.runtime.getURL(`warning.html?id=${warningId}`) });
    }).catch(() => {
      chrome.tabs.create({ url: chrome.runtime.getURL("warning.html") });
    });
    return;
  }
  if (message?.type === "PROOFPIX_ENABLE_TAB" && Number.isInteger(message.tabId)) {
    chrome.scripting.executeScript({ target: { tabId: message.tabId }, files: ["content.js"] })
      .then(() => sendResponse({ ok: true }))
      .catch(() => sendResponse({ ok: false, error: "Chrome cannot inject the checker into this page. Try a regular website tab." }));
    return true;
  }
});

async function analyze(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }), signal: controller.signal
    });
    if (!response.ok) throw new Error(`API returned ${response.status}`);
    const data = await response.json();
    if (!data || typeof data.category !== "string" || !Array.isArray(data.reasons)) throw new Error("Invalid API response");
    return data;
  } finally { clearTimeout(timeout); }
}
