import { defineStore } from "pinia";
import { api } from "../services/api";

export const useContractStore = defineStore("contract", {
  state: () => ({
    contracts: [],
    isLoading: false,
  }),

  actions: {
    async fetchContracts() {
      this.isLoading = true;
      try {
        const data = await api.get("/contract-types/");
        this.contracts = Array.isArray(data) ? data : data.items || [];
      } catch (err) {
        console.error("Erreur chargement contrats:", err);
      } finally {
        this.isLoading = false;
      }
    },

    getContractNameById(id) {
      const contract = this.contracts.find((c) => c.id === id);
      return contract ? contract.name : "Non assigné";
    },

    async addContract(contractData) {
      try {
        const payload = {
          name: contractData.name,
          weekly_hours: contractData.weekly_hours,
        };
        const created = await api.post("/contract-types/", payload);
        this.contracts.push(created);
      } catch (err) {
        console.error("Erreur création contrat:", err);
        throw err;
      }
    },

    async updateContract(id, updatedData) {
      try {
        const payload = {
          name: updatedData.name,
          weekly_hours: updatedData.weekly_hours,
        };
        const updated = await api.put(`/contract-types/${id}`, payload);
        const index = this.contracts.findIndex((c) => c.id === id);
        if (index !== -1) {
          this.contracts[index] = updated;
        }
      } catch (err) {
        console.error("Erreur modification contrat:", err);
        throw err;
      }
    },

    async deleteContract(id) {
      try {
        await api.delete(`/contract-types/${id}`);
        this.contracts = this.contracts.filter((c) => c.id !== id);
      } catch (err) {
        console.error("Erreur suppression contrat:", err);
        throw err;
      }
    },
  },
});
