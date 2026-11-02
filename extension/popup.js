const button = document.getElementById("enable");
const status = document.getElementById("status");
const error = document.getElementById("error");
button.addEventListener("click", async () => {
  button.disabled = true; error.textContent = ""; status.textContent = "Enabling link checking…";
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) throw new Error("No active tab was found.");
    const result = await chrome.runtime.sendMessage({ type: "PROOFPIX_ENABLE_TAB", tabId: tab.id });
    if (!result?.ok) throw new Error(result?.error || "Could not enable checking on this tab.");
    status.textContent = "Link checking is enabled for this tab until it is reloaded.";
    button.textContent = "Enabled on this tab";
  } catch (e) { status.textContent = "Could not enable checking."; error.textContent = String(e.message || e); button.disabled = false; }
});
