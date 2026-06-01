<template>
    <div class="dashboard">
        <div class="d-flex justify-space-between align-center mb-8 mt-2">
            <div>
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">
                    Bonjour, {{ authStore.user?.first_name || 'Utilisateur' }}
                </h1>
                <p class="text-body-1 text-grey-darken-1">
                    {{ authStore.isManager ? "Voici l'état de votre équipe pour aujourd'hui." : "Voici votre récapitulatif personnel." }}
                </p>
            </div>
            <v-btn v-if="authStore.isManager" color="primary" variant="flat" rounded="lg" size="large"
                prepend-icon="mdi-plus" class="px-6" to="/plannings">
                Nouveau Planning
            </v-btn>
            <v-btn v-else color="primary" variant="flat" rounded="lg" size="large" prepend-icon="mdi-calendar-check"
                class="px-6" to="/plannings">
                Mon Planning
            </v-btn>
        </div>

        <v-row class="mb-6" v-if="authStore.isManager">
            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Shifts non assignés</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">{{ unassignedShiftsCount }}</h2>
                        </div>
                        <v-avatar color="#FEF2F2" rounded="lg" size="48">
                            <v-icon color="error">mdi-alert-circle-outline</v-icon>
                        </v-avatar>
                    </div>
                </v-card>
            </v-col>
            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Absences en attente</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">{{ pendingAbsencesCount }}</h2>
                        </div>
                        <v-avatar color="#FFFBEB" rounded="lg" size="48">
                            <v-icon color="warning">mdi-palm-tree</v-icon>
                        </v-avatar>
                    </div>
                </v-card>
            </v-col>
            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Complétion Planning</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">{{ completionRate }}%</h2>
                        </div>
                        <v-avatar color="#ECFDF5" rounded="lg" size="48">
                            <v-icon color="success">mdi-check-circle-outline</v-icon>
                        </v-avatar>
                    </div>
                    <v-progress-linear :model-value="completionRate" color="success" height="8" rounded
                        class="mt-5"></v-progress-linear>
                </v-card>
            </v-col>
        </v-row>

        <v-row class="mb-6" v-else>
            <v-col cols="12" md="6">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card bg-primary text-white">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-white font-weight-medium mb-2 opacity-80">Mes heures cette
                                semaine</p>
                            <h2 class="text-h3 font-weight-bold text-white">{{ employeeWeeklyHours }}h</h2>
                        </div>
                        <v-avatar color="rgba(255,255,255,0.2)" rounded="lg" size="48">
                            <v-icon color="white">mdi-clock-outline</v-icon>
                        </v-avatar>
                    </div>
                </v-card>
            </v-col>
            <v-col cols="12" md="6">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card" @click="router.push('/absences')">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Mes demandes d'absence</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">{{ myAbsencesCount }}</h2>
                        </div>
                        <v-avatar color="#FFFBEB" rounded="lg" size="48">
                            <v-icon color="warning">mdi-palm-tree</v-icon>
                        </v-avatar>
                    </div>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" :md="authStore.isManager ? 8 : 12">
                <v-card border elevation="0" rounded="xl" class="fill-height pb-4">
                    <v-card-title class="px-6 pt-6 pb-4 d-flex justify-space-between align-center">
                        <span class="text-h6 font-weight-bold">{{ authStore.isManager ? 'Service du jour' : 'Mes prochains shifts' }}</span>
                        <v-btn variant="text" color="primary" size="small" class="font-weight-bold" to="/plannings">Voir
                            tout</v-btn>
                    </v-card-title>
                    <v-divider class="mb-4"></v-divider>

                    <div v-if="displayedShifts.length === 0" class="text-center py-6">
                        <p class="text-grey-darken-1">Aucun shift prévu.</p>
                    </div>

                    <v-list v-else lines="two" class="px-4">
                        <v-list-item v-for="shift in displayedShifts" :key="shift.id"
                            class="mb-3 rounded-lg shift-item">
                            <template v-slot:prepend>
                                <v-avatar :color="shift.employeeId ? getRoleColor(shift.roleName) : 'error'" size="48"
                                    rounded="lg" class="mr-4 font-weight-bold text-white">
                                    {{ shift.employeeName ? shift.employeeName.charAt(0) : '?' }}
                                </v-avatar>
                            </template>
                            <v-list-item-title class="font-weight-bold text-body-1"
                                :class="{ 'text-error': !shift.employeeId }">
                                {{ authStore.isManager ? (shift.employeeName || 'Non assigné') : shift.date }}
                            </v-list-item-title>
                            <v-list-item-subtitle class="text-grey-darken-1 mt-1">
                                <v-icon size="small" class="mr-1">mdi-clock-outline</v-icon>
                                {{ shift.startTime }} - {{ shift.endTime }} • {{ shift.roleName }}
                            </v-list-item-subtitle>
                            <template v-slot:append>
                                <v-chip size="small" :color="getStatusColor(shift.status)" variant="tonal"
                                    class="font-weight-bold px-3">
                                    {{ shift.status }}
                                </v-chip>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>

            <v-col cols="12" md="4" v-if="authStore.isManager">
                <v-card border elevation="0" rounded="xl" class="fill-height" bg-color="#F4F6FF">
                    <v-card-title class="px-6 pt-6 pb-3">
                        <span class="text-h6 font-weight-bold text-primary d-flex align-center">
                            <v-icon class="mr-2">mdi-creation</v-icon> Insights IA
                        </span>
                    </v-card-title>
                    <v-card-text class="px-6">
                        <v-card border elevation="0" rounded="xl" class="mb-4 pa-5 insight-card" color="white">
                            <div class="d-flex align-start">
                                <v-avatar color="#FFFBEB" size="40" rounded="lg" class="mr-4 mt-1"><v-icon
                                        color="warning" size="small">mdi-account-alert</v-icon></v-avatar>
                                <div>
                                    <h4 class="text-subtitle-1 font-weight-bold mb-1">Risque de surcharge</h4>
                                    <p class="text-body-2 text-grey-darken-1 mb-3 lh-sm">Vérifiez vos équipes.</p>
                                </div>
                            </div>
                        </v-card>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useScheduleStore } from '../stores/scheduleStore'
import { useAbsenceStore } from '../stores/absenceStore'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const scheduleStore = useScheduleStore()
const absenceStore = useAbsenceStore()
const authStore = useAuthStore()

const today = new Date()
const year = today.getFullYear()
const month = String(today.getMonth() + 1).padStart(2, '0')
const day = String(today.getDate()).padStart(2, '0')
const todayStr = `${year}-${month}-${day}`

const unassignedShiftsCount = computed(() => scheduleStore.shifts.filter(s => !s.employeeId).length)
const pendingAbsencesCount = computed(() => absenceStore.pendingAbsences.length)
const completionRate = computed(() => {
    const total = scheduleStore.shifts.length
    if (total === 0) return 100
    const assigned = scheduleStore.shifts.filter(s => s.employeeId).length
    return Math.round((assigned / total) * 100)
})

const employeeWeeklyHours = computed(() => {
    if (!authStore.user?.employee_id) return 0;
    return scheduleStore.shifts.filter(s => s.employeeId === authStore.user.employee_id).length * 8;
})

const myAbsencesCount = computed(() => {
    if (!authStore.user?.employee_id) return 0;
    return absenceStore.absences.filter(a => a.employeeId === authStore.user.employee_id).length;
})

const displayedShifts = computed(() => {
    if (authStore.isManager) {
        return scheduleStore.getShiftsByDate(todayStr) || []
    } else {
        return scheduleStore.shifts.filter(s => s.employeeId === authStore.user?.employee_id).slice(0, 5)
    }
})

const getRoleColor = (role) => {
    const colors = { 'Manager': '#4F46E5', 'Chef de rang': '#0D9488', 'Serveur': '#6366F1', 'Cuisinier': '#F59E0B' }
    return colors[role] || '#94A3B8'
}
const getStatusColor = (status) => {
    if (status === 'Confirmé' || status === 'Approuvé') return 'success'
    if (status === 'En attente') return 'warning'
    return 'error'
}

onMounted(async () => {
    if (!authStore.user) {
        await authStore.fetchCurrentUser()
    }
    
    await Promise.all([
        scheduleStore.fetchWeeklyShifts(),
        absenceStore.fetchAbsences()
    ])
})
</script>

<style scoped>
.hover-card {
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}

.hover-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
}

.shift-item {
    transition: background-color 0.2s ease;
}

.shift-item:hover {
    background-color: #F9FAFB;
}

.opacity-80 {
    opacity: 0.8;
}
</style>