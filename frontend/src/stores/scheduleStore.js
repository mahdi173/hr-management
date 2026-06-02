import { defineStore } from "pinia";
import { api } from "../services/api";
import { useEmployeeStore } from "./employeeStore";
import { useRoleStore } from "./roleStore";

export const useScheduleStore = defineStore("schedule", {
  state: () => ({
    shifts: [],
    schedules: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    getShiftsByDate: (state) => (date) => {
      const employeeStore = useEmployeeStore();
      const roleStore = useRoleStore();

      return state.shifts
        .filter((shift) => shift.date === date)
        .map((shift) => {
          const emp = shift.employeeId
            ? employeeStore.employees.find((e) => e.id === shift.employeeId)
            : null;
          const role = shift.roleId
            ? roleStore.roles.find((r) => r.id === shift.roleId)
            : null;

          return {
            ...shift,
            employeeName: emp ? `${emp.firstName} ${emp.lastName}` : null,
            roleName: role ? role.name : "Unknown",
          };
        })
        .sort((a, b) => a.startTime.localeCompare(b.startTime));
    },
  },

  actions: {
    formatShiftForUI(backendShift) {
      const assignment =
        backendShift.assignments && backendShift.assignments.length > 0
          ? backendShift.assignments[0]
          : null;

      return {
        id: backendShift.id,
        date: backendShift.date,
        startTime: backendShift.start_time,
        endTime: backendShift.end_time,
        roleId: backendShift.required_role_id,
        employeeId: assignment ? assignment.employee_id : null,
        status: assignment ? "Confirmed" : "Unassigned",
      };
    },

    async fetchSchedules() {
      try {
        const data = await api.get("/api/v1/schedules/");
        this.schedules = Array.isArray(data) ? data : data.items || [];
      } catch (err) {
        console.error("Error fetching schedules:", err);
      }
    },

    async createSchedule(payload) {
      this.isLoading = true;
      try {
        const created = await api.post("/api/v1/schedules/", payload);
        this.schedules.push(created);
        return created;
      } catch (err) {
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    async fetchWeeklyShifts() {
      this.isLoading = true;
      try {
        const data = await api.get("/api/v1/shifts?include_assignments=true");
        const items = Array.isArray(data) ? data : data.items || [];
        this.shifts = items.map(this.formatShiftForUI);
      } catch (err) {
        console.error("Error fetching shifts:", err);
      } finally {
        this.isLoading = false;
      }
    },

    async addShift(shiftData) {
      try {
        const schedule = this.schedules.find(
          (s) => shiftData.date >= s.start_date && shiftData.date <= s.end_date,
        );
        if (!schedule) throw new Error("No schedule exists for this date.");

        const payload = {
          date: shiftData.date,
          start_time: shiftData.startTime,
          end_time: shiftData.endTime,
          required_role_id: shiftData.roleId,
          schedule_id: schedule.id,
        };

        let createdShift = await api.post(
          `/api/v1/schedules/${schedule.id}/shifts`,
          payload,
        );

        if (shiftData.employeeId) {
          const assignPayload = {
            shift_id: createdShift.id,
            employee_id: shiftData.employeeId,
          };
          const assignment = await api.post(
            `/api/v1/shifts/${createdShift.id}/assign`,
            assignPayload,
          );
          createdShift.assignments = [assignment];
        }

        this.shifts.push(this.formatShiftForUI(createdShift));
      } catch (err) {
        console.error("Error creating shift:", err);
        throw err;
      }
    },

    async updateShift(id, updatedData) {
      try {
        const payload = {
          date: updatedData.date,
          start_time: updatedData.startTime,
          end_time: updatedData.endTime,
          required_role_id: updatedData.roleId,
        };
        let updated = await api.put(`/api/v1/shifts/${id}`, payload);

        const oldShift = this.shifts.find((s) => s.id === id);
        const oldEmployeeId = oldShift ? oldShift.employeeId : null;
        const newEmployeeId = updatedData.employeeId || null;

        if (oldEmployeeId !== newEmployeeId) {
          if (oldEmployeeId) {
            await api.delete(`/api/v1/shifts/${id}/assign/${oldEmployeeId}`);
          }
          if (newEmployeeId) {
            const assignPayload = {
              shift_id: id,
              employee_id: newEmployeeId,
            };
            const assignment = await api.post(
              `/api/v1/shifts/${id}/assign`,
              assignPayload,
            );
            updated.assignments = [assignment];
          } else {
            updated.assignments = [];
          }
        } else {
          updated.assignments = oldEmployeeId
            ? [{ employee_id: oldEmployeeId }]
            : [];
        }

        const index = this.shifts.findIndex((s) => s.id === id);
        if (index !== -1) {
          this.shifts[index] = this.formatShiftForUI(updated);
        }
      } catch (err) {
        console.error("Error updating shift:", err);
        throw err;
      }
    },

    async deleteShift(id) {
      try {
        await api.delete(`/api/v1/shifts/${id}?manager_id=1&force=true`);
        this.shifts = this.shifts.filter((s) => s.id !== id);
      } catch (err) {
        console.error("Error deleting shift:", err);
        throw err;
      }
    },

    async fetchMyShifts() {
      this.isLoading = true;
      try {
        const data = await api.get("/api/v1/shifts/me");
        const items = Array.isArray(data) ? data : data.items || [];
        this.shifts = items.map(this.formatShiftForUI);
      } catch (err) {
        console.error("Erreur chargement de mes shifts:", err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
