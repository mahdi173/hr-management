import { defineStore } from "pinia";
import { api } from "../services/api";

export const useEmployeeStore = defineStore("employee", {
  state: () => ({
    // Dummy data to build the UI immediately
    employees: [
      {
        id: 1,
        firstName: "Sarah",
        lastName: "Martin",
        email: "sarah.m@timeapp.fr",
        role: "Chef de rang",
        contract: "CDI 35h",
        status: "Actif",
      },
      {
        id: 2,
        firstName: "Illia",
        lastName: "Semenov",
        email: "illia.s@timeapp.fr",
        role: "Serveur",
        contract: "CDD 20h",
        status: "Actif",
      },
      {
        id: 3,
        firstName: "Ouahid",
        lastName: "Bouanani",
        email: "ouahid.b@timeapp.fr",
        role: "Cuisinier",
        contract: "CDI 35h",
        status: "Actif",
      },
      {
        id: 4,
        firstName: "Mehdi",
        lastName: "Zougari",
        email: "mehdi.z@timeapp.fr",
        role: "Manager",
        contract: "CDI 39h",
        status: "En congé",
      },
    ],
    isLoading: false,
    error: null,
  }),

  getters: {
    totalEmployees: (state) => state.employees.length,
    activeEmployees: (state) =>
      state.employees.filter((e) => e.status === "Actif").length,
  },

  actions: {
    async fetchEmployees() {
      this.isLoading = true;
      this.error = null;
      try {
        // TODO
        // const data = await api.get('/employees');
        // this.employees = data;

        // Simulating network delay for now
        await new Promise((resolve) => setTimeout(resolve, 500));
      } catch (err) {
        this.error = err.message;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
