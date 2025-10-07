const STORAGE_USER = "sm_auth_user";
const STORAGE_USERS = "sm_auth_users";

const DEFAULT_USERS = [
  { email: "axel@axel.fr", password: "123", username: "Axel" },
  { email: "vincent@vincent.fr", password: "123", username: "Vincent" },
];

function loadUsers() {
  if (typeof window === "undefined") return DEFAULT_USERS;
  try {
    const raw = localStorage.getItem(STORAGE_USERS);
    return raw ? JSON.parse(raw) : DEFAULT_USERS;
  } catch {
    return DEFAULT_USERS;
  }
}
function saveUsers(users) {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_USERS, JSON.stringify(users));
}

export function addMockUser({ email, password, username }) {
  const users = loadUsers();
  users.push({ email, password, username });
  saveUsers(users);
}

export function mockLogin(email, password) {
  const users = loadUsers();
  const u = users.find((x) => x.email === email && x.password === password);
  if (!u) return { success: false, message: "Invalid credentials" };

  const user = { email: u.email, username: u.username };
  if (typeof window !== "undefined") {
    localStorage.setItem(STORAGE_USER, JSON.stringify(user));
    // notifier l'app
    window.dispatchEvent(new CustomEvent("sm-auth-change", { detail: user }));
  }
  return { success: true, user };
}

export function getCurrentUser() {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(STORAGE_USER);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function logout() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_USER);
  window.dispatchEvent(new CustomEvent("sm-auth-change", { detail: null }));
}

export function onAuthChange(cb) {
  if (typeof window === "undefined") return () => {};
  const handler = (e) => cb(e.detail ?? null);
  const storageSync = (e) => {
    if (e.key === STORAGE_USER) cb(getCurrentUser());
  };
  window.addEventListener("sm-auth-change", handler);
  window.addEventListener("storage", storageSync);
  return () => {
    window.removeEventListener("sm-auth-change", handler);
    window.removeEventListener("storage", storageSync);
  };
}
