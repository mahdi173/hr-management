<template>
    <div class="parametres-view">
        <div class="d-flex flex-column flex-md-row justify-space-between align-md-center mb-6 mt-2">
            <div>
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Paramètres</h1>
                <p class="text-body-1 text-grey-darken-1">Configurez l'intelligence artificielle, les rôles et les types
                    de contrats.</p>
            </div>
        </div>

        <v-card border elevation="0" rounded="xl" class="mb-8 overflow-hidden border-primary">
            <div
                class="bg-blue-lighten-5 pa-6 d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between">
                <div class="mb-4 mb-sm-0 pr-sm-6">
                    <h3 class="text-h6 font-weight-bold d-flex align-center text-primary mb-1">
                        <v-icon class="mr-2">mdi-brain</v-icon> Entraînement de l'IA (Machine Learning)
                    </h3>
                    <p class="text-body-2 text-grey-darken-3 lh-sm">
                        Lancez l'analyse de l'historique des 3 derniers mois. L'IA apprendra les préférences de vos
                        employés (horaires, jours, collègues favoris) et optimisera ses futures recommandations de
                        planning.
                    </p>
                </div>
                <v-btn color="primary" variant="flat" rounded="lg" class="font-weight-bold px-6 flex-shrink-0"
                    size="large" @click="trainAi" :loading="managementStore.isTraining">
                    <v-icon class="mr-2">mdi-play-circle</v-icon> Lancer l'apprentissage
                </v-btn>
            </div>
        </v-card>

        <v-row>
            <v-col cols="12" md="6">
                <v-card border elevation="0" rounded="xl" class="overflow-hidden bg-white">
                    <div class="d-flex justify-space-between align-center pa-4 border-bottom bg-grey-lighten-4">
                        <h2 class="text-h6 font-weight-bold d-flex align-center">
                            <v-icon color="primary" class="mr-2">mdi-badge-account-horizontal-outline</v-icon>
                            Rôles
                        </h2>
                        <v-btn color="primary" variant="flat" rounded="lg" size="small" prepend-icon="mdi-plus"
                            @click="openRoleModal()">
                            Ajouter
                        </v-btn>
                    </div>

                    <v-table hover>
                        <thead>
                            <tr>
                                <th class="text-left font-weight-bold text-grey-darken-2">Nom du rôle</th>
                                <th class="text-right font-weight-bold text-grey-darken-2">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="roleStore.isLoading">
                                <td colspan="2" class="text-center pa-4">Chargement...</td>
                            </tr>
                            <tr v-else-if="roleStore.roles.length === 0">
                                <td colspan="2" class="text-center pa-4 text-grey-darken-1">Aucun rôle configuré</td>
                            </tr>
                            <tr v-else v-for="role in roleStore.roles" :key="role.id">
                                <td class="font-weight-medium">{{ role.name }}</td>
                                <td class="text-right">
                                    <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="primary"
                                        class="mr-1" @click="editRole(role)"></v-btn>
                                    <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error"
                                        @click="confirmDeleteRole(role)"></v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-col>

            <v-col cols="12" md="6">
                <v-card border elevation="0" rounded="xl" class="overflow-hidden bg-white">
                    <div class="d-flex justify-space-between align-center pa-4 border-bottom bg-grey-lighten-4">
                        <h2 class="text-h6 font-weight-bold d-flex align-center">
                            <v-icon color="secondary" class="mr-2">mdi-file-document-outline</v-icon>
                            Types de Contrats
                        </h2>
                        <v-btn color="secondary" variant="flat" rounded="lg" size="small" prepend-icon="mdi-plus"
                            @click="openContractModal()">
                            Ajouter
                        </v-btn>
                    </div>

                    <v-table hover>
                        <thead>
                            <tr>
                                <th class="text-left font-weight-bold text-grey-darken-2">Nom du contrat</th>
                                <th class="text-center font-weight-bold text-grey-darken-2">Heures / Semaine</th>
                                <th class="text-right font-weight-bold text-grey-darken-2">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="contractStore.isLoading">
                                <td colspan="3" class="text-center pa-4">Chargement...</td>
                            </tr>
                            <tr v-else-if="contractStore.contracts.length === 0">
                                <td colspan="3" class="text-center pa-4 text-grey-darken-1">Aucun contrat configuré</td>
                            </tr>
                            <tr v-else v-for="contract in contractStore.contracts" :key="contract.id">
                                <td class="font-weight-medium">{{ contract.name }}</td>
                                <td class="text-center">{{ contract.weekly_hours }} h</td>
                                <td class="text-right">
                                    <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="primary"
                                        class="mr-1" @click="editContract(contract)"></v-btn>
                                    <v-btn icon="mdi-delete-outline" variant="text" size="small" color="error"
                                        @click="confirmDeleteContract(contract)"></v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-col>
        </v-row>

        <v-dialog v-model="dialogRole" max-width="500" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ editedRoleIndex === -1 ? 'Nouveau rôle' : 'Modifier le rôle' }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="closeRoleModal"></v-btn>
                </v-card-title>
                <v-card-text class="px-6 pt-4">
                    <v-text-field v-model="editedRole.name" label="Nom du rôle" variant="outlined" density="comfortable"
                        color="primary" placeholder="ex: Serveur, Barman, Manager"></v-text-field>
                </v-card-text>
                <v-divider class="mt-2"></v-divider>
                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="closeRoleModal">Annuler</v-btn>
                    <v-btn variant="flat" color="primary" rounded="lg" class="px-6 font-weight-bold" @click="saveRole"
                        :disabled="!editedRole.name">Enregistrer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDeleteRole" max-width="450">
            <v-card rounded="xl" elevation="0" border class="pa-4 text-center">
                <v-avatar color="#FEF2F2" size="64" class="mx-auto mt-4 mb-4">
                    <v-icon color="error" size="32">mdi-delete-outline</v-icon>
                </v-avatar>
                <h3 class="text-h6 font-weight-bold mb-2">Supprimer ce rôle ?</h3>
                <p class="text-body-2 text-grey-darken-1 mb-6 px-4">
                    Êtes-vous sûr de vouloir supprimer le rôle <strong>{{ roleToDelete?.name }}</strong> ? Cette action
                    est irréversible.
                </p>
                <div class="d-flex justify-center mb-2">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium" rounded="lg"
                        @click="dialogDeleteRole = false">Annuler</v-btn>
                    <v-btn variant="flat" color="error" rounded="lg" class="px-6 font-weight-bold"
                        @click="deleteRoleConfirm">Oui, supprimer</v-btn>
                </div>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogContract" max-width="500" persistent>
            <v-card rounded="xl" elevation="0" border>
                <v-card-title class="px-6 pt-6 pb-2 font-weight-bold d-flex justify-space-between align-center text-h6">
                    {{ editedContractIndex === -1 ? 'Nouveau type de contrat' : 'Modifier le contrat' }}
                    <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1"
                        @click="closeContractModal"></v-btn>
                </v-card-title>
                <v-card-text class="px-6 pt-4">
                    <v-row>
                        <v-col cols="12" class="pb-1">
                            <v-text-field v-model="editedContract.name" label="Nom du contrat" variant="outlined"
                                density="comfortable" color="secondary"
                                placeholder="ex: CDI - Temps partiel"></v-text-field>
                        </v-col>
                        <v-col cols="12" class="pt-1">
                            <v-text-field v-model.number="editedContract.weekly_hours" label="Heures par semaine"
                                type="number" variant="outlined" density="comfortable" color="secondary"></v-text-field>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-divider class="mt-2"></v-divider>
                <v-card-actions class="px-6 py-4 d-flex justify-end bg-grey-lighten-4">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium"
                        @click="closeContractModal">Annuler</v-btn>
                    <v-btn variant="flat" color="secondary" rounded="lg" class="px-6 font-weight-bold"
                        @click="saveContract"
                        :disabled="!editedContract.name || !editedContract.weekly_hours">Enregistrer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDeleteContract" max-width="450">
            <v-card rounded="xl" elevation="0" border class="pa-4 text-center">
                <v-avatar color="#FEF2F2" size="64" class="mx-auto mt-4 mb-4">
                    <v-icon color="error" size="32">mdi-delete-outline</v-icon>
                </v-avatar>
                <h3 class="text-h6 font-weight-bold mb-2">Supprimer ce contrat ?</h3>
                <p class="text-body-2 text-grey-darken-1 mb-6 px-4">
                    Êtes-vous sûr de vouloir supprimer le contrat <strong>{{ contractToDelete?.name }}</strong> ? Cette
                    action est irréversible.
                </p>
                <div class="d-flex justify-center mb-2">
                    <v-btn variant="text" color="grey-darken-2" class="mr-3 font-weight-medium" rounded="lg"
                        @click="dialogDeleteContract = false">Annuler</v-btn>
                    <v-btn variant="flat" color="error" rounded="lg" class="px-6 font-weight-bold"
                        @click="deleteContractConfirm">Oui, supprimer</v-btn>
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
import { useAuthStore } from '../stores/authStore'
import { useManagementStore } from '../stores/managementStore'

const roleStore = useRoleStore()
const contractStore = useContractStore()
const authStore = useAuthStore()
const managementStore = useManagementStore()

const snackbar = ref({ show: false, text: '', color: 'success', icon: 'mdi-check-circle' })
const showNotification = (text, type = 'success') => {
    snackbar.value = { show: true, text, color: type, icon: type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }
}

const trainAi = async () => {
    try {
        await managementStore.trainAiPreferences()
        showNotification("L'IA a terminé l'analyse de l'historique avec succès !")
    } catch (err) {
        showNotification("Erreur lors de l'apprentissage de l'IA", "error")
    }
}

const dialogRole = ref(false)
const dialogDeleteRole = ref(false)
const editedRoleIndex = ref(-1)
const roleToDelete = ref(null)
const defaultRole = { name: '' }
const editedRole = ref({ ...defaultRole })

const openRoleModal = () => {
    editedRoleIndex.value = -1
    editedRole.value = { ...defaultRole }
    dialogRole.value = true
}

const editRole = (role) => {
    editedRoleIndex.value = role.id
    editedRole.value = { ...role }
    dialogRole.value = true
}

const closeRoleModal = () => {
    dialogRole.value = false
    setTimeout(() => { editedRole.value = { ...defaultRole }; editedRoleIndex.value = -1 }, 300)
}

const saveRole = async () => {
    try {
        if (editedRoleIndex.value > -1) {
            await roleStore.updateRole(editedRoleIndex.value, editedRole.value)
            showNotification('Rôle modifié avec succès')
        } else {
            await roleStore.addRole(editedRole.value)
            showNotification('Rôle ajouté avec succès')
        }
        closeRoleModal()
    } catch (error) {
        showNotification('Erreur lors de la sauvegarde', 'error')
    }
}

const confirmDeleteRole = (role) => {
    roleToDelete.value = role
    dialogDeleteRole.value = true
}

const deleteRoleConfirm = async () => {
    if (roleToDelete.value) {
        try {
            await roleStore.deleteRole(roleToDelete.value.id)
            showNotification('Rôle supprimé')
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error')
        }
    }
    dialogDeleteRole.value = false
    roleToDelete.value = null
}

const dialogContract = ref(false)
const dialogDeleteContract = ref(false)
const editedContractIndex = ref(-1)
const contractToDelete = ref(null)
const defaultContract = { name: '', weekly_hours: 35 }
const editedContract = ref({ ...defaultContract })

const openContractModal = () => {
    editedContractIndex.value = -1
    editedContract.value = { ...defaultContract }
    dialogContract.value = true
}

const editContract = (contract) => {
    editedContractIndex.value = contract.id
    editedContract.value = { ...contract }
    dialogContract.value = true
}

const closeContractModal = () => {
    dialogContract.value = false
    setTimeout(() => { editedContract.value = { ...defaultContract }; editedContractIndex.value = -1 }, 300)
}

const saveContract = async () => {
    try {
        if (editedContractIndex.value > -1) {
            await contractStore.updateContract(editedContractIndex.value, editedContract.value)
            showNotification('Contrat modifié avec succès')
        } else {
            await contractStore.addContract(editedContract.value)
            showNotification('Contrat ajouté avec succès')
        }
        closeContractModal()
    } catch (error) {
        showNotification('Erreur lors de la sauvegarde', 'error')
    }
}

const confirmDeleteContract = (contract) => {
    contractToDelete.value = contract
    dialogDeleteContract.value = true
}

const deleteContractConfirm = async () => {
    if (contractToDelete.value) {
        try {
            await contractStore.deleteContract(contractToDelete.value.id)
            showNotification('Contrat supprimé')
        } catch (error) {
            showNotification('Erreur lors de la suppression', 'error')
        }
    }
    dialogDeleteContract.value = false
    contractToDelete.value = null
}

onMounted(async () => {
    if (!authStore.user) await authStore.fetchCurrentUser()
    await Promise.all([
        roleStore.fetchRoles(),
        contractStore.fetchContracts()
    ])
})
</script>

<style scoped>
.border-bottom {
    border-bottom: 1px solid #E2E8F0;
}

.border-primary {
    border: 1px solid #BFDBFE !important;
}
</style>