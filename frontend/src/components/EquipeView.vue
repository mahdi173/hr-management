<template>
    <div class="equipe-view">
        <div class="d-flex flex-column flex-lg-row justify-space-between align-lg-center mb-6 mt-2">
            <div class="mb-4 mb-lg-0">
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Équipe</h1>
                <p class="text-body-1 text-grey-darken-1">Consultez les collaborateurs et leurs informations.</p>
            </div>
            <div class="mt-4 mt-md-0 d-flex align-center w-100 justify-end" style="max-width: 600px;">
                <v-switch v-if="authStore.isManager" v-model="showInactive" label="Afficher les inactifs"
                    color="primary" hide-details density="compact"
                    class="mr-4 text-body-2 font-weight-medium flex-shrink-0"></v-switch>

                <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" placeholder="Rechercher un membre..."
                    variant="outlined" density="compact" hide-details bg-color="white" rounded="lg"
                    style="min-width: 260px;" class="flex-grow-1 flex-md-grow-0"></v-text-field>

                <v-btn v-if="authStore.isManager" color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus"
                    class="ml-4 px-5 font-weight-bold flex-shrink-0" @click="openNewModal">
                    Ajouter
                </v-btn>
            </div>
        </div>

        <v-card border elevation="0" rounded="xl" class="overflow-hidden">
            <v-data-table :headers="headers" :items="displayedEmployees" :search="search"
                :loading="employeeStore.isLoading" hover class="bg-white">

                <template v-slot:item.name="{ item }">
                    <div class="d-flex align-center py-3">
                        <v-avatar color="primary-lighten-4" size="40" rounded="lg"
                            class="mr-4 font-weight-bold text-primary">
                            {{ (item.firstName?.charAt(0) || '') }}{{ (item.lastName?.charAt(0) || '') }}
                        </v-avatar>
                        <div>
                            <div class="font-weight-bold text-body-1">{{ item.firstName }} {{ item.lastName }}</div>
                            <div class="text-caption text-grey-darken-1">{{ item.email }}</div>
                        </div>
                    </div>
                </template>

                <template v-slot:item.role="{ item }">
                    {{ roleStore.getRoleNameById(item.role_id) }}
                </template>

                <template v-slot:item.contract="{ item }">
                    {{ contractStore.getContractNameById(item.contract_type_id) }}
                </template>

                <template v-slot:item.status="{ item }">
                    <v-chip
                        :color="item.status === 'Actif' ? 'success' : (item.status === 'En congé' ? 'info' : 'warning')"
                        size="small" variant="tonal" class="font-weight-bold px-3">
                        {{ item.status }}
                    </v-chip>
                </template>

                <template v-slot:item.actions="{ item }">
                    <div class="d-flex justify-end pr-2">
                        <v-btn v-if="authStore.isManager" icon="mdi-brain" variant="text" size="small" color="secondary"
                            class="mr-1" title="Profil IA (Préférences)" @click="openAiProfile(item)"></v-btn>

                        <v-btn v-if="authStore.isManager || item.id === authStore.user?.employee_id"
                            icon="mdi-calendar-clock" variant="text" size="small" color="secondary" class="mr-1"
                            title="Gérer les disponibilités" @click="openAvailabilityModal(item)"></v-btn>

                        <v-btn v-if="authStore.isManager" icon="mdi-pencil-outline" variant="text" size="small"
                            color="primary" class="mr-1" @click="editItem(item)"></v-btn>
                        <v-btn v-if="authStore.isManager" icon="mdi-delete-outline" variant="text" size="small"
                            color="error" @click="confirmDelete(item)"></v-btn>
                    </div>
                </template>
            </v-data-table>
        </v-card>

        <v-dialog v-model="dialog" max-width="600" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ formTitle }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="closeModal"></v-btn>
                </v-card-title>

                <v-card-text class="px-6 pt-4">
                    <v-row>
                        <v-col cols="12" md="6" class="pb-1">
                            <v-text-field v-model="editedItem.firstName" label="Prénom" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" class="pb-1">
                            <v-text-field v-model="editedItem.lastName" label="Nom" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" class="py-1">
                            <v-text-field v-model="editedItem.email" label="Email" type="email" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6" class="py-1">
                            <v-text-field v-model="editedItem.phone" label="Téléphone" type="tel" variant="outlined"
                                density="comfortable" color="primary"></v-text-field>
                        </v-col>

                        <v-col cols="12" md="6" class="pt-1">
                            <v-select v-model="editedItem.role_id" label="Rôle" :items="roleStore.roles"
                                item-title="name" item-value="id" variant="outlined" density="comfortable"
                                color="primary"></v-select>
                        </v-col>

                        <v-col cols="12" md="6" class="pt-1">
                            <v-select v-model="editedItem.contract_type_id" label="Type de contrat"
                                :items="contractStore.contracts" item-title="name" item-value="id" variant="outlined"
                                density="comfortable" color="primary"></v-select>
                        </v-col>

                        <v-col cols="12" class="pt-1" v-if="editedIndex > -1">
                            <v-select v-model="editedItem.status" label="Statut"
                                :items="['Actif', 'En congé', 'Inactif']" variant="outlined" density="comfortable"
                                color="primary"></v-select>
                        </v-col>
                    </v-row>
                </v-card-text>

                <v-divider class="mt-2"></v-divider>

                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="closeModal">Annuler</v-btn>
                    <v-btn variant="flat" color="primary" rounded="lg" class="px-6 font-weight-bold"
                        @click="saveItem">Enregistrer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogAvailability" max-width="600">
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    Disponibilités: {{ currentEmployeeName }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="dialogAvailability = false"></v-btn>
                </v-card-title>

                <v-card-text class="px-6 pt-4 bg-grey-lighten-4">
                    <v-card border elevation="0" rounded="lg" class="pa-4 mb-4 bg-white">
                        <h4 class="text-subtitle-2 font-weight-bold mb-3">Ajouter une disponibilité</h4>
                        <v-row>
                            <v-col cols="12" sm="4" class="pb-0">
                                <v-select v-model="newAvailability.dayOfWeek" label="Jour" :items="daysOfWeek"
                                    item-title="name" item-value="value" variant="outlined" density="compact"
                                    hide-details></v-select>
                            </v-col>
                            <v-col cols="6" sm="4" class="pb-0">
                                <v-text-field v-model="newAvailability.startTime" label="De" type="time"
                                    variant="outlined" density="compact" hide-details></v-text-field>
                            </v-col>
                            <v-col cols="6" sm="4" class="pb-0">
                                <v-text-field v-model="newAvailability.endTime" label="À" type="time" variant="outlined"
                                    density="compact" hide-details></v-text-field>
                            </v-col>
                            <v-col cols="12" class="pt-2">
                                <v-btn color="primary" variant="tonal" block @click="saveAvailability"
                                    :loading="availabilityStore.isLoading">
                                    Ajouter cette plage
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card>

                    <h4 class="text-subtitle-2 font-weight-bold mb-2">Plages enregistrées</h4>
                    <div v-if="availabilityStore.availabilities.length === 0"
                        class="text-center py-4 text-grey-darken-1">
                        Aucune disponibilité enregistrée. (Considéré comme toujours disponible)
                    </div>
                    <v-list v-else lines="one" class="bg-transparent pa-0">
                        <v-card v-for="avail in availabilityStore.availabilities" :key="avail.id" border elevation="0"
                            rounded="lg" class="mb-2 px-4 py-2 d-flex align-center justify-space-between bg-white">
                            <div class="d-flex align-center">
                                <v-avatar color="secondary-lighten-4" size="32" class="mr-3 rounded-lg">
                                    <v-icon color="secondary" size="small">mdi-clock-outline</v-icon>
                                </v-avatar>
                                <div>
                                    <div class="font-weight-bold text-body-2">{{ getDayName(avail.dayOfWeek) }}</div>
                                    <div class="text-caption text-grey-darken-1">{{ avail.startTime }} - {{
                                        avail.endTime }}
                                    </div>
                                </div>
                            </div>
                            <v-btn icon="mdi-delete" variant="text" color="error" size="small"
                                @click="deleteAvailability(avail.id)"></v-btn>
                        </v-card>
                    </v-list>
                </v-card-text>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDelete" max-width="450">
            <v-card rounded="xl" elevation="0" border class="pa-4 text-center">
                <v-avatar color="#FEF2F2" size="64" class="mx-auto mt-4 mb-4">
                    <v-icon color="error" size="32">mdi-alert-outline</v-icon>
                </v-avatar>
                <h3 class="text-h6 font-weight-bold mb-2">Supprimer ce collaborateur ?</h3>
                <p class="text-body-2 text-grey-darken-1 mb-6 px-4">
                    Êtes-vous sûr de vouloir supprimer <strong>{{ itemToDelete?.firstName }} {{ itemToDelete?.lastName
                        }}</strong> ? Cette action retirera également cette personne des plannings futurs.
                </p>
                <div class="d-flex justify-center mb-2">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium" rounded="lg"
                        @click="dialogDelete = false">Annuler</v-btn>
                    <v-btn variant="flat" color="error" rounded="lg" class="px-6 font-weight-bold"
                        @click="deleteItemConfirm">Oui, supprimer</v-btn>
                </div>
            </v-card>
        </v-dialog>

        <v-dialog v-model="aiProfileDialog" max-width="500">
            <v-card rounded="xl" border elevation="0" v-if="selectedEmployeeForAi">
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold text-h6">
                    Profil IA: {{ selectedEmployeeForAi.firstName }}
                </v-card-title>
                <v-card-text class="px-6 py-4">
                    <div v-if="!managementStore.employeePreferences[selectedEmployeeForAi.id]">
                        <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </div>
                    <div v-else-if="managementStore.employeePreferences[selectedEmployeeForAi.id].error">
                        <p class="text-error">Pas assez de données historiques pour analyser ce profil.</p>
                    </div>
                    <div v-else>
                        <h4 class="mb-2 text-subtitle-2 text-grey-darken-1 text-uppercase">Préférences de Période</h4>
                        <div class="d-flex flex-wrap gap-2 mb-4">
                            <v-chip
                                v-for="(score, type) in managementStore.employeePreferences[selectedEmployeeForAi.id].shift_type_preferences"
                                :key="type" color="primary" variant="tonal">
                                {{ type }} ({{ Math.round(score * 100) }}%)
                            </v-chip>
                        </div>

                        <h4 class="mb-2 text-subtitle-2 text-grey-darken-1 text-uppercase">Collègues fréquents</h4>
                        <v-list lines="one" class="pa-0 bg-transparent">
                            <v-list-item
                                v-for="colleague in managementStore.employeePreferences[selectedEmployeeForAi.id].preferred_colleagues"
                                :key="colleague.employee_id" class="px-0">
                                <template v-slot:prepend>
                                    <v-avatar color="grey-lighten-3" size="32" class="mr-3">
                                        <span class="text-caption">{{ colleague.employee_name.charAt(0) }}</span>
                                    </v-avatar>
                                </template>
                                <v-list-item-title class="text-body-2 font-weight-bold">{{ colleague.employee_name
                                    }}</v-list-item-title>
                                <v-list-item-subtitle class="text-caption">Travaillé ensemble {{
                                    colleague.co_assignments }}
                                    fois</v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </div>
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
import { useEmployeeStore } from '../stores/employeeStore'
import { useRoleStore } from '../stores/roleStore'
import { useContractStore } from '../stores/contractStore'
import { useAvailabilityStore } from '../stores/availabilityStore'
import { useAuthStore } from '../stores/authStore'
import { useManagementStore } from '../stores/managementStore'

const managementStore = useManagementStore()

const employeeStore = useEmployeeStore()
const roleStore = useRoleStore()
const contractStore = useContractStore()
const availabilityStore = useAvailabilityStore()
const authStore = useAuthStore()

const search = ref('')
const showInactive = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)
const dialogAvailability = ref(false)

const editedIndex = ref(-1)
const itemToDelete = ref(null)
const currentEmployeeForAvailability = ref(null)

const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })

const defaultItem = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    role_id: null,
    contract_type_id: null,
    status: 'Actif'
}
const editedItem = ref({ ...defaultItem })

const newAvailability = ref({
    dayOfWeek: 0,
    startTime: '09:00',
    endTime: '17:00',
    isRecurring: true
})

const daysOfWeek = [
    { name: 'Lundi', value: 0 },
    { name: 'Mardi', value: 1 },
    { name: 'Mercredi', value: 2 },
    { name: 'Jeudi', value: 3 },
    { name: 'Vendredi', value: 4 },
    { name: 'Samedi', value: 5 },
    { name: 'Dimanche', value: 6 }
]

const headers = computed(() => {
    const base = [
        { title: 'Collaborateur', key: 'name', align: 'start', sortable: true, value: item => `${item.firstName} ${item.lastName} ${item.email}` },
        { title: 'Rôle', key: 'role', align: 'start' },
        { title: 'Contrat', key: 'contract', align: 'start' },
        { title: 'Statut', key: 'status', align: 'center' },
    ]
    base.push({ title: 'Actions', key: 'actions', align: 'end', sortable: false })
    return base
})

const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Nouveau collaborateur' : 'Modifier collaborateur'
})

const currentEmployeeName = computed(() => {
    if (!currentEmployeeForAvailability.value) return ''
    return `${currentEmployeeForAvailability.value.firstName} ${currentEmployeeForAvailability.value.lastName}`
})

const getDayName = (dayValue) => {
    const day = daysOfWeek.find(d => d.value === dayValue)
    return day ? day.name : 'Inconnu'
}

const showNotification = (text, type = 'success') => {
    snackbar.value = { show: true, text, color: type, icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }
}

const openNewModal = () => {
    editedIndex.value = -1
    editedItem.value = { ...defaultItem }
    dialog.value = true
}

const editItem = (item) => {
    editedIndex.value = item.id
    editedItem.value = { ...item }
    dialog.value = true
}

const closeModal = () => {
    dialog.value = false
    setTimeout(() => {
        editedItem.value = { ...defaultItem }
        editedIndex.value = -1
    }, 300)
}

const saveItem = async () => {
    try {
        if (editedIndex.value > -1) {
            await employeeStore.updateEmployee(editedIndex.value, editedItem.value)
            showNotification('Collaborateur modifié avec succès')
        } else {
            await employeeStore.addEmployee(editedItem.value)
            showNotification('Collaborateur ajouté avec succès')
        }
        closeModal()
    } catch (error) {
        showNotification('Erreur lors de la sauvegarde', 'error')
    }
}

const confirmDelete = (item) => {
    itemToDelete.value = item
    dialogDelete.value = true
}

const deleteItemConfirm = async () => {
    if (itemToDelete.value) {
        try {
            await employeeStore.deleteEmployee(itemToDelete.value.id)
            showNotification('Collaborateur supprimé')
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error')
        }
    }
    dialogDelete.value = false
    itemToDelete.value = null
}

const openAvailabilityModal = async (item) => {
    currentEmployeeForAvailability.value = item
    if (authStore.isManager) {
        await availabilityStore.fetchAvailabilitiesByEmployee(item.id)
    } else {
        await availabilityStore.fetchMyAvailabilities()
    }
    dialogAvailability.value = true
}

const saveAvailability = async () => {
    try {
        await availabilityStore.addAvailability({
            employeeId: currentEmployeeForAvailability.value.id,
            ...newAvailability.value
        })
        newAvailability.value.startTime = '09:00'
        newAvailability.value.endTime = '17:00'
        showNotification('Disponibilité ajoutée')
    } catch (err) {
        showNotification('Erreur lors de l\'ajout de la disponibilité', 'error')
    }
}

const deleteAvailability = async (id) => {
    try {
        await availabilityStore.deleteAvailability(id)
        showNotification('Disponibilité supprimée')
    } catch (err) {
        showNotification('Erreur lors de la suppression', 'error')
    }
}

const aiProfileDialog = ref(false);
const selectedEmployeeForAi = ref(null);

const openAiProfile = async (employee) => {
    selectedEmployeeForAi.value = employee;
    aiProfileDialog.value = true;
    if (!managementStore.employeePreferences[employee.id]) {
        await managementStore.fetchEmployeePreferences(employee.id);
    }
}

onMounted(async () => {
    if (!authStore.user) await authStore.fetchCurrentUser()
    if (roleStore.roles.length === 0) await roleStore.fetchRoles()
    if (contractStore.contracts.length === 0) await contractStore.fetchContracts()
    if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()
})

const displayedEmployees = computed(() => {
    if (showInactive.value && authStore.isManager) {
        return employeeStore.employees;
    }
    return employeeStore.employees.filter(emp => emp.status !== 'Inactif');
})
</script>

<style scoped>
.gap-3 {
    gap: 0.75rem;
}

:deep(.v-data-table-header__content) {
    font-weight: 700;
    color: #64748B;
}

:deep(.v-data-table__tr:hover) {
    background-color: #F8FAFC !important;
}
</style>