<template>
    <div class="plannings-view">
        <div class="d-flex flex-column flex-lg-row justify-space-between align-lg-center mb-6 mt-2">
            <div class="mb-4 mb-lg-0">
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Plannings</h1>
                <p class="text-body-1 text-grey-darken-1">Consultez les services et l'assignation de l'équipe.</p>
            </div>

            <div class="d-flex flex-column flex-sm-row align-stretch align-sm-center gap-4">
                <v-btn v-if="authStore.isManager && currentSchedule" color="secondary" variant="tonal" rounded="lg"
                    prepend-icon="mdi-brain" @click="analyzeSchedule" :loading="managementStore.isLoading">
                    Analyse IA
                </v-btn>

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

        <div v-if="!currentSchedule" class="text-center py-16 bg-white rounded-xl border mt-6">
            <v-avatar color="primary-lighten-5" size="80" class="mb-4">
                <v-icon color="primary" size="40">mdi-calendar-plus</v-icon>
            </v-avatar>
            <h2 class="text-h5 font-weight-bold mb-2">Aucun planning pour cette période</h2>
            <p class="text-grey-darken-1 mb-6">La semaine n'a pas encore été initialisée.</p>
            <v-btn v-if="authStore.isManager" color="primary" variant="flat" rounded="lg" size="large"
                prepend-icon="mdi-plus" @click="createNewSchedule" :loading="scheduleStore.isLoading">
                Créer le planning de la semaine
            </v-btn>
        </div>

        <div v-else>
            <div v-if="currentView === 'day'" class="day-view">
                <v-card border elevation="0" rounded="xl" class="pa-4 pa-md-6 bg-white">
                    <div class="d-flex flex-column flex-sm-row justify-space-between align-sm-center mb-6 gap-3">
                        <h2 class="text-h6 font-weight-bold">{{ getFullDateLabel(baseDate) }}</h2>
                        <v-btn v-if="authStore.isManager" color="primary" variant="flat" rounded="lg"
                            prepend-icon="mdi-plus" @click="openNewShiftModal(baseDateStr)">
                            Ajouter un shift
                        </v-btn>
                    </div>

                    <div v-if="shiftsForDay(baseDateStr).length === 0"
                        class="text-center py-10 bg-grey-lighten-4 rounded-lg border-dashed">
                        <v-icon color="grey" size="48" class="mb-2">mdi-calendar-blank</v-icon>
                        <p class="text-grey-darken-1 font-weight-medium">Aucun shift planifié pour cette journée.</p>
                    </div>

                    <v-list v-else class="bg-transparent" lines="two">
                        <v-card v-for="shift in shiftsForDay(baseDateStr)" :key="shift.id" border elevation="0"
                            rounded="lg"
                            class="mb-3 px-4 py-3 d-flex flex-column flex-sm-row align-sm-center justify-space-between shift-card-horizontal"
                            :class="{ 'unassigned-border': !shift.employeeId, 'cursor-pointer': authStore.isManager }"
                            :style="`border-left: 4px solid ${!shift.employeeId ? '#E11D48' : getRoleColor(shift.roleName)} !important;`"
                            @click="authStore.isManager ? editExistingShift(shift) : null">

                            <div class="d-flex align-center mb-3 mb-sm-0">
                                <div class="time-block mr-4 mr-sm-6 text-center">
                                    <div class="text-subtitle-1 text-sm-h6 font-weight-bold">{{ shift.startTime }}</div>
                                    <div class="text-caption text-grey-darken-1">{{ shift.endTime }}</div>
                                </div>
                                <v-avatar :color="!shift.employeeId ? 'error-lighten-4' : 'grey-lighten-3'" size="40"
                                    class="mr-3 mr-sm-4 rounded-lg">
                                    <span v-if="shift.employeeId" class="font-weight-bold">{{
                                        shift.employeeName?.charAt(0) || '?' }}</span>
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
                                class="font-weight-bold align-self-start align-self-sm-center">{{ shift.status
                                }}</v-chip>
                        </v-card>
                    </v-list>
                </v-card>
            </div>

            <div v-else-if="currentView === 'week'" class="week-view">
                <div class="d-flex flex-nowrap gap-4 overflow-x-auto custom-scrollbar pb-6 pt-2"
                    style="min-height: 60vh;">
                    <div v-for="day in weekDays" :key="day.date" class="day-column d-flex flex-column">
                        <div class="day-header text-center py-2 py-sm-3 mb-3 rounded-lg border bg-white flex-shrink-0"
                            :class="{ 'border-primary bg-primary-lighten-5': day.isToday }">
                            <div class="text-uppercase text-caption font-weight-bold text-grey-darken-1 mb-1">{{
                                day.dayName }}</div>
                            <div class="text-h6 font-weight-bold" :class="{ 'text-primary': day.isToday }">{{
                                day.dayNumber }}</div>
                        </div>

                        <div class="shifts-container d-flex flex-column flex-grow-1">
                            <div class="flex-grow-1 mb-2">
                                <v-card v-for="shift in shiftsForDay(day.date)" :key="shift.id" border elevation="0"
                                    rounded="lg" class="mb-3 shift-card pa-3 pa-sm-4 bg-white"
                                    :class="{ 'cursor-pointer': authStore.isManager }"
                                    :style="`border-left: 4px solid ${!shift.employeeId ? '#E11D48' : getRoleColor(shift.roleName)} !important;`"
                                    @click.stop="authStore.isManager ? editExistingShift(shift) : null">
                                    <div class="d-flex justify-space-between align-start mb-2 mb-sm-3">
                                        <span class="font-weight-bold text-body-2 text-sm-body-1">{{ shift.startTime }}
                                            - {{ shift.endTime }}</span>
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

                            <v-btn v-if="authStore.isManager" variant="outlined" color="grey-darken-1"
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
                            @click="authStore.isManager ? openNewShiftModal(cell.date) : null">

                            <div class="d-flex justify-space-between align-start mb-1 mb-sm-2">
                                <span class="text-xs text-sm-caption font-weight-bold"
                                    :class="{ 'text-primary': cell.isToday }">{{ cell.dayNumber }}</span>
                                <v-icon v-if="shiftsForDay(cell.date).some(s => !s.employeeId)" color="error"
                                    size="x-small" class="d-none d-sm-flex">mdi-circle</v-icon>
                            </div>

                            <div class="d-flex flex-column gap-1">
                                <div v-for="shift in shiftsForDay(cell.date).slice(0, 3)" :key="shift.id"
                                    class="text-truncate px-1 px-sm-2 rounded-sm text-micro text-sm-xs font-weight-medium"
                                    :class="{ 'cursor-pointer': authStore.isManager }"
                                    :style="`background-color: ${!shift.employeeId ? '#FFE4E6' : '#F1F5F9'}; color: ${!shift.employeeId ? '#E11D48' : '#334155'}; padding: 2px 4px;`"
                                    @click.stop="authStore.isManager ? editExistingShift(shift) : null">
                                    <span class="d-none d-sm-inline">{{ shift.startTime }}</span>
                                    {{ shift.employeeName ? shift.employeeName.split(' ')[0] : 'Vide' }}
                                </div>
                                <div v-if="shiftsForDay(cell.date).length > 3"
                                    class="text-micro text-grey-darken-1 pl-1 mt-1">
                                    +{{ shiftsForDay(cell.date).length - 3 }} <span
                                        class="d-none d-sm-inline">autres</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </v-card>
            </div>
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

                        <v-col cols="12" class="pt-0"
                            v-if="isEditing && !editedShift.employeeId && authStore.isManager">
                            <div class="d-flex align-center mb-2">
                                <v-icon color="secondary" size="small" class="mr-2">mdi-auto-fix</v-icon>
                                <span class="text-subtitle-2 font-weight-bold text-secondary">Suggestions IA</span>
                                <v-spacer></v-spacer>
                                <v-progress-circular v-if="managementStore.isRecommending" indeterminate size="16"
                                    width="2" color="secondary"></v-progress-circular>
                            </div>

                            <v-card v-if="managementStore.shiftRecommendations?.recommendations?.length > 0" border
                                elevation="0" rounded="lg" class="bg-blue-lighten-5 pa-2">
                                <v-list class="bg-transparent pa-0" lines="two">
                                    <v-list-item
                                        v-for="rec in managementStore.shiftRecommendations.recommendations.slice(0, 3)"
                                        :key="rec.employee_id" class="px-3 py-2 mb-1 rounded bg-white" border>
                                        <template v-slot:prepend>
                                            <v-avatar color="primary-lighten-4" size="32" class="mr-3">
                                                <span class="text-caption font-weight-bold text-primary">{{
                                                    rec.employee_name?.charAt(0) || '?' }}</span>
                                            </v-avatar>
                                        </template>
                                        <v-list-item-title class="text-body-2 font-weight-bold">{{ rec.employee_name
                                            }}</v-list-item-title>
                                        <v-list-item-subtitle class="text-caption text-grey-darken-1">
                                            Score: {{ Math.round(rec.score * 100) }}% - {{ rec.explanation }}
                                        </v-list-item-subtitle>
                                        <template v-slot:append>
                                            <v-btn size="small" color="secondary" variant="tonal" rounded="lg"
                                                class="font-weight-bold px-4"
                                                @click="assignRecommended(rec.employee_id)">
                                                Assigner
                                            </v-btn>
                                        </template>
                                    </v-list-item>
                                </v-list>
                            </v-card>
                            <div v-else-if="!managementStore.isRecommending && managementStore.shiftRecommendations && managementStore.shiftRecommendations.recommendations.length === 0"
                                class="text-caption text-grey-darken-1 text-center py-2">
                                Aucun employé idéal trouvé pour ce shift.
                            </div>
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
                        @click="executeDelete">Oui,
                        supprimer</v-btn>
                </div>
            </v-card>
        </v-dialog>

        <v-dialog v-model="aiAnalysisDialog" max-width="600">
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-4 font-weight-bold text-h6 d-flex justify-space-between align-center">
                    <span><v-icon color="secondary" class="mr-2">mdi-auto-fix</v-icon> Rapport d'Optimisation</span>
                    <v-btn icon="mdi-close" variant="text" @click="aiAnalysisDialog = false"></v-btn>
                </v-card-title>
                <v-card-text class="px-6 pb-6 bg-grey-lighten-4">
                    <div v-if="managementStore.optimizationOpportunities.length === 0"
                        class="text-center py-4 text-success">
                        <v-icon size="40" class="mb-2">mdi-check-decagram</v-icon>
                        <h3>Planning optimal !</h3>
                        <p>Le staffing correspond parfaitement à l'historique d'activité.</p>
                    </div>

                    <v-card v-for="(opp, idx) in managementStore.optimizationOpportunities" :key="idx" class="mb-3 pa-4"
                        border elevation="0" rounded="lg">
                        <div class="d-flex align-center">
                            <v-avatar :color="opp.type === 'understaffing' ? 'error-lighten-4' : 'warning-lighten-4'"
                                size="40" class="mr-3">
                                <v-icon :color="opp.type === 'understaffing' ? 'error' : 'warning'">
                                    {{ opp.type === 'understaffing' ? 'mdi-account-plus' : 'mdi-account-minus' }}
                                </v-icon>
                            </v-avatar>
                            <div>
                                <h4 class="font-weight-bold">{{ opp.shift_date }} à {{ opp.shift_time }}</h4>
                                <p class="text-body-2 text-grey-darken-2">{{ opp.suggestion }}</p>
                                <v-chip size="x-small" class="mt-1 font-weight-bold"
                                    :color="opp.impact === 'high' ? 'error' : 'warning'">
                                    Impact: {{ opp.impact }}
                                </v-chip>
                            </div>
                        </div>
                    </v-card>
                </v-card-text>
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
import { ref, computed, onMounted } from 'vue'
import { useScheduleStore } from '../stores/scheduleStore'
import { useEmployeeStore } from '../stores/employeeStore'
import { useRoleStore } from '../stores/roleStore'
import { useAuthStore } from '../stores/authStore'
import { useManagementStore } from '../stores/managementStore'

const managementStore = useManagementStore()

const scheduleStore = useScheduleStore()
const employeeStore = useEmployeeStore()
const roleStore = useRoleStore()
const authStore = useAuthStore()

const currentView = ref('week')
const baseDate = ref(new Date())
const baseDateStr = computed(() => {
    const d = baseDate.value
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})

const deleteConfirmDialog = ref(false)
const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })

const showNotification = (text, type = 'success') => {
    snackbar.value = { show: true, text, color: type, icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }
}

const navigate = (direction) => {
    const newDate = new Date(baseDate.value)
    if (currentView.value === 'day') newDate.setDate(newDate.getDate() + direction)
    else if (currentView.value === 'week') newDate.setDate(newDate.getDate() + (direction * 7))
    else if (currentView.value === 'month') newDate.setMonth(newDate.getMonth() + direction)
    baseDate.value = newDate
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

        const dateString = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`

        const today = new Date()
        const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

        days.push({
            date: dateString,
            dayName: dayNames[currentDate.getDay()],
            dayNumber: currentDate.getDate(),
            isToday: dateString === todayStr
        })
    }
    return days
})

const currentSchedule = computed(() => {
    const dateToCheck = baseDateStr.value
    return scheduleStore.schedules.find(s => dateToCheck >= s.start_date && dateToCheck <= s.end_date)
})

const createNewSchedule = async () => {
    if (weekDays.value.length === 0) return
    const start = weekDays.value[0].date
    const end = weekDays.value[6].date
    const dateObj = new Date(start)
    const name = `Semaine du ${dateObj.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })}`

    try {
        await scheduleStore.createSchedule({
            name: name,
            start_date: start,
            end_date: end,
            created_by_id: authStore.user?.id || 1
        })
        showNotification('Planning créé avec succès !')
    } catch (error) {
        showNotification('Erreur lors de la création du planning', 'error')
    }
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

const monthCells = computed(() => {
    const cells = []
    const year = baseDate.value.getFullYear()
    const month = baseDate.value.getMonth()
    const firstDayOfMonth = new Date(year, month, 1)
    let startDayOfWeek = firstDayOfMonth.getDay()
    if (startDayOfWeek === 0) startDayOfWeek = 7
    const startDate = new Date(year, month, 1 - (startDayOfWeek - 1))

    const today = new Date()
    const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

    for (let i = 0; i < 42; i++) {
        const d = new Date(startDate)
        d.setDate(startDate.getDate() + i)
        const dateString = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

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
    startTime: '09:00',
    endTime: '17:00',
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

const editExistingShift = async (shift) => {
    isEditing.value = true
    editedShiftId.value = shift.id
    editedShift.value = { ...shift }
    shiftDialog.value = true

    if (!shift.employeeId && authStore.isManager) {
        await managementStore.fetchShiftRecommendations(shift.id)
    } else {
        managementStore.shiftRecommendations = null;
    }
}

const assignRecommended = (employeeId) => {
    editedShift.value.employeeId = employeeId;
    saveShift();
}

const closeShiftModal = () => {
    shiftDialog.value = false
    setTimeout(() => {
        editedShift.value = { ...defaultShift }
    }, 300)
}

const saveShift = async () => {
    const selectedRole = roleStore.roles.find(r => r.id === editedShift.value.roleId)
    const selectedEmployee = employeeStore.employees.find(e => e.id === editedShift.value.employeeId)

    const shiftData = {
        ...editedShift.value,
        roleName: selectedRole ? selectedRole.name : 'Inconnu',
        employeeName: selectedEmployee ? `${selectedEmployee.firstName} ${selectedEmployee.lastName}` : null
    }

    try {
        if (isEditing.value && editedShiftId.value) {
            await scheduleStore.updateShift(editedShiftId.value, shiftData)
            showNotification('Shift modifié avec succès')
        } else {
            await scheduleStore.addShift(shiftData)
            showNotification('Nouveau shift ajouté')
        }
        closeShiftModal()
    } catch (err) {
        showNotification("Erreur lors de l'enregistrement du shift", 'error')
    }
}

const executeDelete = async () => {
    if (editedShiftId.value) {
        try {
            await scheduleStore.deleteShift(editedShiftId.value)
            showNotification('Shift supprimé', 'error')
        } catch (err) {
            showNotification('Erreur lors de la suppression', 'error')
        }
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

const aiAnalysisDialog = ref(false);

const analyzeSchedule = async () => {
    if (currentSchedule.value) {
        await managementStore.fetchOptimizationOpportunities(currentSchedule.value.id);
        aiAnalysisDialog.value = true;
    }
}

onMounted(async () => {
    if (!authStore.user) await authStore.fetchCurrentUser()
    if (roleStore.roles.length === 0) await roleStore.fetchRoles()

    await scheduleStore.fetchSchedules()

    if (authStore.isManager) {
        if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()
        await scheduleStore.fetchWeeklyShifts()
    } else {
        await scheduleStore.fetchMyShifts()
    }
})
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