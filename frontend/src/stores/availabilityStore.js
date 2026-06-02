import { defineStore } from "pinia";
import { api } from "../services/api";

export const useAvailabilityStore = defineStore("availability", {
  state: () => ({
    availabilities: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    formatAvailabilityForUI(backendData) {
      return {
        id: backendData.id,
        employeeId: backendData.employee_id,
        startTime: backendData.start_time,
        endTime: backendData.end_time,
        dayOfWeek: backendData.day_of_week,
        isRecurring: backendData.is_recurring,
        specificDate: backendData.specific_date,
        isActive: backendData.is_active,
      };
    },

    async fetchAvailabilitiesByEmployee(employeeId) {
      this.isLoading = true;
      try {
        const data = await api.get(`/employees/${employeeId}/availabilities`);
        this.availabilities = Array.isArray(data)
          ? data.map(this.formatAvailabilityForUI)
          : [];
      } catch (err) {
        console.error(err);
        this.error = "Failed to load availabilities";
      } finally {
        this.isLoading = false;
      }
    },

    async addAvailability(availabilityData) {
      try {
        const payload = {
          employee_id: availabilityData.employeeId,
          start_time: availabilityData.startTime,
          end_time: availabilityData.endTime,
          is_recurring: availabilityData.isRecurring,
          day_of_week: availabilityData.isRecurring
            ? availabilityData.dayOfWeek
            : null,
          specific_date: !availabilityData.isRecurring
            ? availabilityData.specificDate
            : null,
          is_active: true,
        };

        const created = await api.post(
          `/employees/${availabilityData.employeeId}/availabilities`,
          payload,
        );
        this.availabilities.push(this.formatAvailabilityForUI(created));
      } catch (err) {
        console.error(err);
        throw err;
      }
    },

    async updateAvailability(id, updateData) {
      try {
        const payload = {
          start_time: updateData.startTime,
          end_time: updateData.endTime,
          is_active:
            updateData.isActive !== undefined ? updateData.isActive : true,
        };

        const updated = await api.put(`/availabilities/${id}`, payload);

        const index = this.availabilities.findIndex((a) => a.id === id);
        if (index !== -1) {
          this.availabilities[index] = this.formatAvailabilityForUI(updated);
        }
      } catch (err) {
        console.error(err);
        throw err;
      }
    },

    async deleteAvailability(id) {
      try {
        await api.delete(`/availabilities/${id}`);
        this.availabilities = this.availabilities.filter((a) => a.id !== id);
      } catch (err) {
        console.error(err);
        throw err;
      }
    },

    async fetchMyAvailabilities() {
      this.isLoading = true;
      try {
        const data = await api.get("/availabilities/me");
        this.availabilities = Array.isArray(data) ? data : data.items || [];
      } catch (err) {
        console.error("Erreur chargement de mes disponibilités:", err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
