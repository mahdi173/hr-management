import { defineStore } from "pinia";
import { api } from "../services/api";

export const useContractStore = defineStore("contract", {
  state: () => ({
    contracts: [
      { id: 1, name: "CDI 39h", weekly_hours: 39 },
      { id: 2, name: "CDI 35h", weekly_hours: 35 },
      { id: 3, name: "CDD 20h", weekly_hours: 20 },
      { id: 4, name: "Extra", weekly_hours: 0 },
    ],
    isLoading: false,
  }),

  actions: {
    async fetchContracts() {
      /*
      this.isLoading = true;
      try {
        const data = await api.get('/contract-types/');
        this.contracts = data;
      } catch (err) {
        console.error(err);
      } finally {
        this.isLoading = false;
      }
      */
    },

    getContractNameById(id) {
      const contract = this.contracts.find((c) => c.id === id);
      return contract ? contract.name : "Non assigné";
    },
  },
});
