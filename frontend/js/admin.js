const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
    // Basic auth check
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("user_role");
    
    if (!token || role !== "admin") {
        alert("Access denied. Admins only.");
        window.location.href = "index.html";
        return;
    }
    const adminName = localStorage.getItem("user_name") || "Admin";
    document.getElementById("adminNameDisplay").textContent = adminName;
    document.querySelector(".navbar-user-avatar").textContent = adminName.charAt(0).toUpperCase();
    const navLinks = document.querySelectorAll('.sidebar-nav a[data-view]');
    const views = document.querySelectorAll('.admin-view');
    const viewTitle = document.getElementById('viewTitle');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const targetView = link.getAttribute('data-view');
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(`${targetView}View`).classList.add('active');

            if (targetView === 'dashboard') {
                viewTitle.textContent = 'Dashboard Overview';
                fetchDashboardStats();
            } else if (targetView === 'reports') {
                viewTitle.textContent = 'Reports Management';
                fetchReports();
            }
        });
    });
    document.getElementById('adminLogoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_name");
        localStorage.removeItem("user_role");
        window.location.href = "index.html";
    });
    fetchDashboardStats();
});

async function fetchDashboardStats() {
    try {
        const res = await fetch(`${API_BASE}/admin/dashboard`, {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });
        if (!res.ok) throw new Error("Failed to fetch stats");
        const data = await res.json();
        
        const grid = document.getElementById('statsGrid');
        grid.innerHTML = `
            <div class="stat-card">
                <div class="stat-icon bg-primary-light"><i class="bi bi-file-earmark-text text-primary"></i></div>
                <div class="stat-details">
                    <h3>${data.total_reports}</h3>
                    <p>Total Reports</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon bg-warning-light"><i class="bi bi-clock-history text-warning"></i></div>
                <div class="stat-details">
                    <h3>${data.pending_reports}</h3>
                    <p>Pending</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon bg-success-light"><i class="bi bi-check-circle text-success"></i></div>
                <div class="stat-details">
                    <h3>${data.resolved_reports}</h3>
                    <p>Resolved</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon bg-danger-light"><i class="bi bi-exclamation-triangle text-danger"></i></div>
                <div class="stat-details">
                    <h3>${data.high_priority_reports}</h3>
                    <p>High Priority</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon bg-info-light"><i class="bi bi-people text-info"></i></div>
                <div class="stat-details">
                    <h3>${data.total_users}</h3>
                    <p>Total Users</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon bg-secondary-light"><i class="bi bi-building text-secondary"></i></div>
                <div class="stat-details">
                    <h3>${data.total_departments}</h3>
                    <p>Departments</p>
                </div>
            </div>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById('statsGrid').innerHTML = `<div class="text-danger">Failed to load dashboard stats.</div>`;
    }
}

async function fetchReports() {
    try {
        const res = await fetch(`${API_BASE}/admin/reports`, {
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });
        if (!res.ok) throw new Error("Failed to fetch reports");
        const reports = await res.json();
        const tbody = document.getElementById('reportsTableBody');
        tbody.innerHTML = '';
        if (reports.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center">No reports found.</td></tr>`;
            return;
        }
        reports.forEach(report => {
            const date = new Date(report.created_at).toLocaleDateString();
            const badgeClass = getStatusBadgeClass(report.status);
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${report.id}</td>
                <td><span class="category-tag">${report.category}</span></td>
                <td class="text-truncate" style="max-width: 200px;" title="${report.description}">${report.description}</td>
                <td>
                    <select class="form-select form-select-sm" onchange="updateReportPriority(${report.id}, this.value)">
                        <option value="Low" ${report.priority === 'Low' ? 'selected' : ''}>Low</option>
                        <option value="Medium" ${report.priority === 'Medium' ? 'selected' : ''}>Medium</option>
                        <option value="High" ${report.priority === 'High' ? 'selected' : ''}>High</option>
                    </select>
                </td>
                <td>
                    <select class="form-select form-select-sm status-select ${badgeClass}" onchange="updateReportStatus(${report.id}, this.value, this)">
                        <option value="Pending" ${report.status === 'Pending' ? 'selected' : ''}>Pending</option>
                        <option value="Acknowledged" ${report.status === 'Acknowledged' ? 'selected' : ''}>Acknowledged</option>
                        <option value="In Progress" ${report.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                        <option value="Resolved" ${report.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                    </select>
                </td>
                <td>${date}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteReport(${report.id})"><i class="bi bi-trash"></i></button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        document.getElementById('reportsTableBody').innerHTML = `<tr><td colspan="7" class="text-danger text-center">Failed to load reports.</td></tr>`;
    }
}

function getStatusBadgeClass(status) {
    switch (status) {
        case 'Pending': return 'bg-light text-dark';
        case 'Acknowledged': return 'bg-warning-subtle text-warning-emphasis';
        case 'In Progress': return 'bg-info-subtle text-info-emphasis';
        case 'Resolved': return 'bg-success-subtle text-success-emphasis';
        default: return 'bg-light text-dark';
    }
}

window.updateReportStatus = async function(id, newStatus, selectElement) {
    try {
        const res = await fetch(`${API_BASE}/admin/reports/${id}/status`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({ status: newStatus })
        });
        if (!res.ok) throw new Error("Failed to update status");
        
        selectElement.className = `form-select form-select-sm status-select ${getStatusBadgeClass(newStatus)}`;
    } catch (err) {
        console.error(err);
        alert("Could not update status");
    }
};

window.updateReportPriority = async function(id, newPriority) {
    try {
        const res = await fetch(`${API_BASE}/admin/reports/${id}/priority`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({ priority: newPriority })
        });
        if (!res.ok) throw new Error("Failed to update priority");
    } catch (err) {
        console.error(err);
        alert("Could not update priority");
    }
};

window.deleteReport = async function(id) {
    if (!confirm(`Are you sure you want to delete report #${id}?`)) return;
    try {
        const res = await fetch(`${API_BASE}/admin/reports/${id}`, {
            method: 'DELETE',
            headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
        });
        if (!res.ok) throw new Error("Failed to delete report");
        fetchReports();
    } catch (err) {
        console.error(err);
        alert("Could not delete report");
    }
};
