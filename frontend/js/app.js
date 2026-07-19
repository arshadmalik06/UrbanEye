const API_BASE = "http://localhost:8000";
function getToken() {
    return localStorage.getItem("urbaneye_token");
}

function setToken(token) {
    localStorage.setItem("urbaneye_token", token);
}

function clearToken() {
    localStorage.removeItem("urbaneye_token");
}

function isLoggedIn() {
    return !!getToken();
}

function getUser() {
    const raw = localStorage.getItem("urbaneye_user");
    return raw ? JSON.parse(raw) : null;
}

function setUser(user) {
    localStorage.setItem("urbaneye_user", JSON.stringify(user));
}

function clearUser() {
    localStorage.removeItem("urbaneye_user");
}

async function apiFetch(path, options = {}) {
    const token = getToken();
    if (token) {
        options.headers = {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        };
    }
    const res = await fetch(`${API_BASE}${path}`, options);
    return res;
}

function updateNavbarAuth() {
    const area = document.getElementById("navbarAuthArea");
    if (!area) return;

    if (isLoggedIn()) {
        const user = getUser();
        const initial = user && user.name ? user.name.charAt(0).toUpperCase() : "U";
        const displayName = user ? user.name : "User";

        let adminBtn = "";
        if (user && user.role === "admin") {
            adminBtn = `<a href="admin.html" class="btn-auth-login" style="margin-right:8px; text-decoration:none;">Admin Dashboard</a>`;
        }

        area.innerHTML = `
            ${adminBtn}
            <div class="navbar-user-badge">
                <div class="navbar-user-avatar">${initial}</div>
                <span>${displayName}</span>
            </div>
            <button class="btn-auth-logout" id="logoutBtn">Logout</button>
        `;

        const logoutBtn = document.getElementById("logoutBtn");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", handleLogout);
        }
    }
    else {
        area.innerHTML = `
            <button class="btn-auth-login" id="openAuthModalBtn">Login / Register</button>
        `;

        const openBtn = document.getElementById("openAuthModalBtn");
        if (openBtn) {
            openBtn.addEventListener("click", () => {
                const modal = document.getElementById("authModal");
                if (modal) {
                    const bsModal = new bootstrap.Modal(modal);
                    bsModal.show();
                }
            });
        }
    }
    updateFormOverlay();
}

function updateFormOverlay() {
    const formContainer = document.querySelector(".form-container");
    if (!formContainer) return;

    if (isLoggedIn()) {
        formContainer.classList.remove("login-required-overlay");
    }
    else {
        formContainer.classList.add("login-required-overlay");
        formContainer.addEventListener("click", function overlayClick(e) {
            if (!isLoggedIn()) {
                const modal = document.getElementById("authModal");
                if (modal) {
                    const bsModal = new bootstrap.Modal(modal);
                    bsModal.show();
                }
            }
        }, { once: true });
    }
}

function initAuthTabs() {
    document.querySelectorAll(".auth-tab-btn").forEach(btn => {
        btn.addEventListener("click", () => switchAuthTab(btn.dataset.tab));
    });

    document.querySelectorAll(".auth-switch-link").forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            switchAuthTab(link.dataset.tab);
        });
    });
}

function switchAuthTab(tabName) {
    showAuthMsg("", "");
    document.querySelectorAll(".auth-tab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.tab === tabName);
    });

    const registerPane = document.getElementById("paneRegister");
    const loginPane = document.getElementById("paneLogin");
    if (registerPane) registerPane.classList.toggle("active", tabName === "register");
    if (loginPane) loginPane.classList.toggle("active", tabName === "login");
}

function showAuthMsg(text, type) {
    const msgEl = document.getElementById("authMsg");
    if (!msgEl) return;

    msgEl.className = "auth-msg";
    msgEl.textContent = text;

    if (type === "success") msgEl.classList.add("success");
    else if (type === "error") msgEl.classList.add("error");
}
function initRegisterForm() {
    const form = document.getElementById("registerForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("regName").value.trim();
        const email = document.getElementById("regEmail").value.trim();
        const phone = document.getElementById("regPhone").value.trim();
        const password = document.getElementById("regPassword").value;
        const role = document.getElementById("regRole").value;
        const btn = document.getElementById("regSubmitBtn");
        btn.textContent = "Creating account...";
        btn.disabled = true;
        try {
            const res = await fetch(`${API_BASE}/users`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, phone, password, role }),
            });

            const data = await res.json();
            if (res.ok) {
                const userData = {
                    id: data.id,
                    name: data.name || name,
                    email: data.email || email,
                    phone: data.phone || phone,
                    role: data.role || role,
                };

                setToken(`user_${userData.id}_${Date.now()}`);
                setUser(userData);
                showAuthMsg("Account created! Logging you in...", "success");
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(document.getElementById("authModal"));
                    if (modal) modal.hide();
                    updateNavbarAuth();
                }, 1200);
            } else {
                const errMsg = data.detail || JSON.stringify(data);
                showAuthMsg(`Registration failed: ${errMsg}`, "error");
            }
        }
        catch (err) {
            console.error("Registration error:", err);
            showAuthMsg("Network error. Is the backend running?", "error");
        }
        finally {
            btn.textContent = "Create Account";
            btn.disabled = false;
        }
    });
}

function initLoginForm() {
    const form = document.getElementById("loginForm");
    if (!form) return;
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value;
        const btn = document.getElementById("loginSubmitBtn");
        btn.textContent = "Logging in...";
        btn.disabled = true;
        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
            const data = await res.json();
            if (res.ok) {
                const userData = {
                    id: data.id,
                    name: data.name,
                    email: data.email,
                    phone: data.phone,
                    role: data.role,
                };
                setToken(`user_${userData.id}_${Date.now()}`);
                setUser(userData);
                showAuthMsg("Login successful!", "success");
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(document.getElementById("authModal"));
                    if (modal) modal.hide();
                    updateNavbarAuth();
                }, 1000);
            } else {
                const errMsg = data.detail || "Invalid email or password.";
                showAuthMsg(errMsg, "error");
            }
        }
        catch (err) {
            console.error("Login error:", err);
            showAuthMsg("Network error. Is the backend running?", "error");
        }
        finally {
            btn.textContent = "Log In";
            btn.disabled = false;
        }
    });
}

function handleLogout() {
    clearToken();
    clearUser();
    updateNavbarAuth();
}
const getLocationBtn = document.getElementById("getLocationBtn");
const locationStatus = document.getElementById("locationStatus");
const latInput = document.getElementById("latitude");
const lngInput = document.getElementById("longitude");
if (getLocationBtn) {
    getLocationBtn.addEventListener("click", () => {
        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            return;
        }
        getLocationBtn.textContent = "Fetching location...";
        getLocationBtn.disabled = true;
        navigator.geolocation.getCurrentPosition(
            (position) => {
                latInput.value = position.coords.latitude;
                lngInput.value = position.coords.longitude;
                locationStatus.classList.remove("d-none");
                getLocationBtn.textContent = "Location Captured ✓";
                getLocationBtn.classList.replace("btn-secondary", "btn-success");
                getLocationBtn.disabled = false;
            },
            (error) => {
                alert("Unable to retrieve location. Please allow location access.");
                getLocationBtn.textContent = "Use My Current Location";
                getLocationBtn.disabled = false;
            },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    });
}
const reportForm = document.getElementById("reportForm");
if (reportForm) {
    reportForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (!isLoggedIn()) {
            alert("Please log in or register before submitting a report.");
            const modal = document.getElementById("authModal");
            if (modal) {
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            }
            return;
        }
        const category = document.getElementById("category").value;
        const description = document.getElementById("description").value;
        const lat = document.getElementById("latitude").value;
        const lng = document.getElementById("longitude").value;
        if (!lat || !lng) {
            alert("Please capture your location before submitting.");
            return;
        }
        const submitBtn = reportForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = "Submitting...";
        submitBtn.disabled = true;
        try {
            const user = getUser();
            const reportData = {
                user_id: user ? user.id : 0,
                title: category,
                description: description,
                category: category,
                latitude: parseFloat(lat),
                longitude: parseFloat(lng),
                address: "",
                priority: "medium",
                status: "submitted",
            };
            const res = await fetch(`${API_BASE}/reports`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(reportData),
            });
            const data = await res.json();
            if (res.ok) {
                alert(`Report submitted successfully!\nID: #${data.id}`);
                reportForm.reset();
                locationStatus.classList.add("d-none");
                if (getLocationBtn) {
                    getLocationBtn.textContent = "Use My Current Location";
                    getLocationBtn.classList.replace("btn-success", "btn-secondary");
                    getLocationBtn.disabled = false;
                }
            } else {
                const errMsg = data.detail || JSON.stringify(data);
                alert(`Failed to submit report: ${errMsg}`);
            }
        }
        catch (error) {
            console.error("Submit error:", error);
            alert("Network error. Is the backend running?");
        }
        finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}
document.addEventListener("DOMContentLoaded", () => {
    updateNavbarAuth();
    initAuthTabs();
    initRegisterForm();
    initLoginForm();
});
window.register = async function (name, email, phone, password, role) {
    try {
        const res = await fetch(`${API_BASE}/users`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone, password, role }),
        });

        const data = await res.json();
        if (res.ok) {
            console.log("User created successfully in database:", data);
            alert("Registered successfully!");
        } else {
            console.error("Registration failed:", data);
            alert("Registration failed.");
        }
        return data;
    } catch (err) {
        console.error("Network error:", err);
    }
};
