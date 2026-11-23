// ---------------------------------------------------------------------------
// SecureScan – frontend client
// ---------------------------------------------------------------------------

function showMessage(text, type) {
    const el = document.getElementById("message");
    el.textContent = text;
    el.className = "message " + type;
}

function hideMessage() {
    const el = document.getElementById("message");
    el.className = "message hidden";
}

// Build a single finding card using textContent only (no innerHTML).
function renderFinding(f) {
    const card = document.createElement("div");
    card.className = "finding-card bg-[#1F2937] rounded-lg p-4 shadow mb-3";

    // Status + severity line
    const top = document.createElement("div");
    top.className = "flex items-center gap-2 mb-1";

    const statusBadge = document.createElement("span");
    statusBadge.className = "severity-badge " + (f.status || "").toLowerCase();
    statusBadge.textContent = f.status || "";
    top.appendChild(statusBadge);

    const sevBadge = document.createElement("span");
    sevBadge.className = "severity-badge " + (f.severity || "").toLowerCase();
    sevBadge.textContent = f.severity || "";
    top.appendChild(sevBadge);

    card.appendChild(top);

    // Category heading
    const heading = document.createElement("h4");
    heading.className = "finding-heading text-[#E5E7EB] mt-1 font-medium";
    heading.textContent = f.category || "";
    card.appendChild(heading);

    // Details
    const details = document.createElement("p");
    details.className = "text-[#9CA3AF] mt-1 text-sm";
    details.textContent = f.details || "";
    card.appendChild(details);

    // Recommendation (if any)
    if (f.recommendation) {
        const rec = document.createElement("p");
        rec.className = "recommendation text-[#06B6D4] mt-1 text-sm italic";
        rec.textContent = f.recommendation;
        card.appendChild(rec);
    }

    return card;
}

// ---------------------------------------------------------------------------
// Form submit handler
// ---------------------------------------------------------------------------
document.getElementById("scan-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    hideMessage();

    var urlInput = document.getElementById("target-url");
    var button   = document.getElementById("scan-button");
    var label    = document.getElementById("button-label");
    var originalText = label.textContent;

    // Auto-prepend https:// if the user forgot
    var targetUrl = urlInput.value.trim();
    if (!/^https?:\/\//i.test(targetUrl)) {
        targetUrl = "https://" + targetUrl;
    }

    button.disabled = true;
    label.textContent = "Scanning\u2026";

    try {
        var resp = await fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: targetUrl }),
        });

        var data = await resp.json();

        if (!resp.ok) {
            showMessage(data.error || "Unexpected error", "error");
            return;
        }

        // --- Show results section ---
        document.getElementById("results").hidden = false;

        // HTTP status pill (inside the findings panel)
        var statusPill = document.getElementById("http-status-pill");
        if (statusPill) {
            statusPill.textContent = "HTTP " + (data.status_code || "—");
        }

        // Scan meta line
        var meta = document.getElementById("scan-meta");
        if (meta) {
            meta.textContent = data.target + " \u00b7 " +
                new Date(data.scanned_at_utc).toLocaleString();
        }

        // --- Compute summary from findings ---
        var findings = data.findings || [];
        var passed   = 0;
        var warnings = 0;
        var review   = 0;
        findings.forEach(function (f) {
            if (f.status === "PASS")    passed++;
            if (f.status === "WARNING") warnings++;
            if (f.status === "REVIEW")  review++;
        });

        document.getElementById("total-count").textContent   = findings.length;
        document.getElementById("passed-count").textContent  = passed;
        document.getElementById("warning-count").textContent = warnings;
        document.getElementById("review-count").textContent  = review;

        // Render each finding card
        var list = document.getElementById("findings-list");
        list.textContent = "";          // clear previous results (no innerHTML)
        findings.forEach(function (f) {
            list.appendChild(renderFinding(f));
        });

        // Enable JSON download
        var dlBtn = document.getElementById("download-button");
        var blob  = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
        dlBtn.disabled = false;
        dlBtn.onclick = function () {
            var a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "securescan-" + Date.now() + ".json";
            a.click();
        };

        showMessage("Scan completed successfully!", "success");

    } catch (err) {
        showMessage("Could not reach the server \u2013 please try again later.", "error");
    } finally {
        button.disabled = false;
        label.textContent = originalText;
    }
});
