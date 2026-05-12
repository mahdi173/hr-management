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

    async addRole(roleData) {
      const newId = this.roles.length
        ? Math.max(...this.roles.map((r) => r.id)) + 1
        : 1;
      this.roles.push({ ...roleData, id: newId });
    },

    async updateRole(id, updatedData) {
      const index = this.roles.findIndex((r) => r.id === id);
      if (index !== -1) {
        this.roles[index] = { ...this.roles[index], ...updatedData };
      }
    },

    async deleteRole(id) {
      this.roles = this.roles.filter((r) => r.id !== id);
    },
  },
});
