import { defineStore } from "pinia";
import { api } from "../services/api";

export const useManagementStore = defineStore("management", {
  state: () => ({
    alerts: [],
    workload: null,
    rebalancingSuggestions: [],
    scheduleHealth: null,
    shiftRecommendations: null,
    isLoading: false,
    isRecommending: false,
  }),

  actions: {
    async fetchAlerts() {
      this.isLoading = true;
      try {
        const data = await api.get("/alerts/");
        this.alerts = Array.isArray(data) ? data : data.items || [];
      } catch (err) {
        console.error("Error fetching alerts:", err);
      } finally {
        this.isLoading = false;
      }
    },

    async resolveAlert(alertId) {
      try {
        await api.put(`/alerts/${alertId}/resolve`);
        this.alerts = this.alerts.filter((a) => a.id !== alertId);
      } catch (err) {
        console.error("Error resolving alert:", err);
        throw err;
      }
    },

    async triggerInsightsRefresh() {
      try {
        await api.post("/analytics/refresh-insights");
        await this.fetchAlerts();
      } catch (err) {
        console.error("Error refreshing insights:", err);
      }
    },

    async fetchWorkload(startDate, endDate) {
      try {
        this.workload = await api.get(
          `/analytics/workload?start_date=${startDate}&end_date=${endDate}`,
        );
      } catch (err) {
        console.error("Error fetching workload:", err);
      }
    },

    async fetchScheduleHealth(scheduleId) {
      try {
        this.scheduleHealth = await api.get(
          `/analytics/schedule/${scheduleId}/health`,
        );
      } catch (err) {
        console.error("Error fetching schedule health:", err);
      }
    },

    async fetchRebalancingSuggestions(startDate, endDate) {
      try {
        const data = await api.get(
          `/analytics/rebalancing-suggestions?start_date=${startDate}&end_date=${endDate}`,
        );
        this.rebalancingSuggestions = Array.isArray(data)
          ? data
          : data.items || [];
      } catch (err) {
        console.error("Error fetching rebalancing suggestions:", err);
      }
    },

    async fetchShiftRecommendations(shiftId) {
      this.isRecommending = true;
      this.shiftRecommendations = null;
      try {
        this.shiftRecommendations = await api.get(
          `/recommendations/shift/${shiftId}`,
        );
      } catch (err) {
        console.error("Error fetching shift recommendations:", err);
      } finally {
        this.isRecommending = false;
      }
    },
  },
});
