# 📋 BACKLOG – Timeapp Frontend (Vue.js)

*User Stories and Technical Sub-tasks for Frontend Implementation*

### Architecture Pattern (Frontend)

1. **Views/Pages**: Top-level route components.
2. **Components**: Reusable UI elements (buttons, modals, schedule grids).
3. **Stores (Pinia)**: Global state management and API data caching.
4. **Composables**: Reusable Vue 3 Composition API logic (e.g., `useSchedule()`, `useAuth()`).
5. **Services/API**: Axios wrapper for backend communication.

---

## Phase 1 – Foundations (MVP)

### US-1.1: Employee Directory & Profiles

* **Views**: `/employees` (List view), `/employees/:id` (Detail view).
* **Components**: `EmployeeTable`, `EmployeeFormModal`, `ProfileCard`.
* **Tasks**:
* Create Pinia `employeeStore` to handle CRUD operations via API.
* Build responsive data table with search and pagination.
* Design a form with validation (Vuelidate or VeeValidate) for creating/editing users.

### US-1.2 & 1.3: Settings - Roles & Contracts

* **Views**: `/settings/roles`, `/settings/contracts`.
* **Components**: `RoleManager`, `ContractTypeList`.
* **Tasks**:
* Build simple CRUD interfaces for admins to define roles and contract parameters.
* Integrate these options into the `EmployeeFormModal` dropdowns.

### US-1.4: Availability Matrix

* **Components**: `AvailabilityGrid` (Interactive weekly time selector).
* **Tasks**:
* Build a drag-to-select grid allowing employees to paint their availability (green for available, red for unavailable).
* Ensure the component works smoothly on both desktop and mobile.

### US-1.5: Absence Management UI

* **Views**: `/absences` (Employee view), `/manager/absences` (Manager approval view).
* **Components**: `AbsenceRequestForm`, `PendingApprovalsList`, `StatusBadge`.
* **Tasks**:
* Build a date-picker form for requesting time off.
* Create a manager dashboard widget to quickly approve/deny requests.

### US-1.6, 1.7 & 1.9: Interactive Schedule Grid (The Core)

* **Views**: `/schedule` (Main planning view).
* **Components**: `ScheduleCalendar`, `ShiftCard`, `EmployeeDragList`, `ViewToggle` (Day/Week/Month).
* **Tasks**:
* Implement a robust calendar interface (consider wrapping FullCalendar or building a custom CSS Grid).
* Implement drag-and-drop functionality: drag employees from a sidebar onto open shift slots.
* Create shift creation modals (setting time, role required, max employees).

---

## Phase 2 – Controls & Optimization

### US-2.1 & 2.2: Visual Conflict & Compliance Warnings

* **Components**: `ConflictToast`, `ShiftCard` (Warning states).
* **Tasks**:
* Update `ShiftCard` to show a red border/icon if a conflict is returned by the API.
* Create inline warnings when a manager tries to assign an employee who exceeds their weekly contract hours.

### US-2.3 & 2.5: Alert Center & Schedule Health

* **Views**: Top Navigation Bar, `/schedule` (Header).
* **Components**: `NotificationBell`, `AlertDropdown`, `CompletionProgressBar`.
* **Tasks**:
* Implement a global notification state to show unassigned shift alerts.
* Add a progress bar at the top of the schedule view showing "85% Scheduled".

### US-2.4: Workload Dashboard

* **Views**: `/analytics`.
* **Components**: `WorkloadChart` (Bar/Pie charts using Chart.js or ECharts).
* **Tasks**:
* Build a visual representation of team hours to easily spot over-utilized vs. under-utilized staff.

---

## Phase 3 – Intelligence artificielle légère

### US-3.1: AI Magic Suggestions

* **Components**: `AiSuggestionPopover`, `ConfidenceScoreBadge`.
* **Tasks**:
* Add an "Auto-Fill Suggestion" (magic wand icon) button to empty shifts.
* Display a ranked list of employees with their AI confidence score, allowing the manager to assign them in one click.

### US-3.2 & 3.3: Smart Insights & Rebalancing UI

* **Components**: `InsightWidget`, `RebalanceModal`.
* **Tasks**:
* Create a dashboard widget that translates backend insights into plain text (e.g., "Risk: 3 shifts unassigned for tomorrow").
* Build a modal that shows a before/after view of the schedule if the AI's rebalancing suggestions are applied.

---

## Phase 4 – IA Avancée

### US-4.1 & 4.2: 1-Click Schedule Generation

* **Components**: `GenerateScheduleWizard`, `LoadingSkeleton` (AI thinking state).
* **Tasks**:
* Create a step-by-step wizard to set parameters before generating a whole week's schedule.
* Implement engaging loading states while the backend optimizer runs.
* Add "Accept" or "Reject" buttons for dynamic optimization feedback.
