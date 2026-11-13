const byId = (id) => document.getElementById(id);

function setProgress(id, value) {
    const safeValue = Math.max(0, Math.min(100, Number(value) || 0));
    byId(id).style.width = `${safeValue}%`;
}

function renderDisks(disks) {
    byId("disk-list").innerHTML = disks.map(disk => {
        if (disk.error) {
            return `<div class="disk-row disk-error">${disk.mount}: ${disk.error}</div>`;
        }

        return `
            <div class="disk-row">
                <div class="disk-meta">
                    <strong>${disk.mount}</strong>
                    <span>${disk.used_gb} / ${disk.total_gb} GB · ${disk.percent}%</span>
                </div>
                <div class="disk-track">
                    <div class="disk-fill" style="width:${Math.min(100, disk.percent)}%"></div>
                </div>
            </div>`;
    }).join("");
}

function renderServices(services) {
    byId("service-list").innerHTML = Object.entries(services).map(([name, status]) => `
        <div class="service-row">
            <strong>${name}</strong>
            <span class="status ${status === "Running" ? "" : "bad"}">${status}</span>
        </div>`).join("");
}

function renderCustomers(customers) {
    byId("customer-list").innerHTML = customers.map(customer => `
        <div class="customer-row">
            <div>
                <strong>${customer.name}</strong>
                <span class="customer-detail">${customer.directory}</span>
            </div>
            <span class="status ${customer.website_present ? "" : "bad"}">
                ${customer.website_present ? "Website ready" : "Missing index"}
            </span>
        </div>`).join("");
}

function renderBackups(data) {
    if (!data.available) {
        byId("backup-list").textContent = "Backup directory is not accessible.";
        return;
    }

    if (!data.backups.length) {
        byId("backup-list").textContent = "No backups found.";
        return;
    }

    byId("backup-list").innerHTML = data.backups.map(backup => `
        <div class="backup-row">
            <strong>${backup.name}</strong>
            <span class="backup-detail">${new Date(backup.created).toLocaleString()}</span>
        </div>`).join("");
}

async function refreshDashboard() {
    try {
        const response = await fetch("/api/overview", { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        const system = data.system;

        byId("hostname").textContent = system.hostname;
        byId("cpu").textContent = `${system.cpu_percent}%`;
        setProgress("cpu-bar", system.cpu_percent);

        byId("memory").textContent = `${system.memory.percent}%`;
        byId("memory-detail").textContent =
            `${system.memory.used_gb} / ${system.memory.total_gb} GB RAM`;
        setProgress("memory-bar", system.memory.percent);

        byId("uptime").textContent = `${system.uptime_hours} hrs`;
        byId("site-count").textContent =
            data.customers.filter(c => c.website_present).length;

        byId("last-updated").textContent =
            `Updated ${new Date(system.timestamp).toLocaleTimeString()}`;

        renderDisks(data.disks);
        renderServices(data.services);
        renderCustomers(data.customers);
        renderBackups(data.backups);

        byId("vg-info").textContent = data.storage.data_disk;
        byId("lv-info").textContent = data.storage.logical_volumes;
    } catch (error) {
        byId("last-updated").textContent = "Connection error";
        console.error("CloudGuard dashboard:", error);
    }
}

refreshDashboard();
setInterval(refreshDashboard, 15000);

// ================= SUPPORT TICKET MANAGEMENT =================

function escapeSupportHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

function renderSupportTickets(tickets) {
    const container = byId("support-list");
    const summary = byId("support-summary");

    if (!Array.isArray(tickets)) {
        summary.textContent = "Unexpected response from support service.";
        container.innerHTML = "";
        return;
    }

    const open = tickets.filter(ticket => ticket.status === "Open").length;
    const progress = tickets.filter(ticket => ticket.status === "In Progress").length;
    const resolved = tickets.filter(ticket => ticket.status === "Resolved").length;

    summary.textContent =
        `${tickets.length} total · ${open} open · ${progress} in progress · ${resolved} resolved`;

    if (tickets.length === 0) {
        container.innerHTML = '<p class="support-empty">No support tickets yet.</p>';
        return;
    }

    container.innerHTML = tickets.map(ticket => {
        const id = Number(ticket.id);

        if (!Number.isSafeInteger(id) || id < 1) return "";

        const status = ["Open", "In Progress", "Resolved"].includes(ticket.status)
            ? ticket.status
            : "Open";

        return `
            <article class="support-ticket" data-ticket-id="${id}">
                <div class="support-ticket-header">
                    <div>
                        <strong>Ticket #${id} — ${escapeSupportHtml(ticket.subject)}</strong>
                        <div class="support-ticket-meta">
                            ${escapeSupportHtml(ticket.customer)} ·
                            ${escapeSupportHtml(ticket.name)} ·
                            ${escapeSupportHtml(ticket.email)}
                        </div>
                    </div>
                    <span class="ticket-status">${escapeSupportHtml(status)}</span>
                </div>

                <p class="support-message">${escapeSupportHtml(ticket.message)}</p>

                <div class="support-ticket-meta">
                    Submitted: ${escapeSupportHtml(
                        ticket.created_at
                            ? new Date(ticket.created_at).toLocaleString()
                            : "Unknown"
                    )}
                </div>

                <div class="support-ticket-form">
                    <label>
                        Status
                        <select class="ticket-status-select">
                            ${["Open", "In Progress", "Resolved"].map(option =>
                                `<option value="${option}" ${status === option ? "selected" : ""}>${option}</option>`
                            ).join("")}
                        </select>
                    </label>

                    <label>
                        Administrator reply
                        <textarea class="ticket-reply" maxlength="2000"
                            placeholder="Write a response to the customer...">${escapeSupportHtml(ticket.admin_reply || "")}</textarea>
                    </label>

                    <button type="button" class="ticket-save">Save Changes</button>
                    <span class="ticket-feedback" aria-live="polite"></span>
                </div>
            </article>
        `;
    }).join("");
}

async function refreshSupport() {
    const container = byId("support-list");

    try {
        const response = await fetch("/api/support", { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const tickets = await response.json();
        renderSupportTickets(tickets);
    } catch (error) {
        byId("support-summary").textContent = "Unable to load support requests.";
        container.innerHTML =
            '<p class="support-error">Support service connection failed. Please refresh.</p>';
        console.error("CloudGuard support:", error);
    }
}

async function saveSupportTicket(ticketElement) {
    const id = ticketElement.dataset.ticketId;
    const status = ticketElement.querySelector(".ticket-status-select").value;
    const reply = ticketElement.querySelector(".ticket-reply").value;
    const button = ticketElement.querySelector(".ticket-save");
    const feedback = ticketElement.querySelector(".ticket-feedback");

    button.disabled = true;
    feedback.textContent = "Saving...";

    try {
        const response = await fetch(`/api/support/${encodeURIComponent(id)}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                status: status,
                admin_reply: reply
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || `HTTP ${response.status}`);
        }

        feedback.textContent = "Saved successfully.";
        await refreshSupport();
    } catch (error) {
        feedback.textContent = `Save failed: ${error.message}`;
        console.error("CloudGuard ticket update:", error);
    } finally {
        button.disabled = false;
    }
}

byId("refresh-support").addEventListener("click", refreshSupport);

byId("support-list").addEventListener("click", event => {
    const button = event.target.closest(".ticket-save");
    if (!button) return;

    const ticket = button.closest(".support-ticket");
    if (ticket) saveSupportTicket(ticket);
});

refreshSupport();
setInterval(refreshSupport, 15000);
