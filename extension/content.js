(() => {
  if (window.__proofpixSentinelInstalled) return;
  window.__proofpixSentinelInstalled = true;

  document.addEventListener("click", async (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = event.target instanceof Element ? event.target : null;
    const anchor = target?.closest("a[href]");
    if (!anchor || anchor.hasAttribute("download") || anchor.target === "_blank") return;
    let destination;
    try { destination = new URL(anchor.href); } catch { return; }
    if (!(["http:", "https:"].includes(destination.protocol))) return;
    if (destination.origin === location.origin && destination.href === location.href) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    const originalHref = anchor.href;
    const result = await new Promise((resolve) => {
      const timer = setTimeout(() => resolve({ category: "ANALYSIS_UNAVAILABLE", score: 0, url: originalHref, reasons: ["The check did not return in time. The link was not automatically opened."] }), 6000);
      chrome.runtime.sendMessage({ type: "PROOFPIX_ANALYZE", url: originalHref }, (response) => {
        clearTimeout(timer);
        if (chrome.runtime.lastError || !response) {
          resolve({ category: "ANALYSIS_UNAVAILABLE", score: 0, url: originalHref, reasons: ["The local checker is unavailable. The link was not automatically opened."] });
        } else resolve(response);
      });
    });

    if (result.category === "NO_KNOWN_THREAT") {
      // The heuristic found no configured indicator. This is not a safety guarantee.
      location.href = originalHref;
    } else {
      chrome.runtime.sendMessage({ type: "PROOFPIX_SHOW_WARNING", result, originalTabId: null });
    }
  }, true);
})();
