import { defineStore } from "pinia";
import { api } from "../services/api";

export const useScheduleStore = defineStore("schedule", {
  state: () => ({
    isLoading: false,
    currentDate: new Date(),
    shifts: [
      {
        id: 1,
        date: "2023-10-24",
        startTime: "10:00",
        endTime: "15:00",
        roleId: 3,
        roleName: "Cuisinier",
        employeeId: 3,
        employeeName: "Ouahid Bouanani",
        status: "Confirmé",
      },
      {
        id: 2,
        date: "2023-10-24",
        startTime: "18:00",
        endTime: "23:30",
        roleId: 2,
        roleName: "Chef de rang",
        employeeId: 1,
        employeeName: "Sarah Martin",
        status: "Confirmé",
      },
      {
        id: 3,
        date: "2023-10-25",
        startTime: "18:30",
        endTime: "23:30",
        roleId: 4,
        roleName: "Serveur",
        employeeId: 2,
        employeeName: "Illia Semenov",
        status: "En attente",
      },
      {
        id: 4,
        date: "2023-10-26",
        startTime: "19:00",
        endTime: "23:30",
        roleId: 5,
        roleName: "Plongeur",
        employeeId: null,
        employeeName: null,
        status: "À combler",
      },
    ],
  }),

  getters: {
    getShiftsByDate: (state) => {
      return (dateString) =>
        state.shifts.filter((shift) => shift.date === dateString);
    },
  },

  actions: {
    async fetchWeeklyShifts(startDate, endDate) {
      this.isLoading = true;
      try {
        // const data = await api.get(`/shifts?start=${startDate}&end=${endDate}`);
        // this.shifts = data;
        await new Promise((resolve) => setTimeout(resolve, 500));
      } catch (error) {
        console.error("Error fetching shifts", error);
      } finally {
        this.isLoading = false;
      }
    },

    addShift(shiftData) {
      const newId = this.shifts.length
        ? Math.max(...this.shifts.map((s) => s.id)) + 1
        : 1;
      this.shifts.push({
        ...shiftData,
        id: newId,
        status: shiftData.employeeId ? "Confirmé" : "À combler",
      });
    },

    updateShift(id, updatedData) {
      const index = this.shifts.findIndex((s) => s.id === id);
      if (index !== -1) {
        this.shifts[index] = {
          ...this.shifts[index],
          ...updatedData,
          status: updatedData.employeeId ? "Confirmé" : "À combler",
        };
      }
    },

    deleteShift(id) {
      this.shifts = this.shifts.filter((s) => s.id !== id);
    },
  },
});
