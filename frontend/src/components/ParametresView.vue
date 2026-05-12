<template>
    <div class="parametres-view">
        <div class="mb-6 mt-2">
            <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Paramètres</h1>
            <p class="text-body-1 text-grey-darken-1">Configurez les règles de votre établissement.</p>
        </div>

        <v-row>
            <v-col cols="12" md="3" lg="2">
                <v-card border elevation="0" rounded="xl" class="bg-white pa-2">
                    <v-list class="bg-transparent" nav>
                        <v-list-item v-for="tab in tabs" :key="tab.value" :value="tab.value"
                            :active="currentTab === tab.value" active-color="primary" rounded="lg"
                            class="mb-1 cursor-pointer font-weight-medium" @click="currentTab = tab.value">
                            <template v-slot:prepend>
                                <v-icon :color="currentTab === tab.value ? 'primary' : 'grey-darken-1'">{{ tab.icon
                                    }}</v-icon>
                            </template>
                            <v-list-item-title :class="{ 'text-primary font-weight-bold': currentTab === tab.value }">
                                {{ tab.title }}
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>

            <v-col cols="12" md="9" lg="10">
                <v-card border elevation="0" rounded="xl" class="bg-white pa-4 pa-sm-6 min-height-card">
                    <div v-if="currentTab === 'general'">
                        <div class="d-flex align-center mb-6 border-bottom pb-4">
                            <v-icon size="large" color="primary" class="mr-3">mdi-store</v-icon>
                            <h2 class="text-h6 font-weight-bold">Informations générales</h2>
                        </div>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <v-text-field v-model="generalSettings.name" label="Nom de l'établissement"
                                    variant="outlined" density="comfortable" color="primary"></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <v-text-field v-model="generalSettings.email" label="Email de contact" type="email"
                                    variant="outlined" density="comfortable" color="primary"></v-text-field>
                            </v-col>
                        </v-row>
                        <v-btn color="primary" variant="flat" rounded="lg" class="px-6 font-weight-bold mt-4"
                            @click="showNotification('Paramètres généraux enregistrés')">Sauvegarder</v-btn>
                    </div>

                    <div v-if="currentTab === 'roles'">
                        <div
                            class="d-flex flex-column flex-sm-row justify-space-between align-sm-center mb-6 border-bottom pb-4 gap-3">
                            <div class="d-flex align-center">
                                <v-icon size="large" color="primary" class="mr-3">mdi-badge-account</v-icon>
                                <h2 class="text-h6 font-weight-bold">Gestion des rôles</h2>
                            </div>
                            <v-btn color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus" class="px-4"
                                @click="openRoleModal()">
                                Ajouter un rôle
                            </v-btn>
                        </div>

                        <v-list lines="one" class="bg-transparent pa-0">
                            <v-card v-for="role in roleStore.roles" :key="role.id" border elevation="0" rounded="lg"
                                class="mb-3 px-4 py-2 d-flex align-center justify-space-between hover-card">
                                <div class="font-weight-medium text-body-1">{{ role.name }}</div>
                                <div>
                                    <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="primary"
                                        class="mr-1" @click="openRoleModal(role)"></v-btn>
                                    <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error"
                                        @click="confirmDelete('role', role)"></v-btn>
                                </div>
                            </v-card>
                        </v-list>
                    </div>

                    <div v-if="currentTab === 'contracts'">
                        <div
                            class="d-flex flex-column flex-sm-row justify-space-between align-sm-center mb-6 border-bottom pb-4 gap-3">
                            <div class="d-flex align-center">
                                <v-icon size="large" color="primary" class="mr-3">mdi-file-document-edit</v-icon>
                                <h2 class="text-h6 font-weight-bold">Types de contrats</h2>
                            </div>
                            <v-btn color="primary" variant="flat" rounded="lg" prepend-icon="mdi-plus" class="px-4"
                                @click="openContractModal()">
                                Ajouter un contrat
                            </v-btn>
                        </div>

                        <v-list lines="one" class="bg-transparent pa-0">
                            <v-card v-for="contract in contractStore.contracts" :key="contract.id" border elevation="0"
                                rounded="lg"
                                class="mb-3 px-4 py-2 d-flex align-center justify-space-between hover-card">
                                <div>
                                    <div class="font-weight-bold text-body-1">{{ contract.name }}</div>
                                    <div class="text-caption text-grey-darken-1">{{ contract.weekly_hours }} heures par
                                        semaine
                                    </div>
                                </div>
                                <div>
                                    <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="primary"
                                        class="mr-1" @click="openContractModal(contract)"></v-btn>
                                    <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error"
                                        @click="confirmDelete('contract', contract)"></v-btn>
                                </div>
                            </v-card>
                        </v-list>
                    </div>
                </v-card>
            </v-col>
        </v-row>

        <v-dialog v-model="roleDialog" max-width="400" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ isEditing ? 'Modifier le rôle' : 'Nouveau rôle' }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="roleDialog = false"></v-btn>
                </v-card-title>
                <v-card-text class="px-6 pt-4">
                    <v-text-field v-model="editedRole.name" label="Nom du rôle" variant="outlined" density="comfortable"
                        color="primary"></v-text-field>
                </v-card-text>
                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="roleDialog = false">Annuler</v-btn>
                    <v-btn variant="flat" color="primary" rounded="lg" class="px-6 font-weight-bold"
                        @click="saveRole">Enregistrer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="contractDialog" max-width="400" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ isEditing ? 'Modifier le contrat' : 'Nouveau contrat' }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="contractDialog = false"></v-btn>
                </v-card-title>
                <v-card-text class="px-6 pt-4">
                    <v-text-field v-model="editedContract.name" label="Nom du contrat" variant="outlined"
                        density="comfortable" color="primary" class="mb-2"></v-text-field>
                    <v-text-field v-model.number="editedContract.weekly_hours" label="Heures hebdomadaires"
                        type="number" variant="outlined" density="comfortable" color="primary" hint="0 pour les extras"
                        persistent-hint></v-text-field>
                </v-card-text>
                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4 mt-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="contractDialog = false">Annuler</v-btn>
                    <v-btn variant="flat" color="primary" rounded="lg" class="px-6 font-weight-bold"
                        @click="saveContract">Enregistrer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="deleteDialog" max-width="400">
            <v-card rounded="xl" elevation="0" border class="pa-4 text-center">
                <v-avatar color="#FEF2F2" size="64" class="mx-auto mt-4 mb-4">
                    <v-icon color="error" size="32">mdi-delete-outline</v-icon>
                </v-avatar>
                <h3 class="text-h6 font-weight-bold mb-2">Confirmer la suppression</h3>
                <p class="text-body-2 text-grey-darken-1 mb-6 px-4">
                    Êtes-vous sûr de vouloir supprimer cet élément ? Cette action est irréversible.
                </p>
                <div class="d-flex justify-center mb-2">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium" rounded="lg"
                        @click="deleteDialog = false">Annuler</v-btn>
                    <v-btn variant="flat" color="error" rounded="lg" class="px-6 font-weight-bold"
                        @click="executeDelete">Oui,
                        supprimer</v-btn>
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
import { ref, onMounted } from 'vue'
import { useRoleStore } from '../stores/roleStore'
import { useContractStore } from '../stores/contractStore'

const roleStore = useRoleStore()
const contractStore = useContractStore()

const currentTab = ref('general')
const tabs = [
    { title: 'Général', value: 'general', icon: 'mdi-store-cog-outline' },
    { title: 'Rôles', value: 'roles', icon: 'mdi-badge-account-outline' },
    { title: 'Contrats', value: 'contracts', icon: 'mdi-file-document-edit-outline' }
]

const generalSettings = ref({
    name: 'Le Central',
    email: 'contact@lecentral.fr'
})

const roleDialog = ref(false)
const contractDialog = ref(false)
const deleteDialog = ref(false)
const isEditing = ref(false)

const itemToDelete = ref({ type: '', id: null })
const editedRole = ref({ id: null, name: '' })
const editedContract = ref({ id: null, name: '', weekly_hours: 0 })

const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })

const showNotification = (text, type = 'success') => {
    snackbar.value = { show: true, text, color: type, icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }
}

const openRoleModal = (role = null) => {
    isEditing.value = !!role
    editedRole.value = role ? { ...role } : { id: null, name: '' }
    roleDialog.value = true
}

const saveRole = async () => {
    if (isEditing.value) {
        await roleStore.updateRole(editedRole.value.id, editedRole.value)
        showNotification('Rôle modifié')
    } else {
        await roleStore.addRole(editedRole.value)
        showNotification('Rôle ajouté')
    }
    roleDialog.value = false
}

const openContractModal = (contract = null) => {
    isEditing.value = !!contract
    editedContract.value = contract ? { ...contract } : { id: null, name: '', weekly_hours: 35 }
    contractDialog.value = true
}

const saveContract = async () => {
    if (isEditing.value) {
        await contractStore.updateContract(editedContract.value.id, editedContract.value)
        showNotification('Contrat modifié')
    } else {
        await contractStore.addContract(editedContract.value)
        showNotification('Contrat ajouté')
    }
    contractDialog.value = false
}

const confirmDelete = (type, item) => {
    itemToDelete.value = { type, id: item.id }
    deleteDialog.value = true
}

const executeDelete = async () => {
    if (itemToDelete.value.type === 'role') {
        await roleStore.deleteRole(itemToDelete.value.id)
        showNotification('Rôle supprimé', 'error')
    } else if (itemToDelete.value.type === 'contract') {
        await contractStore.deleteContract(itemToDelete.value.id)
        showNotification('Contrat supprimé', 'error')
    }
    deleteDialog.value = false
}

onMounted(async () => {
    if (roleStore.roles.length === 0) await roleStore.fetchRoles()
    if (contractStore.contracts.length === 0) await contractStore.fetchContracts()
})
</script>

<style scoped>
.gap-3 {
    gap: 0.75rem;
}

.border-bottom {
    border-bottom: 1px solid #E2E8F0;
}

.min-height-card {
    min-height: 400px;
}

.hover-card {
    transition: background-color 0.2s;
    border: 1px solid #E2E8F0 !important;
}

.hover-card:hover {
    background-color: #F8FAFC !important;
}
</style>