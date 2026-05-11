import { defineStore } from "pinia";
import { api } from "../services/api";

export const useEmployeeStore = defineStore("employee", {
  state: () => ({
    employees: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    formatEmployeeForUI(backendEmployee) {
      return {
        id: backendEmployee.id,
        firstName: backendEmployee.first_name,
        lastName: backendEmployee.last_name,
        email: backendEmployee.email,
        phone: backendEmployee.phone || "",
        role_id: backendEmployee.role_id,
        contract_type_id: backendEmployee.contract_type_id,
        status: backendEmployee.is_active ? "Actif" : "Inactif",
      };
    },

    formatEmployeeForAPI(uiEmployee) {
      return {
        first_name: uiEmployee.firstName,
        last_name: uiEmployee.lastName,
        email: uiEmployee.email,
        phone: uiEmployee.phone || null,
        role_id: uiEmployee.role_id || null,
        contract_type_id: uiEmployee.contract_type_id || null,
        is_active: uiEmployee.status === "Actif",
      };
    },

    async fetchEmployees() {
      this.isLoading = true;
      try {
        const data = await api.get("/employees/");
        const items = Array.isArray(data) ? data : data.items || [];
        this.employees = items.map(this.formatEmployeeForUI);
      } catch (err) {
        this.error = "Erreur chargement employés";
      } finally {
        this.isLoading = false;
      }
    },

    async addEmployee(employeeData) {
      this.isLoading = true;
      try {
        const payload = this.formatEmployeeForAPI(employeeData);
        const created = await api.post("/employees/", payload);
        this.employees.push(this.formatEmployeeForUI(created));
      } finally {
        this.isLoading = false;
      }
    },

    async updateEmployee(id, updatedData) {
      this.isLoading = true;
      try {
        const payload = this.formatEmployeeForAPI(updatedData);
        const updated = await api.put(`/employees/${id}`, payload);
        const index = this.employees.findIndex((e) => e.id === id);
        if (index !== -1) {
          this.employees[index] = this.formatEmployeeForUI(updated);
        }
      } finally {
        this.isLoading = false;
      }
    },

    async deleteEmployee(id) {
      this.isLoading = true;
      try {
        await api.delete(`/employees/${id}`);
        this.employees = this.employees.filter((e) => e.id !== id);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
