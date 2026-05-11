import { defineStore } from "pinia";
import { api } from "../services/api";

export const useRoleStore = defineStore("role", {
  state: () => ({
    roles: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchRoles() {
      this.isLoading = true;
      try {
        const data = await api.get("/roles/");
        this.roles = data;
      } catch (err) {
        this.error = "Erreur lors du chargement des rôles.";
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    getRoleNameById(id) {
      const role = this.roles.find((r) => r.id === id);
      return role ? role.name : "Non assigné";
    },
  },
});
