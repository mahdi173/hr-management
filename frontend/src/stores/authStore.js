import { defineStore } from "pinia";
import { api } from "../services/api";
import router from "../router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  }),

  getters: {
    userInitials: (state) => {
      if (!state.user || !state.user.first_name) return "?";

      const first = state.user.first_name.charAt(0);
      const last = state.user.last_name ? state.user.last_name.charAt(0) : "";
      return `${first}${last}`;
    },
    isManager: (state) => {
      return state.user?.role === "Manager" || state.user?.role === "Admin";
    },
    isEmployee: (state) => {
      return state.user?.role === "Employee" || state.user?.role === "Serveur";
    },
  },

  actions: {
    async login(email, password) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.post("/auth/login", { email, password });
        this.user = response;
        this.isAuthenticated = true;
        router.push("/dashboard");
      } catch (err) {
        this.error = "Email ou mot de passe incorrect";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCurrentUser() {
      try {
        const response = await api.get("/auth/me");
        this.user = response;
        this.isAuthenticated = true;
      } catch (err) {
        this.user = null;
        this.isAuthenticated = false;
      }
    },

    async logout() {
      try {
        await api.post("/auth/logout");
      } catch (err) {
      } finally {
        this.user = null;
        this.isAuthenticated = false;
        router.push("/");
      }
    },
  },
});
