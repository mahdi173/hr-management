import { defineStore } from "pinia";
import { api } from "../services/api";

export const useRoleStore = defineStore("role", {
  state: () => ({
    roles: [],
    isLoading: false,
  }),

  actions: {
    async fetchRoles() {
      this.isLoading = true;
      try {
        const data = await api.get("/roles/");
        this.roles = Array.isArray(data) ? data : data.items || [];
      } catch (err) {
        console.error("Erreur chargement roles:", err);
      } finally {
        this.isLoading = false;
      }
    },

    getRoleNameById(id) {
      const role = this.roles.find((r) => r.id === id);
      return role ? role.name : "Non assigné";
    },

    async addRole(roleData) {
      try {
        const payload = {
          name: roleData.name,
          description: roleData.name,
        };
        const created = await api.post("/roles/", payload);
        this.roles.push(created);
      } catch (err) {
        console.error("Erreur création role:", err);
        throw err;
      }
    },

    async updateRole(id, updatedData) {
      try {
        const payload = {
          name: updatedData.name,
          description: updatedData.name,
        };
        const updated = await api.put(`/roles/${id}`, payload);
        const index = this.roles.findIndex((r) => r.id === id);
        if (index !== -1) {
          this.roles[index] = updated;
        }
      } catch (err) {
        console.error("Erreur modification role:", err);
        throw err;
      }
    },

    async deleteRole(id) {
      try {
        await api.delete(`/roles/${id}`);
        this.roles = this.roles.filter((r) => r.id !== id);
      } catch (err) {
        console.error("Erreur suppression role:", err);
        throw err;
      }
    },
  },
});
