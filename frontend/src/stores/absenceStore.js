import { defineStore } from "pinia";
import { api } from "../services/api";

export const useAbsenceStore = defineStore("absence", {
  state: () => ({
    absences: [
      {
        id: 1,
        employeeId: 1,
        employeeName: "Sarah Martin",
        type: "Congé payé",
        startDate: "2023-11-10",
        endDate: "2023-11-17",
        status: "En attente",
        reason: "Vacances annuelles",
      },
      {
        id: 2,
        employeeId: 2,
        employeeName: "Illia Semenov",
        type: "Maladie",
        startDate: "2023-10-25",
        endDate: "2023-10-26",
        status: "Approuvé",
        reason: "Certificat médical fourni",
      },
      {
        id: 3,
        employeeId: 3,
        employeeName: "Ouahid Bouanani",
        type: "Congé sans solde",
        startDate: "2023-12-01",
        endDate: "2023-12-05",
        status: "Refusé",
        reason: "Déménagement",
      },
    ],
    isLoading: false,
    error: null,
  }),

  getters: {
    pendingAbsences: (state) =>
      state.absences.filter((a) => a.status === "En attente"),
    allAbsences: (state) => state.absences,
  },

  actions: {
    async fetchAbsences() {
      this.isLoading = true;
      try {
        await new Promise((resolve) => setTimeout(resolve, 500));
      } finally {
        this.isLoading = false;
      }
    },

    async addAbsence(absenceData) {
      const newId = this.absences.length
        ? Math.max(...this.absences.map((a) => a.id)) + 1
        : 1;
      this.absences.unshift({
        ...absenceData,
        id: newId,
        status: "En attente",
      });
    },

    async updateAbsenceStatus(id, newStatus) {
      const index = this.absences.findIndex((a) => a.id === id);
      if (index !== -1) {
        this.absences[index].status = newStatus;
      }
    },
  },
});
