const params = new URLSearchParams(location.search);
let result = null;
let safeUrl = "";
const warningId = params.get("id");
const heading = document.getElementById("heading");
const category = document.getElementById("category");
const summary = document.getElementById("summary");
const reasons = document.getElementById("reasons");
const destination = document.getElementById("destination");

function renderResult() {
  const categories = {
    CONFIRMED_THREAT: "Synthetic demo fixture",
    HIGH_RISK: "High risk indicators",
    SUSPICIOUS: "Suspicious indicators",
    ANALYSIS_UNAVAILABLE: "Analysis unavailable"
  };
  if (!result) {
    result = { category: "ANALYSIS_UNAVAILABLE", reasons: ["No analysis details were provided."] };
  }
  category.textContent = categories[result.category] || result.category || "Review this link";
  summary.textContent = result.category === "ANALYSIS_UNAVAILABLE"
    ? "The checker could not verify this link. It has not been opened automatically."
    : `Heuristic score: ${Number(result.score) || 0}/100. This is not a definitive verdict.`;
  reasons.replaceChildren();
  for (const reason of (Array.isArray(result.reasons) ? result.reasons : [])) {
    const li = document.createElement("li");
    li.textContent = String(reason);
    reasons.appendChild(li);
  }
  safeUrl = "";
  try {
    const u = new URL(result.url);
    if (["http:", "https:"].includes(u.protocol)) {
      u.username = "";
      u.password = "";
      safeUrl = u.href;
    }
  } catch {}
  destination.textContent = safeUrl ? `Destination: ${safeUrl}` : "Destination details unavailable";
  document.getElementById("continue").disabled = !safeUrl;
}

document.getElementById("back").addEventListener("click", () => window.close());
document.getElementById("continue").addEventListener("click", () => {
  if (safeUrl) location.href = safeUrl;
});

if (warningId) {
  chrome.storage.session.get(warningId).then((items) => {
    result = items[warningId] || null;
    renderResult();
    chrome.storage.session.remove(warningId);
  }).catch(() => renderResult());
} else {
  renderResult();
}
