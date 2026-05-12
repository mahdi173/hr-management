<template>
    <div class="absences-view">
        <div class="d-flex flex-column flex-lg-row justify-space-between align-lg-center mb-6 mt-2">
            <div class="mb-4 mb-lg-0">
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Absences</h1>
                <p class="text-body-1 text-grey-darken-1">Gérez les demandes de congés et indisponibilités.</p>
            </div>

            <div class="d-flex flex-column flex-sm-row align-stretch align-sm-center gap-3 w-100"
                style="max-width: 600px;">
                <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" placeholder="Rechercher une demande..."
                    variant="outlined" density="compact" hide-details bg-color="white" rounded="lg"
                    class="flex-grow-1"></v-text-field>

                <v-btn color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus" height="40"
                    class="px-5 font-weight-bold flex-shrink-0" @click="openNewModal">
                    Nouvelle Demande
                </v-btn>
            </div>
        </div>

        <v-card border elevation="0" rounded="xl" class="overflow-hidden bg-white mb-6">
            <v-tabs v-model="tab" color="primary" class="border-bottom px-4 pt-2">
                <v-tab value="pending" class="font-weight-bold text-none">En attente ({{
                    absenceStore.pendingAbsences.length }})</v-tab>
                <v-tab value="history" class="font-weight-bold text-none">Historique complet</v-tab>
            </v-tabs>

            <v-data-table :headers="headers" :items="displayedAbsences" :search="search"
                :loading="absenceStore.isLoading" hover class="cursor-pointer" @click:row="handleRowClick">

                <template v-slot:item.employeeName="{ item }">
                    <div class="d-flex align-center py-3">
                        <v-avatar color="primary-lighten-4" size="40" rounded="lg"
                            class="mr-4 font-weight-bold text-primary">
                            {{ item.employeeName.charAt(0) }}
                        </v-avatar>
                        <div class="font-weight-bold text-body-1">{{ item.employeeName }}</div>
                    </div>
                </template>

                <template v-slot:item.dates="{ item }">
                    <div class="text-body-2 text-no-wrap">
                        <v-icon size="small" class="mr-1 text-grey-darken-1">mdi-calendar-start</v-icon> {{
                        formatDate(item.startDate) }}
                    </div>
                    <div class="text-body-2 mt-1 text-no-wrap">
                        <v-icon size="small" class="mr-1 text-grey-darken-1">mdi-calendar-end</v-icon> {{
                        formatDate(item.endDate) }}
                    </div>
                </template>

                <template v-slot:item.status="{ item }">
                    <v-chip :color="getStatusColor(item.status)" size="small" variant="tonal"
                        class="font-weight-bold px-3">
                        {{ item.status }}
                    </v-chip>
                </template>

                <template v-slot:item.actions="{ item }">
                    <div class="d-flex justify-end pr-2" v-if="item.status === 'En attente'">
                        <v-btn icon="mdi-check" variant="tonal" size="small" color="success" class="mr-2"
                            @click.stop="updateStatus(item, 'Approuvé')"></v-btn>
                        <v-btn icon="mdi-close" variant="tonal" size="small" color="error"
                            @click.stop="updateStatus(item, 'Refusé')"></v-btn>
                    </div>
                </template>
            </v-data-table>
        </v-card>

        <v-dialog v-model="dialog" max-width="500" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    Déclarer une absence
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="closeModal"></v-btn>
                </v-card-title>

                <v-card-text class="px-6 pt-4">
                    <v-row>
                        <v-col cols="12" class="pb-1">
                            <v-select v-model="newItem.employeeId" label="Employé" :items="employeeStore.employees"
                                item-title="firstName" item-value="id" variant="outlined" density="comfortable"
                                color="primary"></v-select>
                        </v-col>
                        <v-col cols="12" class="py-1">
                            <v-select v-model="newItem.type" label="Type d'absence"
                                :items="['Congé payé', 'Maladie', 'Congé sans solde', 'Autre']" variant="outlined"
                                density="comfortable" color="primary"></v-select>
                        </v-col>
                        <v-col cols="12" md="6" class="py-1">
                            <v-text-field v-model="newItem.startDate" label="Date de début" type="date"
                                variant="outlined" density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" class="py-1">
                            <v-text-field v-model="newItem.endDate" label="Date de fin" type="date" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" class="pt-1">
                            <v-textarea v-model="newItem.reason" label="Motif / Commentaire" variant="outlined" rows="3"
                                density="comfortable" color="primary"></v-textarea>
                        </v-col>
                    </v-row>
                </v-card-text>

                <v-divider class="mt-2"></v-divider>

                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="closeModal">Annuler</v-btn>
                    <v-btn variant="flat" color="primary" rounded="lg" class="px-6 font-weight-bold"
                        @click="saveItem">Soumettre</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDetails" max-width="500">
            <v-card rounded="xl" elevation="0" border v-if="selectedAbsence">
                <v-card-title
                    class="px-6 pt-6 pb-4 font-weight-bold d-flex justify-space-between align-center text-h6 border-bottom">
                    Détails de l'absence
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="dialogDetails = false"></v-btn>
                </v-card-title>

                <v-card-text class="px-6 py-6">
                    <div class="d-flex align-center mb-6">
                        <v-avatar color="primary-lighten-4" size="56" rounded="lg"
                            class="mr-4 font-weight-bold text-primary text-h6">
                            {{ selectedAbsence.employeeName.charAt(0) }}
                        </v-avatar>
                        <div>
                            <div class="text-h6 font-weight-bold">{{ selectedAbsence.employeeName }}</div>
                            <v-chip :color="getStatusColor(selectedAbsence.status)" size="small" variant="tonal"
                                class="font-weight-bold mt-1">
                                {{ selectedAbsence.status }}
                            </v-chip>
                        </div>
                    </div>

                    <v-row>
                        <v-col cols="12" sm="6" class="pb-2">
                            <div class="text-caption text-grey-darken-1 mb-1 font-weight-bold text-uppercase">Type
                                d'absence
                            </div>
                            <div class="font-weight-medium text-body-1">{{ selectedAbsence.type }}</div>
                        </v-col>
                        <v-col cols="12" sm="6" class="pb-2">
                            <div class="text-caption text-grey-darken-1 mb-1 font-weight-bold text-uppercase">Période
                            </div>
                            <div class="font-weight-medium text-body-2">
                                Du {{ formatDate(selectedAbsence.startDate) }}<br>Au {{
                                    formatDate(selectedAbsence.endDate) }}
                            </div>
                        </v-col>
                        <v-col cols="12" class="pt-2" v-if="selectedAbsence.reason">
                            <div class="text-caption text-grey-darken-1 mb-1 font-weight-bold text-uppercase">Motif
                            </div>
                            <v-sheet color="grey-lighten-4" rounded="lg" class="pa-4 text-body-2 text-grey-darken-3">
                                {{ selectedAbsence.reason }}
                            </v-sheet>
                        </v-col>
                    </v-row>
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
import { useAbsenceStore } from '../stores/absenceStore'
import { useEmployeeStore } from '../stores/employeeStore'

const absenceStore = useAbsenceStore()
const employeeStore = useEmployeeStore()

const search = ref('')
const tab = ref('pending')
const dialog = ref(false)
const dialogDetails = ref(false)
const selectedAbsence = ref(null)

const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })

const defaultItem = {
    employeeId: null,
    type: 'Congé payé',
    startDate: '',
    endDate: '',
    reason: ''
}
const newItem = ref({ ...defaultItem })

const headers = [
    { title: 'Collaborateur', key: 'employeeName', align: 'start', sortable: true },
    { title: 'Type', key: 'type', align: 'start' },
    { title: 'Dates', key: 'dates', align: 'start', sortable: false },
    { title: 'Statut', key: 'status', align: 'center' },
    { title: 'Actions', key: 'actions', align: 'end', sortable: false },
]

const displayedAbsences = computed(() => {
    if (tab.value === 'pending') {
        return absenceStore.pendingAbsences
    }
    return absenceStore.allAbsences
})

const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

const getStatusColor = (status) => {
    if (status === 'Approuvé') return 'success'
    if (status === 'Refusé') return 'error'
    return 'warning'
}

const showNotification = (text, type = 'success') => {
    snackbar.value = {
        show: true,
        text,
        color: type,
        icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
    }
}

const openNewModal = () => {
    newItem.value = { ...defaultItem }
    dialog.value = true
}

const closeModal = () => {
    dialog.value = false
    setTimeout(() => {
        newItem.value = { ...defaultItem }
    }, 300)
}

const saveItem = async () => {
    const emp = employeeStore.employees.find(e => e.id === newItem.value.employeeId)
    const absenceData = {
        ...newItem.value,
        employeeName: emp ? `${emp.firstName} ${emp.lastName}` : 'Inconnu'
    }
    await absenceStore.addAbsence(absenceData)
    showNotification('Demande d\'absence soumise avec succès')
    closeModal()
}

const updateStatus = async (item, status) => {
    await absenceStore.updateAbsenceStatus(item.id, status)
    showNotification(`Absence ${status.toLowerCase()}`, status === 'Approuvé' ? 'success' : 'error')
}

const handleRowClick = (event, { item }) => {
    selectedAbsence.value = item
    dialogDetails.value = true
}

onMounted(async () => {
    if (absenceStore.absences.length === 0) await absenceStore.fetchAbsences()
    if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()
})
</script>

<style scoped>
.gap-3 {
    gap: 0.75rem;
}

.border-bottom {
    border-bottom: 1px solid #E2E8F0;
}

.cursor-pointer {
    cursor: pointer;
}

.text-no-wrap {
    white-space: nowrap;
}

:deep(.v-data-table-header__content) {
    font-weight: 700;
    color: #64748B;
}

:deep(.v-data-table__tr:hover) {
    background-color: #F8FAFC !important;
}
</style>