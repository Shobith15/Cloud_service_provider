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
