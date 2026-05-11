<template>
    <div class="dashboard">
        <div class="d-flex justify-space-between align-center mb-8 mt-2">
            <div>
                <h1 class="text-h4 font-weight-bold text-grey-darken-4 mb-2">Bonjour, Louis 👋</h1>
                <p class="text-body-1 text-grey-darken-1">Voici l'état de votre équipe pour aujourd'hui.</p>
            </div>
            <v-btn color="primary" variant="flat" rounded="lg" size="large" prepend-icon="mdi-plus" class="px-6">
                Nouveau Planning
            </v-btn>
        </div>

        <v-row class="mb-6">
            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Shifts non assignés</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">4</h2>
                        </div>
                        <v-avatar color="#FEF2F2" rounded="lg" size="48">
                            <v-icon color="error">mdi-alert-circle-outline</v-icon>
                        </v-avatar>
                    </div>
                    <div class="mt-5 text-caption text-error font-weight-bold d-flex align-center">
                        <v-icon size="small" class="mr-1">mdi-arrow-up-right</v-icon>
                        <span>À traiter urgemment pour ce soir</span>
                    </div>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Absences en attente</p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">2</h2>
                        </div>
                        <v-avatar color="#FFFBEB" rounded="lg" size="48">
                            <v-icon color="warning">mdi-palm-tree</v-icon>
                        </v-avatar>
                    </div>
                    <div class="mt-5 text-caption text-warning font-weight-bold">
                        Demandes pour la semaine prochaine
                    </div>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="pa-6 hover-card">
                    <div class="d-flex justify-space-between align-start">
                        <div>
                            <p class="text-body-2 text-grey-darken-1 font-weight-medium mb-2">Complétion Planning (S32)
                            </p>
                            <h2 class="text-h3 font-weight-bold text-grey-darken-4">85%</h2>
                        </div>
                        <v-avatar color="#ECFDF5" rounded="lg" size="48">
                            <v-icon color="success">mdi-check-circle-outline</v-icon>
                        </v-avatar>
                    </div>
                    <v-progress-linear model-value="85" color="success" height="8" rounded
                        class="mt-5"></v-progress-linear>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12" md="8">
                <v-card border elevation="0" rounded="xl" class="fill-height pb-4">
                    <v-card-title class="px-6 pt-6 pb-4 d-flex justify-space-between align-center">
                        <span class="text-h6 font-weight-bold">Service du jour</span>
                        <v-btn variant="text" color="primary" size="small" class="font-weight-bold">Voir tout</v-btn>
                    </v-card-title>

                    <v-divider class="mb-4"></v-divider>

                    <v-list lines="two" class="px-4">
                        <v-list-item v-for="shift in todayShifts" :key="shift.id" class="mb-3 rounded-lg shift-item">
                            <template v-slot:prepend>
                                <v-avatar :color="shift.color" size="48" rounded="lg"
                                    class="mr-4 font-weight-bold text-white">
                                    {{ shift.initials }}
                                </v-avatar>
                            </template>

                            <v-list-item-title class="font-weight-bold text-body-1">{{ shift.name }}</v-list-item-title>
                            <v-list-item-subtitle class="text-grey-darken-1 mt-1">
                                <v-icon size="small" class="mr-1">mdi-clock-outline</v-icon>
                                {{ shift.time }} • {{ shift.role }}
                            </v-list-item-subtitle>

                            <template v-slot:append>
                                <v-chip size="small" :color="shift.statusColor" variant="tonal"
                                    class="font-weight-bold px-3">
                                    {{ shift.status }}
                                </v-chip>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card border elevation="0" rounded="xl" class="fill-height" bg-color="#F4F6FF">
                    <v-card-title class="px-6 pt-6 pb-3">
                        <span class="text-h6 font-weight-bold text-primary d-flex align-center">
                            <v-icon class="mr-2">mdi-creation</v-icon> Insights IA
                        </span>
                    </v-card-title>

                    <v-card-text class="px-6">
                        <p class="text-body-2 text-grey-darken-1 mb-5">
                            Recommandations pour optimiser votre semaine.
                        </p>

                        <v-card border elevation="0" rounded="xl" class="mb-4 pa-5 insight-card" color="white">
                            <div class="d-flex align-start">
                                <v-avatar color="#FFFBEB" size="40" rounded="lg" class="mr-4 mt-1">
                                    <v-icon color="warning" size="small">mdi-account-alert</v-icon>
                                </v-avatar>
                                <div>
                                    <h4 class="text-subtitle-1 font-weight-bold mb-1">Risque de surcharge</h4>
                                    <p class="text-body-2 text-grey-darken-1 mb-3 lh-sm">Mehdi Zougari est planifié 42h
                                        cette
                                        semaine (Contrat: 35h).</p>
                                    <v-btn size="small" variant="tonal" color="primary" rounded="lg"
                                        class="font-weight-bold">Rééquilibrer</v-btn>
                                </div>
                            </div>
                        </v-card>

                        <v-card border elevation="0" rounded="xl" class="pa-5 insight-card" color="white">
                            <div class="d-flex align-start">
                                <v-avatar color="#E0F2FE" size="40" rounded="lg" class="mr-4 mt-1">
                                    <v-icon color="secondary" size="small">mdi-auto-fix</v-icon>
                                </v-avatar>
                                <div>
                                    <h4 class="text-subtitle-1 font-weight-bold mb-1">Staffing Optimal</h4>
                                    <p class="text-body-2 text-grey-darken-1 mb-3 lh-sm">L'IA suggère d'ajouter 1
                                        serveur ce soir en
                                        raison de la météo favorable.</p>
                                    <v-btn size="small" variant="tonal" color="secondary" rounded="lg"
                                        class="font-weight-bold">Voir
                                        suggestion</v-btn>
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
import { ref } from 'vue'

const todayShifts = ref([
    { id: 1, name: 'Sarah Martin', initials: 'SM', time: '18:00 - 23:30', role: 'Chef de rang', status: 'Confirmé', statusColor: 'success', color: 'primary' },
    { id: 2, name: 'Illia Semenov', initials: 'IS', time: '18:30 - 23:30', role: 'Serveur', status: 'En attente', statusColor: 'warning', color: '#6366F1' },
    { id: 3, name: 'Ouahid Bouanani', initials: 'OB', time: '17:00 - 23:00', role: 'Cuisinier', status: 'Confirmé', statusColor: 'success', color: 'secondary' },
    { id: 4, name: 'Non assigné', initials: '?', time: '19:00 - 23:30', role: 'Plongeur', status: 'À combler', statusColor: 'error', color: 'grey-darken-1' },
])
</script>

<style scoped>
.hover-card {
    transition: all 0.2s ease-in-out;
}

.hover-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025) !important;
    border-color: transparent !important;
}

.shift-item {
    transition: background-color 0.2s ease;
}

.shift-item:hover {
    background-color: #F9FAFB;
}

.insight-card {
    transition: border-color 0.2s ease;
}

.insight-card:hover {
    border-color: #CBD5E1 !important;
}

.lh-sm {
    line-height: 1.4 !important;
}
</style>