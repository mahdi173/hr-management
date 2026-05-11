<template>
    <div class="equipe-view">
        <div class="d-flex flex-column flex-md-row justify-space-between align-md-center mb-6 mt-2">
            <div>
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Équipe</h1>
                <p class="text-body-1 text-grey-darken-1">Gérez vos collaborateurs et leurs contrats.</p>
            </div>
            <div class="mt-4 mt-md-0 d-flex align-center">
                <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" placeholder="Rechercher un membre..."
                    variant="outlined" density="compact" hide-details bg-color="white" rounded="lg"
                    style="min-width: 280px;"></v-text-field>

                <v-btn color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus"
                    class="ml-4 px-5 font-weight-bold" @click="openNewModal">
                    Ajouter
                </v-btn>
            </div>
        </div>

        <v-card border elevation="0" rounded="xl" class="overflow-hidden">
            <v-data-table :headers="headers" :items="employeeStore.employees" :search="search"
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
                        <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="primary" class="mr-1"
                            @click="editItem(item)"></v-btn>
                        <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error"
                            @click="confirmDelete(item)"></v-btn>
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
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEmployeeStore } from '../stores/employeeStore'
import { useRoleStore } from '../stores/roleStore'
import { useContractStore } from '../stores/contractStore'

const employeeStore = useEmployeeStore()
const roleStore = useRoleStore()
const contractStore = useContractStore()

const search = ref('')

const dialog = ref(false)
const dialogDelete = ref(false)

const editedIndex = ref(-1)
const itemToDelete = ref(null)

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

const headers = [
    {
        title: 'Collaborateur',
        key: 'name',
        align: 'start',
        sortable: true,
        value: item => `${item.firstName} ${item.lastName} ${item.email}`
    },
    { title: 'Rôle', key: 'role', align: 'start' },
    { title: 'Contrat', key: 'contract', align: 'start' },
    { title: 'Statut', key: 'status', align: 'center' },
    { title: 'Actions', key: 'actions', align: 'end', sortable: false },
]

const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'Nouveau collaborateur' : 'Modifier collaborateur'
})

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

const saveItem = () => {
    if (editedIndex.value > -1) {
        employeeStore.updateEmployee(editedIndex.value, editedItem.value)
    } else {
        employeeStore.addEmployee(editedItem.value)
    }
    closeModal()
}

const confirmDelete = (item) => {
    itemToDelete.value = item
    dialogDelete.value = true
}

const deleteItemConfirm = () => {
    if (itemToDelete.value) {
        employeeStore.deleteEmployee(itemToDelete.value.id)
    }
    dialogDelete.value = false
    itemToDelete.value = null
}

onMounted(async () => {
    if (roleStore.roles.length === 0) await roleStore.fetchRoles()
    if (contractStore.contracts.length === 0) await contractStore.fetchContracts()
    if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()
})
</script>

<style scoped>
:deep(.v-data-table-header__content) {
    font-weight: 700;
    color: #64748B;
}

:deep(.v-data-table__tr:hover) {
    background-color: #F8FAFC !important;
}
</style>