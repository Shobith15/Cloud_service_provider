const money = amount =>
    new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(amount);

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

async function loadPortal() {
    try {
        const response = await fetch("/api/portal", { cache: "no-store" });
        if (!response.ok) throw new Error("Portal API unavailable");

        const data = await response.json();

        document.getElementById("welcome").textContent =
            `Welcome, ${data.name}`;

        document.getElementById("customer-domain").textContent = data.domain;
        document.getElementById("website-domain").textContent = data.domain;
        document.getElementById("plan-name").textContent = data.plan;
        document.getElementById("plan-price").textContent = money(data.price);
        document.getElementById("website-status").textContent = data.website.status;
        document.getElementById("response-time").textContent =
            data.website.response_ms === null
                ? "Response time unavailable"
                : `${data.website.response_ms} ms response time`;

        document.getElementById("billing-status").textContent =
            data.billing.status;
        document.getElementById("next-due").textContent =
            `Next due: ${data.billing.next_due}`;

        document.getElementById("website-detail").textContent =
            data.website.status;

        document.getElementById("website-response").textContent =
            data.website.response_ms === null
                ? "Response time unavailable"
                : `Response time: ${data.website.response_ms} ms`;

        const dot = document.getElementById("website-dot");
        dot.classList.toggle("bad", data.website.status !== "Online");

        const used = Number(data.storage.used_gb);
        const limit = Number(data.storage.limit_gb);
        const percentage = limit > 0
            ? Math.min(100, (used / limit) * 100)
            : 0;

        document.getElementById("storage-used").textContent = `${used} GB`;
        document.getElementById("storage-limit").textContent = `of ${limit} GB`;
        document.getElementById("storage-bar").style.width = `${percentage}%`;
        document.getElementById("storage-note").textContent =
            `${percentage.toFixed(1)}% of allocated hosting storage used`;

        document.getElementById("invoice-list").innerHTML =
            data.invoices.map(invoice => `
                <tr>
                    <td>${escapeHtml(invoice.id)}</td>
                    <td>${escapeHtml(invoice.date)}</td>
                    <td>${money(invoice.amount)}</td>
                    <td>
                        <span class="status ${invoice.status === "Pending" ? "pending" : ""}">
                            ${escapeHtml(invoice.status)}
                        </span>
                    </td>
                </tr>
            `).join("");

    } catch (error) {
        document.getElementById("welcome").textContent =
            "Portal temporarily unavailable";
        document.getElementById("website-status").textContent = "Unavailable";
        document.getElementById("billing-status").textContent = "Unavailable";
        console.error(error);
    }
}

document.getElementById("support-form").addEventListener("submit", async event => {
    event.preventDefault();

    const form = event.currentTarget;
    const button = document.getElementById("submit-button");
    const message = document.getElementById("form-message");

    button.disabled = true;
    button.textContent = "Submitting...";
    message.textContent = "";
    message.classList.remove("error");

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/api/support", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Unable to submit request");
        }

        message.textContent =
            `Request #${result.request_id} submitted successfully.`;
        form.reset();

    } catch (error) {
        message.textContent = error.message;
        message.classList.add("error");
    } finally {
        button.disabled = false;
        button.textContent = "Submit request";
    }
});

loadPortal();
setInterval(loadPortal, 15000);
