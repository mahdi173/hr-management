import { defineStore } from "pinia";
import { api } from "../services/api";

const typeMapping = {
  "Congé payé": 1,
  "Maladie": 2,
  "Congé sans solde": 3,
  "Autre": 4,
};

const reverseTypeMapping = {
  1: "Congé payé",
  2: "Maladie",
  3: "Congé sans solde",
  4: "Autre",
};

export const useAbsenceStore = defineStore("absence", {
  state: () => ({
    absences: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    pendingAbsences: (state) =>
      state.absences.filter(
        (a) => a.status === "En attente" || a.status === "pending",
      ),
    allAbsences: (state) => state.absences,
  },

  actions: {
    formatAbsenceForUI(backendAbsence) {
      let uiStatus = "En attente";
      if (
        backendAbsence.status === "approved" ||
        backendAbsence.status === "Approuvé"
      )
        uiStatus = "Approuvé";
      if (
        backendAbsence.status === "rejected" ||
        backendAbsence.status === "Refusé"
      )
        uiStatus = "Refusé";

      return {
        id: backendAbsence.id,
        employeeId: backendAbsence.employee_id,
        employeeName: backendAbsence.employee_name || "Collaborateur",
        type:
          backendAbsence.type ||
          reverseTypeMapping[backendAbsence.absence_type_id] ||
          "Congé payé",
        startDate: backendAbsence.start_date,
        endDate: backendAbsence.end_date,
        status: uiStatus,
        reason: backendAbsence.reason || "",
      };
    },

    async fetchAbsences(isManager = false) {
      this.isLoading = true;
      try {
        const data = await api.get(isManager ? "/absences/" : "/absences/me");
        const items = Array.isArray(data) ? data : data.items || [];
        this.absences = items.map(this.formatAbsenceForUI);
      } catch (err) {
        console.error("Erreur chargement absences:", err);
        this.error = "Impossible de charger les absences";
      } finally {
        this.isLoading = false;
      }
    },

    async addAbsence(absenceData) {
      try {
        const payload = {
          employee_id: absenceData.employeeId,
          absence_type_id: typeMapping[absenceData.type] || 1,
          start_date: absenceData.startDate,
          end_date: absenceData.endDate,
          reason: absenceData.reason,
        };

        const created = await api.post("/absences/", payload);
        this.absences.unshift(this.formatAbsenceForUI(created));
      } catch (err) {
        console.error("Erreur création absence:", err);
        throw err;
      }
    },

    async updateAbsenceStatus(id, newStatus) {
      try {
        const endpoint =
          newStatus === "Approuvé"
            ? `/absences/${id}/approve`
            : `/absences/${id}/reject`;

        const updated = await api.put(endpoint);

        const index = this.absences.findIndex((a) => a.id === id);
        if (index !== -1) {
          this.absences[index] =
            updated && updated.id
              ? this.formatAbsenceForUI(updated)
              : { ...this.absences[index], status: newStatus };
        }
      } catch (err) {
        console.error(
          `Erreur lors de la mise à jour du statut (${newStatus}):`,
          err,
        );
        throw err;
      }
    },
  },
});
