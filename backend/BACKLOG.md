# 📋 BACKLOG – Timeapp Backend

_User Stories and Technical Sub-tasks for Backend Implementation_

---

## 📖 Document Overview

This document breaks down the Timeapp roadmap into actionable User Stories (US) and technical sub-tasks for backend development. Each phase builds upon the previous one, following a structured approach from MVP to advanced AI features.

### Architecture Pattern
All features follow the established pattern:
1. **Models** (SQLAlchemy) – Database schema
2. **Schemas** (Pydantic) – Validation and serialization
3. **Repositories** – Data access layer
4. **Services** – Business logic
5. **Controllers** – API endpoints (FastAPI)
6. **Tests** – Unit and integration tests

### Priority Order
- **Phase 1**: Critical (MVP)
- **Phase 2**: High (Quality & Safety)
- **Phase 3**: Medium (AI Assistant)
- **Phase 4**: Low (Optional Advanced AI)

---

# Phase 1 – Foundations (MVP Fonctionnel)

**Goal:** Disposer d'un système utilisable avec gestion manuelle complète.

---

## 🧑‍💼 Personnel Management

### US-1.1: Employee Profile Management

**As a** manager  
**I want** to create, read, update, and delete employee profiles  
**So that** I can maintain an accurate database of my team members

#### Acceptance Criteria
- ✅ Create new employee with required fields (name, email, role)
- ✅ Update employee information
- ✅ Delete employee (soft delete recommended)
- ✅ View employee details
- ✅ List all employees with pagination
- ✅ Input validation (email format, unique email, etc.)

#### Technical Sub-tasks
- [ ] **Models**: Create `Employee` model
  - Fields: id, first_name, last_name, email (unique), phone, role_id, contract_type, is_active, created_at, updated_at
  - Relationships: role (ManyToOne), availabilities (OneToMany), absences (OneToMany), schedule_assignments (OneToMany)
- [ ] **Schemas**: Create Pydantic schemas
  - `EmployeeBase`, `EmployeeCreate`, `EmployeeUpdate`, `Employee` (response)
  - Validation: email format, phone format, required fields
- [ ] **Repository**: Create `EmployeeRepository` extending `BaseRepository`
  - Methods: get_by_email(), get_active_employees(), soft_delete()
- [ ] **Service**: Create `EmployeeService` extending `BaseService`
  - Methods: create_employee(), update_employee(), delete_employee(), get_employee(), list_employees()
  - Business logic: check email uniqueness, validate role exists
- [ ] **Controller**: Create `employee_controller.py`
  - Endpoints: POST /employees, GET /employees, GET /employees/{id}, PUT /employees/{id}, DELETE /employees/{id}
  - Status codes: 201 (created), 200 (success), 404 (not found), 400 (validation error)
- [ ] **Tests**: Unit and integration tests
  - Test CRUD operations, validation rules, edge cases

**Dependencies:** None (foundational)

---

### US-1.2: Role Management

**As a** manager  
**I want** to define and assign roles to employees  
**So that** I can organize my team by job function and permissions

#### Acceptance Criteria
- ✅ Create predefined roles (Manager, Employee, Team Lead, etc.)
- ✅ Assign role to employee
- ✅ View employees by role
- ✅ Roles have descriptive names and optional permissions

#### Technical Sub-tasks
- [ ] **Models**: Create `Role` model
  - Fields: id, name (unique), description, permissions (JSON), is_active, created_at
  - Relationships: employees (OneToMany)
- [ ] **Schemas**: Create Pydantic schemas
  - `RoleBase`, `RoleCreate`, `RoleUpdate`, `Role` (response)
- [ ] **Repository**: Create `RoleRepository`
  - Methods: get_by_name(), get_active_roles()
- [ ] **Service**: Create `RoleService`
  - Methods: create_role(), update_role(), list_roles()
  - Business logic: validate unique role names
- [ ] **Controller**: Create `role_controller.py`
  - Endpoints: POST /roles, GET /roles, GET /roles/{id}, PUT /roles/{id}
- [ ] **Migrations**: Create Alembic migration for Role and update Employee table
- [ ] **Tests**: Test role creation, assignment, and retrieval

**Dependencies:** US-1.1 (Employee model needs role_id foreign key)

---

### US-1.3: Contract Type Management

**As a** manager  
**I want** to specify contract types for employees (full-time, part-time, intern, etc.)  
**So that** I can track different employment arrangements

#### Acceptance Criteria
- ✅ Define contract types with weekly hour limits
- ✅ Assign contract type to employee
- ✅ View employees by contract type
- ✅ Contract types include: Temps plein, Temps partiel, Stagiaire, CDD, CDI

#### Technical Sub-tasks
- [ ] **Models**: Create `ContractType` model
  - Fields: id, name (unique), description, weekly_hours (default), max_weekly_hours, is_active
  - Relationships: employees (OneToMany)
- [ ] **Schemas**: Create Pydantic schemas
  - `ContractTypeBase`, `ContractTypeCreate`, `ContractType` (response)
- [ ] **Repository**: Create `ContractTypeRepository`
  - Methods: get_by_name(), get_active_contract_types()
- [ ] **Service**: Create `ContractTypeService`
  - Methods: create_contract_type(), list_contract_types()
  - Seed default contract types (CDI 35h, CDD, Temps partiel 20h, Stagiaire)
- [ ] **Controller**: Create `contract_type_controller.py`
  - Endpoints: GET /contract-types, POST /contract-types
- [ ] **Migrations**: Create Alembic migration for ContractType and update Employee table
- [ ] **Tests**: Test contract type creation and assignment

**Dependencies:** US-1.1 (Employee model update)

---

### US-1.4: Employee Availability Management

**As an** employee  
**I want** to define my weekly availability  
**So that** my manager can schedule me only during times I'm available

#### Acceptance Criteria
- ✅ Define recurring weekly availability (e.g., Monday 9:00-17:00)
- ✅ Define specific date availability overrides
- ✅ View my own availability
- ✅ Manager can view employee availability
- ✅ Support multiple time slots per day

#### Technical Sub-tasks
- [ ] **Models**: Create `Availability` model
  - Fields: id, employee_id (FK), day_of_week (0-6), start_time, end_time, is_recurring, specific_date, is_active
  - Relationships: employee (ManyToOne)
  - Constraints: check start_time < end_time, no overlapping slots for same employee
- [ ] **Schemas**: Create Pydantic schemas
  - `AvailabilityBase`, `AvailabilityCreate`, `AvailabilityUpdate`, `Availability` (response)
  - Validation: time format, day_of_week range (0-6), logical time order
- [ ] **Repository**: Create `AvailabilityRepository`
  - Methods: get_by_employee(), get_by_day(), check_overlap()
- [ ] **Service**: Create `AvailabilityService`
  - Methods: create_availability(), update_availability(), delete_availability()
  - Business logic: validate no overlapping slots, check employee exists
- [ ] **Controller**: Create `availability_controller.py`
  - Endpoints: POST /employees/{id}/availabilities, GET /employees/{id}/availabilities, PUT /availabilities/{id}, DELETE /availabilities/{id}
- [ ] **Tests**: Test availability creation, overlap detection, retrieval

**Dependencies:** US-1.1 (Employee model must exist)

---

### US-1.5: Absence and Leave Management

**As an** employee  
**I want** to request absences and leaves (vacation, sick leave, etc.)  
**So that** my manager knows when I'm not available

#### Acceptance Criteria
- ✅ Submit absence request with date range and type
- ✅ Absence types: vacation, sick leave, personal, unpaid
- ✅ Manager can approve or reject absence requests
- ✅ View absence status (pending, approved, rejected)
- ✅ Absences block scheduling during those dates

#### Technical Sub-tasks
- [ ] **Models**: Create `AbsenceType` and `Absence` models
  - `AbsenceType`: id, name (unique), description, requires_approval, is_paid
  - `Absence`: id, employee_id (FK), absence_type_id (FK), start_date, end_date, reason, status (pending/approved/rejected), approved_by_id (FK to Employee), created_at, updated_at
  - Relationships: employee (ManyToOne), absence_type (ManyToOne), approved_by (ManyToOne to Employee)
- [ ] **Schemas**: Create Pydantic schemas
  - `AbsenceTypeBase`, `AbsenceType` (response)
  - `AbsenceBase`, `AbsenceCreate`, `AbsenceUpdate`, `Absence` (response)
  - Validation: start_date <= end_date, valid status enum
- [ ] **Repository**: Create `AbsenceRepository`
  - Methods: get_by_employee(), get_by_status(), get_by_date_range(), get_pending_approvals()
- [ ] **Service**: Create `AbsenceService`
  - Methods: create_absence_request(), approve_absence(), reject_absence(), list_absences()
  - Business logic: validate date range, check employee exists, send notifications (future)
- [ ] **Controller**: Create `absence_controller.py`
  - Endpoints: POST /absences, GET /absences, GET /absences/{id}, PUT /absences/{id}/approve, PUT /absences/{id}/reject
- [ ] **Migrations**: Create Alembic migrations for AbsenceType and Absence tables
- [ ] **Tests**: Test absence creation, approval workflow, date validation

**Dependencies:** US-1.1 (Employee model), US-1.2 (Manager role for approval)

---

## 📅 Schedule Management

### US-1.6: Schedule Creation and Management

**As a** manager  
**I want** to create schedules for different time periods  
**So that** I can organize work shifts for my team

#### Acceptance Criteria
- ✅ Create schedule with name and date range
- ✅ Update schedule details
- ✅ Delete schedule
- ✅ View schedule details
- ✅ List all schedules with filtering by date range

#### Technical Sub-tasks
- [ ] **Models**: Create `Schedule` model
  - Fields: id, name, description, start_date, end_date, created_by_id (FK to Employee), status (draft/published/archived), created_at, updated_at
  - Relationships: created_by (ManyToOne to Employee), shifts (OneToMany)
- [ ] **Schemas**: Create Pydantic schemas
  - `ScheduleBase`, `ScheduleCreate`, `ScheduleUpdate`, `Schedule` (response)
  - Validation: start_date <= end_date, valid status
- [ ] **Repository**: Create `ScheduleRepository`
  - Methods: get_by_date_range(), get_by_status(), get_by_created_by()
- [ ] **Service**: Create `ScheduleService`
  - Methods: create_schedule(), update_schedule(), delete_schedule(), publish_schedule(), archive_schedule()
  - Business logic: validate dates, check creator permissions
- [ ] **Controller**: Create `schedule_controller.py`
  - Endpoints: POST /schedules, GET /schedules, GET /schedules/{id}, PUT /schedules/{id}, DELETE /schedules/{id}
- [ ] **Tests**: Test schedule CRUD operations, date validation, status transitions

**Dependencies:** US-1.1 (Employee model for created_by)

---

### US-1.7: Shift Management and Employee Assignment

**As a** manager  
**I want** to create shifts and assign employees to them  
**So that** I can define who works when

#### Acceptance Criteria
- ✅ Create shift with date, time, and position/role required
- ✅ Assign one or more employees to a shift
- ✅ Update shift details
- ✅ Remove employee from shift
- ✅ View all shifts in a schedule
- ✅ Track shift type (regular, overtime)

#### Technical Sub-tasks
- [ ] **Models**: Create `Shift` and `ShiftAssignment` models
  - `Shift`: id, schedule_id (FK), date, start_time, end_time, required_role_id (FK), min_employees, max_employees, notes, created_at, updated_at
  - `ShiftAssignment`: id, shift_id (FK), employee_id (FK), status (assigned/confirmed/completed), assignment_type (regular/overtime), created_at
  - Relationships: shift.schedule (ManyToOne), shift.assignments (OneToMany), shift.required_role (ManyToOne to Role)
- [ ] **Schemas**: Create Pydantic schemas
  - `ShiftBase`, `ShiftCreate`, `ShiftUpdate`, `Shift` (response with assignments)
  - `ShiftAssignmentBase`, `ShiftAssignmentCreate`, `ShiftAssignment` (response)
  - Validation: time order, employee capacity limits
- [ ] **Repository**: Create `ShiftRepository` and `ShiftAssignmentRepository`
  - Methods: get_by_schedule(), get_by_date_range(), get_by_employee(), check_employee_conflict()
- [ ] **Service**: Create `ShiftService`
  - Methods: create_shift(), assign_employee(), remove_employee(), update_shift()
  - Business logic: validate employee availability, check role match, prevent double-booking
- [ ] **Controller**: Create `shift_controller.py`
  - Endpoints: POST /schedules/{id}/shifts, GET /shifts, POST /shifts/{id}/assign, DELETE /shifts/{id}/assign/{employee_id}
- [ ] **Tests**: Test shift creation, employee assignment, conflict detection

**Dependencies:** US-1.6 (Schedule model), US-1.1 (Employee), US-1.2 (Role), US-1.4 (Availability check)

---

### US-1.8: Working Hours Tracking

**As a** manager  
**I want** to track different types of working hours (regular, part-time, overtime)  
**So that** I can ensure compliance with contracts and labor laws

#### Acceptance Criteria
- ✅ Calculate total hours per shift
- ✅ Classify hours as regular, part-time, or overtime
- ✅ Track weekly hours per employee
- ✅ Alert when approaching contract hour limits
- ✅ Generate hours summary per employee per week/month

#### Technical Sub-tasks
- [ ] **Models**: Extend `ShiftAssignment` model
  - Add computed fields: duration_hours (calculated from shift times)
  - Add field: is_overtime (boolean)
- [ ] **Service**: Extend `ShiftService` with hour calculation
  - Methods: calculate_shift_duration(), calculate_weekly_hours(), classify_hours_type()
  - Business logic: compare against contract_type.weekly_hours, flag overtime
- [ ] **Repository**: Extend `ShiftAssignmentRepository`
  - Methods: get_hours_by_employee_and_period(), get_overtime_shifts()
- [ ] **Controller**: Add endpoints to `shift_controller.py`
  - Endpoints: GET /employees/{id}/hours?start_date=&end_date=, GET /employees/{id}/overtime
- [ ] **Schemas**: Create summary schemas
  - `HoursSummary`: employee_id, period_start, period_end, regular_hours, overtime_hours, total_hours
- [ ] **Tests**: Test hour calculations, overtime detection, weekly summaries

**Dependencies:** US-1.7 (Shift and ShiftAssignment), US-1.3 (ContractType for limits)

---

### US-1.9: Schedule Visualization - Multiple Views

**As a** manager  
**I want** to view schedules in different formats (day, week, month)  
**So that** I can plan effectively at different time scales

#### Acceptance Criteria
- ✅ Day view: See all shifts for a specific date with assigned employees
- ✅ Week view: See shifts across 7 days
- ✅ Month view: See shifts across entire month
- ✅ Filter by employee, role, or location (if applicable)
- ✅ Export schedule data in structured format (JSON)

#### Technical Sub-tasks
- [ ] **Service**: Extend `ScheduleService` with view generators
  - Methods: get_day_view(), get_week_view(), get_month_view()
  - Business logic: aggregate shifts, group by date, include employee details
- [ ] **Repository**: Extend `ShiftRepository` with efficient queries
  - Methods: get_shifts_for_date(), get_shifts_for_week(), get_shifts_for_month()
  - Optimization: eager loading of related data (employees, roles)
- [ ] **Controller**: Add view endpoints to `schedule_controller.py`
  - Endpoints: GET /schedules/{id}/day-view?date=, GET /schedules/{id}/week-view?start_date=, GET /schedules/{id}/month-view?year=&month=
- [ ] **Schemas**: Create view response schemas
  - `DayView`: date, shifts (list of shifts with employees)
  - `WeekView`: start_date, end_date, days (list of day views)
  - `MonthView`: year, month, weeks (list of week views)
- [ ] **Tests**: Test view generation, date filtering, data aggregation

**Dependencies:** US-1.6 (Schedule), US-1.7 (Shifts), US-1.1 (Employee data)

---

# Phase 2 – Contrôles et optimisation basique

**Goal:** Réduire les erreurs et améliorer la fiabilité des plannings.

---

## ⚠️ Conflict Detection and Validation

### US-2.1: Automatic Conflict Detection

**As a** manager  
**I want** the system to detect scheduling conflicts automatically  
**So that** I don't double-book employees or violate their availability

#### Acceptance Criteria
- ✅ Detect when employee is assigned to overlapping shifts
- ✅ Detect when employee is assigned outside their availability
- ✅ Detect when employee is assigned during approved absence
- ✅ Prevent saving conflicting assignments (hard constraint)
- ✅ Display clear conflict messages

#### Technical Sub-tasks
- [ ] **Service**: Create `ConflictDetectionService`
  - Methods: check_shift_conflicts(), check_availability_conflicts(), check_absence_conflicts()
  - Business logic: time overlap calculation, availability matching, absence blocking
- [ ] **Repository**: Create helper queries in repositories
  - Methods: get_overlapping_shifts(), get_availability_for_date_time(), get_absences_for_date_range()
- [ ] **Service**: Extend `ShiftService` with conflict checking
  - Integrate conflict detection before saving assignments
  - Return detailed conflict information in exceptions
- [ ] **Schemas**: Create conflict response schemas
  - `ConflictError`: type (overlap/availability/absence), message, conflicting_shift_ids, employee_id
- [ ] **Controller**: Update `shift_controller.py` error handling
  - Return 409 Conflict status with detailed error information
- [ ] **Tests**: Test all conflict scenarios, edge cases (same time boundaries, etc.)

**Dependencies:** US-1.7 (Shifts), US-1.4 (Availability), US-1.5 (Absences)

---

### US-2.2: Working Hours Compliance Validation

**As a** manager  
**I want** to be alerted when scheduling violates hour limits  
**So that** I comply with labor laws and contract terms

#### Acceptance Criteria
- ✅ Alert when weekly hours exceed contract maximum
- ✅ Alert when daily hours exceed legal maximum (configurable, e.g., 10h)
- ✅ Alert when insufficient rest time between shifts (e.g., <11h)
- ✅ Warnings vs. hard blocks (configurable per rule)
- ✅ Track violation history

#### Technical Sub-tasks
- [ ] **Models**: Create `ComplianceRule` and `ComplianceViolation` models
  - `ComplianceRule`: id, name, rule_type (max_daily_hours/max_weekly_hours/min_rest_hours), threshold_value, is_blocking, is_active
  - `ComplianceViolation`: id, shift_assignment_id (FK), rule_id (FK), violation_date, severity (warning/error), message, resolved
- [ ] **Service**: Create `ComplianceService`
  - Methods: check_daily_hours(), check_weekly_hours(), check_rest_period(), validate_assignment()
  - Business logic: calculate hours, compare to rules, create violations
- [ ] **Repository**: Create `ComplianceRuleRepository` and `ComplianceViolationRepository`
  - Methods: get_active_rules(), log_violation(), get_unresolved_violations()
- [ ] **Service**: Integrate with `ShiftService`
  - Call compliance validation before finalizing assignments
  - Return warnings and errors separately
- [ ] **Controller**: Update assignment endpoints
  - Return compliance warnings in response (200 with warnings or 400 with errors)
- [ ] **Migrations**: Create tables for compliance rules and violations
- [ ] **Tests**: Test all compliance rules, threshold validation, blocking vs. warning behavior

**Dependencies:** US-1.8 (Hours tracking), US-1.7 (Shift assignments)

---

### US-2.3: Simple Alert System

**As a** manager  
**I want** to receive alerts for conflicts and compliance issues  
**So that** I can address problems proactively

#### Acceptance Criteria
- ✅ Generate alerts for scheduling conflicts
- ✅ Generate alerts for compliance violations
- ✅ Generate alerts for unassigned shifts
- ✅ View all active alerts
- ✅ Mark alerts as resolved
- ✅ Filter alerts by severity (info/warning/error)

#### Technical Sub-tasks
- [ ] **Models**: Create `Alert` model
  - Fields: id, alert_type (conflict/compliance/unassigned/other), severity (info/warning/error), title, message, related_shift_id, related_employee_id, is_resolved, resolved_at, created_at
  - Relationships: related_shift (ManyToOne), related_employee (ManyToOne)
- [ ] **Service**: Create `AlertService`
  - Methods: create_alert(), resolve_alert(), get_active_alerts(), get_alerts_by_type()
  - Business logic: auto-generate from conflicts and violations
- [ ] **Repository**: Create `AlertRepository`
  - Methods: get_unresolved(), get_by_severity(), get_by_employee()
- [ ] **Service**: Integrate with existing services
  - `ConflictDetectionService` → create conflict alerts
  - `ComplianceService` → create compliance alerts
  - `ShiftService` → create unassigned shift alerts
- [ ] **Controller**: Create `alert_controller.py`
  - Endpoints: GET /alerts, GET /alerts/{id}, PUT /alerts/{id}/resolve
- [ ] **Schemas**: Create Pydantic schemas
  - `AlertBase`, `Alert` (response)
- [ ] **Tests**: Test alert creation, resolution, filtering

**Dependencies:** US-2.1 (Conflict detection), US-2.2 (Compliance), US-1.7 (Shifts)

---

## 📊 Workload Tracking

### US-2.4: Employee Workload Analysis

**As a** manager  
**I want** to view workload distribution across my team  
**So that** I can balance work fairly

#### Acceptance Criteria
- ✅ Calculate total hours per employee for a period
- ✅ Identify under-utilized employees (below contract hours)
- ✅ Identify over-utilized employees (above contract hours)
- ✅ View workload comparison across team
- ✅ Generate workload reports (JSON/structured data)

#### Technical Sub-tasks
- [ ] **Service**: Create `WorkloadAnalysisService`
  - Methods: calculate_workload(), get_underutilized(), get_overutilized(), compare_workloads()
  - Business logic: aggregate hours, compare to contract hours, calculate utilization percentage
- [ ] **Repository**: Extend `ShiftAssignmentRepository`
  - Methods: get_total_hours_by_employee(), get_workload_summary()
  - Optimization: efficient aggregation queries
- [ ] **Schemas**: Create analysis schemas
  - `WorkloadSummary`: employee_id, employee_name, contract_hours, scheduled_hours, utilization_percentage, status (underutilized/balanced/overutilized)
  - `TeamWorkloadReport`: period_start, period_end, employees (list of WorkloadSummary)
- [ ] **Controller**: Create `analytics_controller.py`
  - Endpoints: GET /analytics/workload?start_date=&end_date=, GET /analytics/workload/employee/{id}
- [ ] **Tests**: Test workload calculations, status classification, report generation

**Dependencies:** US-1.8 (Hours tracking), US-1.3 (Contract types with hour limits)

---

### US-2.5: Schedule Completion Indicators

**As a** manager  
**I want** to see how complete my schedules are  
**So that** I know what still needs to be planned

#### Acceptance Criteria
- ✅ Calculate percentage of shifts with full assignments
- ✅ List unassigned or partially assigned shifts
- ✅ Show total required vs. assigned employee count
- ✅ Highlight gaps by date and role
- ✅ Dashboard view with schedule health metrics

#### Technical Sub-tasks
- [ ] **Service**: Extend `ScheduleService` with completion analysis
  - Methods: calculate_completion_rate(), get_unassigned_shifts(), get_coverage_gaps()
  - Business logic: count assigned vs. required positions
- [ ] **Schemas**: Create completion schemas
  - `ScheduleCompletion`: schedule_id, total_shifts, fully_assigned, partially_assigned, unassigned, completion_percentage
  - `CoverageGap`: date, shift_id, required_employees, assigned_employees, missing_count, required_role
- [ ] **Controller**: Add endpoints to `schedule_controller.py`
  - Endpoints: GET /schedules/{id}/completion, GET /schedules/{id}/gaps
- [ ] **Service**: Add dashboard aggregation
  - Method: get_schedule_dashboard() → overall metrics
- [ ] **Tests**: Test completion calculations, gap identification

**Dependencies:** US-1.7 (Shifts with min/max employee counts)

---

# Phase 3 – Intelligence artificielle légère (pertinente)

**Goal:** Assister les managers dans la prise de décision.

---

## 🤖 AI-Assisted Scheduling

### US-3.1: Smart Employee Assignment Recommendations

**As a** manager  
**I want** to receive AI-powered employee assignment suggestions  
**So that** I can fill shifts more efficiently

#### Acceptance Criteria
- ✅ For an unassigned shift, suggest best-fit employees
- ✅ Ranking based on: availability, role match, current workload, past assignments
- ✅ Show confidence score for each suggestion
- ✅ Explain why each employee is recommended
- ✅ Exclude employees with conflicts or absences

#### Technical Sub-tasks
- [ ] **External Dependencies**: Add ML library to requirements
  - `scikit-learn==1.4.0` or lightweight alternative
  - `numpy==1.26.0` for calculations
- [ ] **Service**: Create `RecommendationService`
  - Methods: recommend_for_shift(), score_employee_fit(), explain_recommendation()
  - Scoring factors: availability_match (weight: 0.3), role_match (0.3), workload_balance (0.2), preference_history (0.2)
  - Business logic: normalize scores, rank by total score, filter conflicts
- [ ] **Models**: Create `AssignmentPreference` model (for learning)
  - Fields: id, employee_id, shift_type, preference_score (historical data from successful assignments)
- [ ] **Repository**: Create `RecommendationRepository`
  - Methods: get_assignment_history(), get_employee_preferences()
- [ ] **Schemas**: Create recommendation schemas
  - `EmployeeRecommendation`: employee_id, employee_name, score, confidence, explanation, conflicts (list)
  - `ShiftRecommendations`: shift_id, recommendations (list of EmployeeRecommendation)
- [ ] **Controller**: Create `recommendation_controller.py`
  - Endpoints: GET /shifts/{id}/recommendations, POST /recommendations/feedback
- [ ] **Algorithm**: Implement scoring function
  - Weighted sum of normalized factors
  - Conflict filtering (zero score if any hard conflict)
- [ ] **Tests**: Test recommendation generation, scoring accuracy, conflict exclusion

**Dependencies:** US-1.7 (Shifts), US-1.4 (Availability), US-2.1 (Conflict detection), US-2.4 (Workload)

---

### US-3.2: Intelligent Alerts and Insights

**As a** manager  
**I want** to receive proactive alerts about potential scheduling issues  
**So that** I can address them before they become problems

#### Acceptance Criteria
- ✅ Alert when schedule has low completion rate close to start date
- ✅ Alert when certain employees consistently underutilized
- ✅ Alert when patterns suggest burnout risk (too many consecutive shifts)
- ✅ Suggest schedule optimizations
- ✅ Prioritize alerts by urgency and impact

#### Technical Sub-tasks
- [ ] **Service**: Create `InsightService`
  - Methods: detect_completion_risk(), detect_underutilization_pattern(), detect_burnout_risk(), generate_insights()
  - Heuristics: completion < 70% within 3 days of start, employee at < 60% utilization for 4+ weeks, 7+ consecutive days scheduled
- [ ] **Models**: Extend `Alert` model with insight-specific fields
  - Add field: insight_type (completion_risk/underutilization/burnout/optimization)
  - Add field: recommended_action (text suggestion)
- [ ] **Service**: Create scheduled analysis job structure (async task placeholder)
  - Method: run_periodic_insights() → generate insights for all active schedules
  - Note: Actual scheduling (Celery/APScheduler) in future iteration
- [ ] **Controller**: Add insights endpoints to `alert_controller.py`
  - Endpoints: GET /insights, GET /insights/schedule/{id}
- [ ] **Schemas**: Create insight schemas
  - `Insight`: type, severity, title, description, recommended_action, affected_entities (employees/shifts)
- [ ] **Tests**: Test pattern detection, alert generation, action recommendations

**Dependencies:** US-2.3 (Alert system), US-2.4 (Workload analysis), US-2.5 (Schedule completion)

---

### US-3.3: Workload Rebalancing Suggestions

**As a** manager  
**I want** to receive suggestions to rebalance workload  
**So that** I can distribute work more fairly

#### Acceptance Criteria
- ✅ Identify imbalanced schedules (high variance in employee hours)
- ✅ Suggest shift reassignments to improve balance
- ✅ Show before/after workload distribution
- ✅ Ensure suggestions don't create conflicts
- ✅ Allow applying suggestions with one action

#### Technical Sub-tasks
- [ ] **Service**: Create `RebalancingService`
  - Methods: detect_imbalance(), generate_rebalancing_plan(), apply_rebalancing()
  - Algorithm: calculate variance in utilization, identify swappable shifts, simulate reassignments
  - Business logic: validate all suggestions against conflicts and compliance
- [ ] **Schemas**: Create rebalancing schemas
  - `RebalancingProposal`: schedule_id, current_variance, proposed_variance, shift_changes (list of ShiftChange)
  - `ShiftChange`: shift_id, current_employee_id, proposed_employee_id, reason
- [ ] **Controller**: Add endpoints to `recommendation_controller.py`
  - Endpoints: GET /schedules/{id}/rebalancing-proposals, POST /schedules/{id}/apply-rebalancing
- [ ] **Service**: Integration with conflict detection
  - Validate each proposed change doesn't violate constraints
- [ ] **Algorithm**: Implement simple rebalancing heuristic
  - Identify overutilized (>110%) and underutilized (<90%) employees
  - Find shifts from overutilized that can move to underutilized
  - Prioritize shifts with fewer dependencies
- [ ] **Tests**: Test imbalance detection, proposal generation, conflict-free validation

**Dependencies:** US-2.4 (Workload analysis), US-2.1 (Conflict detection), US-1.7 (Shift reassignment)

---

# Phase 4 – IA avancée (optionnelle)

**Goal:** Automatisation partielle des plannings.

---

## 🧠 Advanced AI Features

### US-4.1: Semi-Automatic Schedule Generation

**As a** manager  
**I want** the system to generate a draft schedule automatically  
**So that** I save time on initial planning

#### Acceptance Criteria
- ✅ Generate complete schedule for a date range given constraints
- ✅ Input: required shifts (times, roles, coverage), employee pool
- ✅ Output: optimized assignment plan
- ✅ Respect all constraints: availability, absences, contract hours, compliance rules
- ✅ Optimize for: workload balance, employee preferences, minimal conflicts
- ✅ Allow manual adjustments after generation

#### Technical Sub-tasks
- [ ] **External Dependencies**: Add optimization library
  - `pulp==2.7.0` or `ortools==9.8.0` (constraint satisfaction)
- [ ] **Service**: Create `ScheduleGeneratorService`
  - Methods: generate_schedule(), define_constraints(), optimize_assignments()
  - Constraints: availability, absences, max hours, min rest, role requirements
  - Objective function: minimize workload variance + maximize preference match
- [ ] **Models**: Create `ScheduleTemplate` model
  - Fields: id, name, default_shifts (JSON structure), rules (JSON)
  - Usage: define recurring schedule patterns
- [ ] **Service**: Implement constraint satisfaction problem (CSP)
  - Variables: employee assignments to shifts
  - Domain: eligible employees per shift
  - Constraints: no conflicts, hour limits, coverage requirements
  - Solution: use LP solver or genetic algorithm
- [ ] **Schemas**: Create generation schemas
  - `ScheduleGenerationRequest`: date_range, template_id, required_coverage, preferences
  - `GeneratedSchedule`: schedule_id, shifts (list), assignments, quality_score, warnings
- [ ] **Controller**: Create `generation_controller.py`
  - Endpoints: POST /schedules/generate, GET /schedules/templates
- [ ] **Algorithm**: Multi-stage generation
  1. Load constraints and preferences
  2. Generate feasible assignments (CSP solver)
  3. Optimize for objectives (linear programming)
  4. Validate and return with quality metrics
- [ ] **Tests**: Test generation with various constraints, edge cases, performance benchmarks

**Dependencies:** US-1.6 (Schedules), US-1.7 (Shifts), US-2.1 (Conflict detection), US-2.2 (Compliance), US-3.1 (Recommendations)

**Note:** This is computationally intensive. Consider async task processing for large schedules.

---

### US-4.2: Dynamic Schedule Optimization

**As a** manager  
**I want** the system to suggest schedule improvements based on real activity  
**So that** I can adapt to changing business needs

#### Acceptance Criteria
- ✅ Analyze past schedules vs. actual needs (requires activity data)
- ✅ Identify patterns: busy periods, overstaffing, understaffing
- ✅ Suggest schedule adjustments for upcoming periods
- ✅ Learn from manager's acceptance/rejection of suggestions
- ✅ Improve recommendations over time

#### Technical Sub-tasks
- [ ] **Models**: Create `ActivityLog` model (requires external data integration)
  - Fields: id, date, hour, actual_workload_metric, scheduled_employees, notes
  - Purpose: track actual business activity for learning
- [ ] **Models**: Create `OptimizationFeedback` model
  - Fields: id, suggestion_id, was_accepted, manager_id, feedback_notes, created_at
  - Purpose: reinforcement learning data
- [ ] **Service**: Create `LearningService`
  - Methods: analyze_historical_data(), predict_workload(), improve_model()
  - ML approach: time series forecasting for workload, feedback-based weight adjustment
- [ ] **External Dependencies**: Add ML libraries
  - `pandas==2.2.0` for data analysis
  - `statsmodels==0.14.0` or `prophet==1.1.0` for forecasting
- [ ] **Service**: Create `OptimizationService`
  - Methods: suggest_optimizations(), compare_schedules(), calculate_efficiency_gain()
  - Business logic: compare predicted vs. scheduled coverage, identify gaps/excesses
- [ ] **Schemas**: Create optimization schemas
  - `OptimizationSuggestion`: type, description, affected_shifts, expected_improvement, confidence
  - `ScheduleEfficiency`: schedule_id, coverage_accuracy, workload_balance, compliance_score, overall_score
- [ ] **Controller**: Create `optimization_controller.py`
  - Endpoints: POST /schedules/{id}/optimize, GET /schedules/{id}/efficiency, POST /feedback
- [ ] **Algorithm**: Iterative improvement
  1. Baseline: current schedule quality metrics
  2. Generate alternative assignments
  3. Predict outcomes using historical patterns
  4. Rank alternatives by predicted efficiency
  5. Present top suggestions with confidence scores
- [ ] **Tests**: Test pattern recognition, prediction accuracy, feedback integration

**Dependencies:** US-4.1 (Schedule generation), US-2.4 (Workload analysis), US-3.2 (Insights)

**Note:** Requires significant historical data to be effective. Phase implementation with mock data first.

---

### US-4.3: Preference Learning and Personalization

**As a** manager  
**I want** the system to learn employee preferences and scheduling patterns  
**So that** automatic suggestions align with team dynamics

#### Acceptance Criteria
- ✅ Track which shift types employees are typically assigned to
- ✅ Learn preferred shift partners (who works well together)
- ✅ Identify employees who prefer/avoid certain days or times
- ✅ Factor learned preferences into recommendations
- ✅ Allow explicit preference input from employees

#### Technical Sub-tasks
- [ ] **Models**: Create `EmployeePreference` model
  - Fields: id, employee_id, preference_type (shift_time/day_of_week/colleague/shift_type), preference_value (JSON), strength (0.0-1.0), is_explicit, created_at
- [ ] **Models**: Create `PreferredColleague` model
  - Fields: id, employee_id, preferred_colleague_id, strength (learned from co-assignments), created_at
- [ ] **Service**: Create `PreferenceLearningService`
  - Methods: learn_from_assignments(), calculate_preference_strength(), get_employee_preferences()
  - Learning approach: frequency analysis, pattern mining from historical assignments
- [ ] **Repository**: Create `PreferenceRepository`
  - Methods: get_preferences_by_employee(), get_preferred_colleagues(), update_preference_strength()
- [ ] **Service**: Integrate with `RecommendationService`
  - Enhance scoring function with preference factors
  - Increase score for matches with learned preferences
- [ ] **Schemas**: Create preference schemas
  - `PreferenceInput`: preference_type, value, strength
  - `LearnedPreference`: type, value, confidence, source (learned/explicit)
- [ ] **Controller**: Create `preference_controller.py`
  - Endpoints: POST /employees/{id}/preferences, GET /employees/{id}/preferences, GET /employees/{id}/learned-patterns
- [ ] **Algorithm**: Pattern mining
  - Analyze past 3-6 months of assignments
  - Calculate frequency of shift types, days, times per employee
  - Identify co-occurrence patterns (who works together often)
  - Assign confidence scores based on sample size and consistency
- [ ] **Tests**: Test pattern detection, preference learning, integration with recommendations

**Dependencies:** US-3.1 (Recommendations), US-1.7 (Shift assignments with history)

**Note:** Privacy consideration - ensure employees can view and override learned preferences.

---

## 🔧 Infrastructure and Supporting Features

### US-0.1: Database Setup and Migrations

**Technical task for initial setup**

#### Sub-tasks
- [ ] Configure PostgreSQL connection in database.py
- [ ] Set up Alembic for migrations
- [ ] Create initial migration with all Phase 1 models
- [ ] Create seed data script for roles, contract types, absence types
- [ ] Document migration workflow in README

**Dependencies:** None (foundational)

---

### US-0.2: Authentication and Authorization

**As a** user  
**I want** to log in securely  
**So that** only authorized people can access the system

#### Sub-tasks
- [ ] **Models**: Create `User` model (may merge with Employee or separate)
  - Fields: id, email (unique), hashed_password, is_active, employee_id (FK)
- [ ] **Security**: Implement JWT authentication
  - Add `python-jose[cryptography]==3.3.0`, `passlib[bcrypt]==1.7.4` to requirements
- [ ] **Service**: Create `AuthService`
  - Methods: register(), login(), verify_token(), hash_password()
- [ ] **Controller**: Create `auth_controller.py`
  - Endpoints: POST /auth/register, POST /auth/login, POST /auth/logout
- [ ] **Middleware**: Add authentication dependency for protected routes
- [ ] **Authorization**: Role-based permissions (manager vs employee)

**Dependencies:** US-1.1 (Employee), US-1.2 (Role)

---

### US-0.3: API Documentation and Testing Setup

**Technical task for development quality**

#### Sub-tasks
- [ ] Ensure OpenAPI/Swagger docs are comprehensive
- [ ] Add request/response examples to all endpoints
- [ ] Set up pytest with fixtures for database testing
- [ ] Create test database configuration
- [ ] Implement test coverage reporting (pytest-cov)
- [ ] Document API usage in README with examples

**Dependencies:** None (ongoing)

---

### US-0.4: Error Handling and Logging

**Technical task for production readiness**

#### Sub-tasks
- [ ] Implement centralized error handling
- [ ] Create custom exception classes (NotFoundError, ConflictError, ValidationError)
- [ ] Add logging configuration (Python logging module)
- [ ] Log all API requests and errors
- [ ] Add health check endpoint (GET /health)
- [ ] Add version endpoint (GET /version)

**Dependencies:** None (ongoing)

---

## 📝 Development Guidelines

### Code Quality Standards
- [ ] Follow PEP 8 style guide
- [ ] Type hints for all function signatures
- [ ] Docstrings for all classes and public methods
- [ ] Minimum 80% test coverage
- [ ] All tests passing before merge

### Git Workflow
- [ ] Feature branches from main
- [ ] Descriptive commit messages
- [ ] One US or sub-task per PR when possible
- [ ] Code review required before merge

### Priority Execution Order

**Sprint 1: Core Foundation**
1. US-0.1 (Database setup)
2. US-1.1 (Employee profiles)
3. US-1.2 (Roles)
4. US-1.3 (Contract types)

**Sprint 2: Employee Features**
5. US-1.4 (Availability)
6. US-1.5 (Absences)
7. US-0.2 (Authentication)

**Sprint 3: Schedule Foundation**
8. US-1.6 (Schedule creation)
9. US-1.7 (Shifts and assignments)
10. US-1.8 (Hours tracking)

**Sprint 4: Visualization and Validation**
11. US-1.9 (Schedule views)
12. US-2.1 (Conflict detection)
13. US-2.2 (Compliance)

**Sprint 5: Analytics and Alerts**
14. US-2.3 (Alert system)
15. US-2.4 (Workload analysis)
16. US-2.5 (Schedule completion)

**Sprint 6: AI Foundation**
17. US-3.1 (Recommendations)
18. US-3.2 (Intelligent alerts)
19. US-3.3 (Rebalancing)

**Sprint 7+: Advanced AI (Optional)**
20. US-4.1 (Auto-generation)
21. US-4.2 (Optimization)
22. US-4.3 (Preference learning)

---

## 📚 External Dependencies Summary

### Phase 1-2 (Required)
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
psycopg2-binary==2.9.9
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
pytest-cov==4.1.0
```

### Phase 3 (AI Light)
```txt
scikit-learn==1.4.0
numpy==1.26.0
```

### Phase 4 (AI Advanced)
```txt
pulp==2.7.0  # or ortools==9.8.0
pandas==2.2.0
statsmodels==0.14.0  # or prophet==1.1.0
```

---

## ✅ Definition of Done

A User Story is considered **Done** when:
- [ ] All sub-tasks completed
- [ ] Code reviewed and approved
- [ ] Unit tests written and passing (>80% coverage for new code)
- [ ] Integration tests passing
- [ ] API documented in Swagger
- [ ] Alembic migration created (if DB changes)
- [ ] No critical bugs or security issues
- [ ] Acceptance criteria validated
- [ ] Merged to main branch

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-11  
**Status:** Ready for Implementation

