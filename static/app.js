
const form = document.getElementById("scan-form");
const targetInput = document.getElementById("target-url");
const scanButton = document.getElementById("scan-button");
const buttonLabel = document.getElementById("button-label");
const message = document.getElementById("message");
const results = document.getElementById("results");
const scanMeta = document.getElementById("scan-meta");
const downloadButton = document.getElementById("download-button");
const findingsList = document.getElementById("findings-list");

let latestScan = null;

function showMessage(text, type = "info") {
    message.textContent = text;
    message.className = `message ${type}`;
}

function updateCount(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value);
}

function renderFindings(findings = []) {
    findingsList.replaceChildren();

    if (findings.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "No findings were returned for this scan.";
        findingsList.appendChild(empty);
        return;
    }

    findings.forEach((finding) => {
        const card = document.createElement("article");
        card.className = "finding-card";

        const heading = document.createElement("div");
        heading.className = "finding-heading";

        const category = document.createElement("h3");
        category.textContent = finding.category || "General";

        const badge = document.createElement("span");
        const severity = String(finding.severity || "info").toLowerCase();
        badge.className = `severity-badge ${severity}`;
        badge.textContent = finding.status || finding.severity || "INFO";

        heading.append(category, badge);

        const details = document.createElement("p");
        details.textContent = finding.details || "No additional details.";

        const recommendation = document.createElement("p");
        recommendation.className = "recommendation";
        recommendation.textContent =
            `Recommendation: ${finding.recommendation || "Review this finding."}`;

        card.append(heading, details, recommendation);
        findingsList.appendChild(card);
    });
}

function displayScan(data) {
    latestScan = data;

    const findings = Array.isArray(data.findings) ? data.findings : [];
    const passed = findings.filter(
        (item) => String(item.status).toUpperCase() === "PASS"
    ).length;
    const warnings = findings.filter(
        (item) => String(item.status).toUpperCase() === "WARNING"
    ).length;
    const reviews = findings.filter(
        (item) => String(item.status).toUpperCase() === "REVIEW"
    ).length;

    updateCount("total-count", findings.length);
    updateCount("passed-count", passed);
    updateCount("warning-count", warnings);
    updateCount("review-count", reviews);

    const statusElement = document.getElementById("http-status");
    if (statusElement) {
        statusElement.textContent =
            data.status_code != null ? String(data.status_code) : "N/A";
    }

    scanMeta.textContent =
        `Target: ${data.final_url || data.target || "Unknown target"} · ` +
        `Scanned at: ${data.scanned_at_utc || "N/A"}`;

    renderFindings(findings);
    results.hidden = false;
    downloadButton.disabled = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const url = targetInput.value.trim();

    if (!url) {
        showMessage("Please enter a website URL.", "error");
        targetInput.focus();
        return;
    }

    scanButton.disabled = true;
    buttonLabel.textContent = "Scanning...";
    results.hidden = true;
    downloadButton.disabled = true;
    showMessage("Checking the target website. Please wait...", "info");

    try {
        const response = await fetch("/api/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Scan failed (HTTP ${response.status}).`);
        }

        displayScan(data);
        showMessage("Scan completed successfully.", "success");
    } catch (error) {
        showMessage(
            error.message || "Something went wrong. Please try again.",
            "error"
        );
    } finally {
        scanButton.disabled = false;
        buttonLabel.textContent = "Run Security Scan";
    }
});

downloadButton.addEventListener("click", () => {
    if (!latestScan) return;

    const blob = new Blob([JSON.stringify(latestScan, null, 2)], {
        type: "application/json",
    });

    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = "security-scan-report.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(objectUrl);
});