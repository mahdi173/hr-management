<template>
  <v-app style="background-color: #F9FAFB;">
    <v-navigation-drawer v-model="drawer" border elevation="0" width="260" color="surface" app>
      <div class="pa-6 d-flex align-center">
        <v-icon color="primary" size="32" class="mr-3">mdi-clock-check-outline</v-icon>
        <span class="text-h5 font-weight-bold text-primary">Timeapp</span>
      </div>

      <v-list class="px-4" nav>
        <v-list-item v-for="item in menuItems" :key="item.title" :prepend-icon="item.icon" :title="item.title"
          :value="item.title" active-color="primary" rounded="lg" class="mb-2 list-item-hover"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar border elevation="0" color="surface" height="72" app>
      <v-app-bar-nav-icon @click="drawer = !drawer" color="grey-darken-2" class="ml-2"></v-app-bar-nav-icon>

      <v-spacer></v-spacer>

      <v-text-field hide-details prepend-inner-icon="mdi-magnify" placeholder="Rechercher un employé, un planning..."
        variant="solo-filled" flat density="compact" class="mx-4" style="max-width: 350px;" bg-color="#F3F4F6"
        rounded="lg"></v-text-field>

      <v-btn icon color="grey-darken-2" class="mr-3">
        <v-badge color="error" content="3" dot>
          <v-icon>mdi-bell-outline</v-icon>
        </v-badge>
      </v-btn>

      <v-avatar color="primary-lighten-4" size="40" class="mr-6 cursor-pointer hover-scale">
        <span class="text-primary font-weight-bold">LM</span>
      </v-avatar>
    </v-app-bar>

    <v-main>
      <div class="pa-6 pa-md-8 pt-4 pt-md-6">
        <DashboardView />
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import DashboardView from './components/DashboardView.vue'

const drawer = ref(true)

const menuItems = ref([
  { title: 'Tableau de bord', icon: 'mdi-view-dashboard-outline' },
  { title: 'Plannings', icon: 'mdi-calendar-month-outline' },
  { title: 'Équipe', icon: 'mdi-account-group-outline' },
  { title: 'Absences', icon: 'mdi-palm-tree' },
  { title: 'Paramètres', icon: 'mdi-cog-outline' },
])
</script>

<style>
.v-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
}

.list-item-hover:hover {
  background-color: #F3F4F6 !important;
  transition: background-color 0.2s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}
</style>