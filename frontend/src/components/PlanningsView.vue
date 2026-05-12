<template>
    <div class="plannings-view">
        <div class="d-flex flex-column flex-lg-row justify-space-between align-lg-center mb-6 mt-2">
            <div class="mb-4 mb-lg-0">
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Plannings</h1>
                <p class="text-body-1 text-grey-darken-1">Gérez les services et assignez votre équipe.</p>
            </div>

            <div class="d-flex flex-column flex-sm-row align-stretch align-sm-center gap-4">
                <v-btn-toggle v-model="currentView" mandatory color="primary" variant="outlined"
                    class="bg-white flex-grow-1 flex-sm-grow-0" rounded="lg" divided>
                    <v-btn value="day" class="font-weight-bold text-body-2 flex-grow-1" height="40">Jour</v-btn>
                    <v-btn value="week" class="font-weight-bold text-body-2 flex-grow-1" height="40">Semaine</v-btn>
                    <v-btn value="month" class="font-weight-bold text-body-2 flex-grow-1" height="40">Mois</v-btn>
                </v-btn-toggle>

                <div class="d-flex align-center justify-space-between bg-white border rounded-lg px-2"
                    style="height: 40px;">
                    <v-btn icon="mdi-chevron-left" variant="text" size="small" color="grey-darken-2"
                        @click="navigate(-1)"></v-btn>
                    <span class="px-2 font-weight-bold text-body-2 text-sm-body-1 text-center"
                        style="min-width: 130px;">
                        {{ headerLabel }}
                    </span>
                    <v-btn icon="mdi-chevron-right" variant="text" size="small" color="grey-darken-2"
                        @click="navigate(1)"></v-btn>
                </div>
            </div>
        </div>

        <div v-if="currentView === 'day'" class="day-view">
            <v-card border elevation="0" rounded="xl" class="pa-4 pa-md-6 bg-white">
                <div class="d-flex flex-column flex-sm-row justify-space-between align-sm-center mb-6 gap-3">
                    <h2 class="text-h6 font-weight-bold">{{ getFullDateLabel(baseDate) }}</h2>
                    <v-btn color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus"
                        @click="openNewShiftModal(baseDateStr)">
                        Ajouter un shift
                    </v-btn>
                </div>

                <div v-if="shiftsForDay(baseDateStr).length === 0"
                    class="text-center py-10 bg-grey-lighten-4 rounded-lg border-dashed">
                    <v-icon color="grey" size="48" class="mb-2">mdi-calendar-blank</v-icon>
                    <p class="text-grey-darken-1 font-weight-medium">Aucun shift planifié pour cette journée.</p>
                </div>

                <v-list v-else class="bg-transparent" lines="two">
                    <v-card v-for="shift in shiftsForDay(baseDateStr)" :key="shift.id" border elevation="0" rounded="lg"
                        class="mb-3 px-4 py-3 d-flex flex-column flex-sm-row align-sm-center justify-space-between shift-card-horizontal cursor-pointer"
                        :class="{ 'unassigned-border': !shift.employeeId }"
                        :style="`border-left: 4px solid ${!shift.employeeId ? '#E11D48' : getRoleColor(shift.roleName)} !important;`"
                        @click="editExistingShift(shift)">

                        <div class="d-flex align-center mb-3 mb-sm-0">
                            <div class="time-block mr-4 mr-sm-6 text-center">
                                <div class="text-subtitle-1 text-sm-h6 font-weight-bold">{{ shift.startTime }}</div>
                                <div class="text-caption text-grey-darken-1">{{ shift.endTime }}</div>
                            </div>
                            <v-avatar :color="!shift.employeeId ? 'error-lighten-4' : 'grey-lighten-3'" size="40"
                                class="mr-3 mr-sm-4 rounded-lg">
                                <span v-if="shift.employeeId" class="font-weight-bold">{{ shift.employeeName.charAt(0)
                                }}</span>
                                <v-icon v-else color="error">mdi-account-alert</v-icon>
                            </v-avatar>
                            <div>
                                <div class="font-weight-bold text-body-2 text-sm-body-1"
                                    :class="{ 'text-error': !shift.employeeId }">
                                    {{ shift.employeeName || 'Shift Non Assigné' }}
                                </div>
                                <div class="text-caption text-grey-darken-1">{{ shift.roleName }}</div>
                            </div>
                        </div>
                        <v-chip :color="getRoleColor(shift.roleName)" variant="tonal" size="small"
                            class="font-weight-bold align-self-start align-self-sm-center">{{ shift.status }}</v-chip>
                    </v-card>
                </v-list>
            </v-card>
        </div>

        <div v-else-if="currentView === 'week'" class="week-view">
            <div class="d-flex flex-nowrap gap-4 overflow-x-auto custom-scrollbar pb-6 pt-2" style="min-height: 60vh;">
                <div v-for="day in weekDays" :key="day.date" class="day-column d-flex flex-column">
                    <div class="day-header text-center py-2 py-sm-3 mb-3 rounded-lg border bg-white flex-shrink-0"
                        :class="{ 'border-primary bg-primary-lighten-5': day.isToday }">
                        <div class="text-uppercase text-caption font-weight-bold text-grey-darken-1 mb-1">{{ day.dayName
                        }}</div>
                        <div class="text-h6 font-weight-bold" :class="{ 'text-primary': day.isToday }">{{ day.dayNumber
                        }}</div>
                    </div>

                    <div class="shifts-container d-flex flex-column flex-grow-1">
                        <div class="flex-grow-1 mb-2">
                            <v-card v-for="shift in shiftsForDay(day.date)" :key="shift.id" border elevation="0"
                                rounded="lg" class="mb-3 shift-card pa-3 pa-sm-4 bg-white cursor-pointer"
                                :style="`border-left: 4px solid ${!shift.employeeId ? '#E11D48' : getRoleColor(shift.roleName)} !important;`"
                                @click.stop="editExistingShift(shift)">
                                <div class="d-flex justify-space-between align-start mb-2 mb-sm-3">
                                    <span class="font-weight-bold text-body-2 text-sm-body-1">{{ shift.startTime }} - {{
                                        shift.endTime }}</span>
                                </div>
                                <div v-if="shift.employeeId" class="d-flex align-center mt-2">
                                    <v-avatar color="grey-lighten-3" size="24" rounded="sm"
                                        class="mr-2 mr-sm-3 text-caption font-weight-bold">
                                        {{ shift.employeeName.charAt(0) }}
                                    </v-avatar>
                                    <span
                                        class="text-caption text-sm-body-2 font-weight-medium text-grey-darken-3 text-truncate">{{
                                            shift.employeeName }}</span>
                                </div>
                                <div v-else
                                    class="d-flex align-center mt-2 text-error bg-red-lighten-5 pa-1 pa-sm-2 rounded">
                                    <v-icon size="small" class="mr-1 mr-sm-2">mdi-alert-circle-outline</v-icon>
                                    <span class="text-caption font-weight-bold">Non assigné</span>
                                </div>
                            </v-card>
                        </div>

                        <v-btn variant="outlined" color="grey-darken-1"
                            class="w-100 border-dashed mt-auto bg-transparent" rounded="lg" prepend-icon="mdi-plus"
                            height="40" @click="openNewShiftModal(day.date)">
                            Ajouter
                        </v-btn>
                    </div>
                </div>
            </div>
        </div>

        <div v-else-if="currentView === 'month'" class="month-view">
            <v-card border elevation="0" rounded="xl" class="overflow-hidden bg-white">
                <div class="month-grid-header border-bottom bg-grey-lighten-4">
                    <div v-for="day in ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']" :key="day"
                        class="pa-2 pa-sm-3 text-center text-xs text-sm-caption font-weight-bold text-grey-darken-1">
                        {{ day }}
                    </div>
                </div>
                <div class="month-grid">
                    <div v-for="cell in monthCells" :key="cell.date" class="month-cell pa-1 pa-sm-2"
                        :class="{ 'bg-grey-lighten-5 text-grey': !cell.isCurrentMonth, 'bg-primary-lighten-5': cell.isToday }"
                        @click="openNewShiftModal(cell.date)">

                        <div class="d-flex justify-space-between align-start mb-1 mb-sm-2">
                            <span class="text-xs text-sm-caption font-weight-bold"
                                :class="{ 'text-primary': cell.isToday }">{{ cell.dayNumber }}</span>
                            <v-icon v-if="shiftsForDay(cell.date).some(s => !s.employeeId)" color="error" size="x-small"
                                class="d-none d-sm-flex">mdi-circle</v-icon>
                        </div>

                        <div class="d-flex flex-column gap-1">
                            <div v-for="shift in shiftsForDay(cell.date).slice(0, 3)" :key="shift.id"
                                class="text-truncate px-1 px-sm-2 rounded-sm text-micro text-sm-xs font-weight-medium cursor-pointer"
                                :style="`background-color: ${!shift.employeeId ? '#FFE4E6' : '#F1F5F9'}; color: ${!shift.employeeId ? '#E11D48' : '#334155'}; padding: 2px 4px;`"
                                @click.stop="editExistingShift(shift)">
                                <span class="d-none d-sm-inline">{{ shift.startTime }}</span>
                                {{ shift.employeeName ? shift.employeeName.split(' ')[0] : 'Vide' }}
                            </div>
                            <div v-if="shiftsForDay(cell.date).length > 3"
                                class="text-micro text-grey-darken-1 pl-1 mt-1">
                                +{{ shiftsForDay(cell.date).length - 3 }} <span class="d-none d-sm-inline">autres</span>
                            </div>
                        </div>
                    </div>
                </div>
            </v-card>
        </div>

        <v-dialog v-model="shiftDialog" max-width="500" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ isEditing ? 'Modifier le shift' : 'Ajouter un shift' }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="closeShiftModal"></v-btn>
                </v-card-title>

                <v-card-text class="px-6 pt-4">
                    <div class="text-subtitle-2 text-grey-darken-1 mb-4">
                        <v-icon size="small" class="mr-1">mdi-calendar</v-icon>
                        {{ getFullDateLabel(editedShift.date) }}
                    </div>

                    <v-row>
                        <v-col cols="6" class="pb-1">
                            <v-text-field v-model="editedShift.startTime" label="Début" type="time" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="6" class="pb-1">
                            <v-text-field v-model="editedShift.endTime" label="Fin" type="time" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" class="py-1">
                            <v-select v-model="editedShift.roleId" label="Rôle requis" :items="roleStore.roles"
                                item-title="name" item-value="id" variant="outlined" density="comfortable"
                                color="primary"></v-select>
                        </v-col>
                        <v-col cols="12" class="pt-1">
                            <v-select v-model="editedShift.employeeId" label="Assigner à (Optionnel)"
                                :items="employeeStore.employees" item-title="firstName" item-value="id"
                                variant="outlined" density="comfortable" color="primary" clearable
                                placeholder="Laisser vide pour assigner plus tard"></v-select>
                        </v-col>
                    </v-row>
                </v-card-text>

                <v-divider class="mt-2"></v-divider>

                <v-card-actions class="px-6 py-4 d-flex justify-space-between bg-grey-lighten-4">
                    <div>
                        <v-btn v-if="isEditing" variant="text" color="error" class="font-weight-medium px-2"
                            prepend-icon="mdi-delete" @click="deleteConfirmDialog = true">
                            <span class="d-none d-sm-inline">Supprimer</span>
                        </v-btn>
                    </div>
                    <div>
                        <v-btn variant="text" color="grey-darken-2" class="mr-2 font-weight-medium"
                            @click="closeShiftModal">Annuler</v-btn>
                        <v-btn variant="flat" color="primary" rounded="lg" class="px-4 font-weight-bold"
                            @click="saveShift">Enregistrer</v-btn>
                    </div>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="deleteConfirmDialog" max-width="400">
            <v-card rounded="xl" elevation="0" border class="pa-4 text-center">
                <v-avatar color="#FEF2F2" size="64" class="mx-auto mt-4 mb-4">
                    <v-icon color="error" size="32">mdi-delete-outline</v-icon>
                </v-avatar>
                <h3 class="text-h6 font-weight-bold mb-2">Supprimer ce shift ?</h3>
                <p class="text-body-2 text-grey-darken-1 mb-6 px-4">
                    Êtes-vous sûr de vouloir supprimer le shift de <strong>{{ editedShift.startTime }}</strong> ? Cette
                    action est irréversible.
                </p>
                <div class="d-flex justify-center mb-2">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium" rounded="lg"
                        @click="deleteConfirmDialog = false">Annuler</v-btn>
                    <v-btn variant="flat" color="error" rounded="lg" class="px-6 font-weight-bold"
                        @click="executeDelete">Oui, supprimer</v-btn>
                </div>
            </v-card>
        </v-dialog>

        <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000" location="bottom right"
            rounded="pill">
            <div class="d-flex align-center font-weight-medium">
                <v-icon size="small" class="mr-2">{{ snackbar.icon }}</v-icon>
                {{ snackbar.text }}
            </div>
        </v-snackbar>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useScheduleStore } from '../stores/scheduleStore'
import { useEmployeeStore } from '../stores/employeeStore'
import { useRoleStore } from '../stores/roleStore'

const scheduleStore = useScheduleStore()
const employeeStore = useEmployeeStore()
const roleStore = useRoleStore()

const currentView = ref('week')
const baseDate = ref(new Date('2023-10-24'))
const baseDateStr = computed(() => baseDate.value.toISOString().split('T')[0])

const deleteConfirmDialog = ref(false)
const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })

const showNotification = (text, type = 'success') => {
    snackbar.value = {
        show: true,
        text,
        color: type,
        icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
    }
}

const navigate = (direction) => {
    const newDate = new Date(baseDate.value)
    if (currentView.value === 'day') newDate.setDate(newDate.getDate() + direction)
    else if (currentView.value === 'week') newDate.setDate(newDate.getDate() + (direction * 7))
    else if (currentView.value === 'month') newDate.setMonth(newDate.getMonth() + direction)
    baseDate.value = newDate
}

const headerLabel = computed(() => {
    const opts = { month: 'long', year: 'numeric' }
    if (currentView.value === 'day') {
        return baseDate.value.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })
    } else if (currentView.value === 'week') {
        if (weekDays.value.length === 0) return ''
        const start = new Date(weekDays.value[0].date)
        const end = new Date(weekDays.value[6].date)
        return `${start.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })} - ${end.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}`
    } else {
        const label = baseDate.value.toLocaleDateString('fr-FR', opts)
        return label.charAt(0).toUpperCase() + label.slice(1)
    }
})

const getFullDateLabel = (dateObj) => {
    if (!dateObj) return '';
    const d = typeof dateObj === 'string' ? new Date(dateObj) : dateObj;
    const label = d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    return label.charAt(0).toUpperCase() + label.slice(1);
}

const shiftsForDay = (dateStr) => {
    return scheduleStore.getShiftsByDate(dateStr) || []
}

const weekDays = computed(() => {
    const days = []
    const startOfWeek = new Date(baseDate.value)
    const day = startOfWeek.getDay()
    const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1)
    startOfWeek.setDate(diff)
    const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
    for (let i = 0; i < 7; i++) {
        const currentDate = new Date(startOfWeek)
        currentDate.setDate(startOfWeek.getDate() + i)
        const dateString = currentDate.toISOString().split('T')[0]
        days.push({
            date: dateString,
            dayName: dayNames[currentDate.getDay()],
            dayNumber: currentDate.getDate(),
            isToday: dateString === new Date().toISOString().split('T')[0]
        })
    }
    return days
})

const monthCells = computed(() => {
    const cells = []
    const year = baseDate.value.getFullYear()
    const month = baseDate.value.getMonth()
    const firstDayOfMonth = new Date(year, month, 1)
    let startDayOfWeek = firstDayOfMonth.getDay()
    if (startDayOfWeek === 0) startDayOfWeek = 7
    const startDate = new Date(year, month, 1 - (startDayOfWeek - 1))
    const todayStr = new Date().toISOString().split('T')[0]

    for (let i = 0; i < 42; i++) {
        const d = new Date(startDate)
        d.setDate(startDate.getDate() + i)
        const dateString = d.toISOString().split('T')[0]
        cells.push({
            date: dateString,
            dayNumber: d.getDate(),
            isCurrentMonth: d.getMonth() === month,
            isToday: dateString === todayStr
        })
    }
    return cells
})

const shiftDialog = ref(false)
const isEditing = ref(false)
const editedShiftId = ref(null)

const defaultShift = {
    date: '',
    startTime: '18:00',
    endTime: '23:30',
    roleId: null,
    employeeId: null
}
const editedShift = ref({ ...defaultShift })

const openNewShiftModal = (date) => {
    isEditing.value = false
    editedShiftId.value = null
    editedShift.value = { ...defaultShift, date: date }
    shiftDialog.value = true
}

const editExistingShift = (shift) => {
    isEditing.value = true
    editedShiftId.value = shift.id
    editedShift.value = { ...shift }
    shiftDialog.value = true
}

const closeShiftModal = () => {
    shiftDialog.value = false
    setTimeout(() => {
        editedShift.value = { ...defaultShift }
    }, 300)
}

const saveShift = () => {
    const selectedRole = roleStore.roles.find(r => r.id === editedShift.value.roleId)
    const selectedEmployee = employeeStore.employees.find(e => e.id === editedShift.value.employeeId)

    const shiftData = {
        ...editedShift.value,
        roleName: selectedRole ? selectedRole.name : 'Inconnu',
        employeeName: selectedEmployee ? `${selectedEmployee.firstName} ${selectedEmployee.lastName}` : null
    }

    if (isEditing.value && editedShiftId.value) {
        scheduleStore.updateShift(editedShiftId.value, shiftData)
        showNotification('Shift modifié avec succès')
    } else {
        scheduleStore.addShift(shiftData)
        showNotification('Nouveau shift ajouté')
    }
    closeShiftModal()
}

const executeDelete = () => {
    if (editedShiftId.value) {
        scheduleStore.deleteShift(editedShiftId.value)
        showNotification('Shift supprimé', 'error')
    }
    deleteConfirmDialog.value = false
    closeShiftModal()
}

const getRoleColor = (role) => {
    const colors = {
        'Manager': '#4F46E5',
        'Chef de rang': '#0D9488',
        'Serveur': '#6366F1',
        'Cuisinier': '#F59E0B',
        'Plongeur': '#64748B'
    }
    return colors[role] || '#94A3B8'
}
</script>

<style scoped>
.cursor-pointer {
    cursor: pointer;
}

.gap-1 {
    gap: 0.25rem;
}

.gap-3 {
    gap: 0.75rem;
}

.gap-4 {
    gap: 1rem;
}

.shift-card-horizontal {
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #E2E8F0 !important;
}

.shift-card-horizontal:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}

.time-block {
    min-width: 80px;
}

.custom-scrollbar::-webkit-scrollbar {
    height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
    margin: 0 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}

.day-column {
    min-width: 240px;
    width: calc(100% / 7);
}

.shift-card {
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid #E2E8F0 !important;
}

.shift-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025) !important;
}

.month-grid-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    border-bottom: 1px solid #E2E8F0;
}

.month-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-auto-rows: minmax(80px, auto);
    background-color: #E2E8F0;
    gap: 1px;
}

.month-cell {
    background-color: #FFFFFF;
    transition: background-color 0.2s;
    cursor: pointer;
}

.month-cell:hover {
    background-color: #F8FAFC !important;
}

.border-dashed {
    border: 2px dashed #CBD5E1 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}

.border-dashed:hover {
    background-color: #F8FAFC !important;
    border-color: #94A3B8 !important;
}

.unassigned-border {
    border-left: 4px solid #E11D48 !important;
}

.text-xs {
    font-size: 0.75rem;
}

.text-micro {
    font-size: 0.65rem;
    line-height: 1.1;
}

@media (max-width: 600px) {
    .day-column {
        min-width: 220px;
    }
}
</style>