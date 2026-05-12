<template>
  <v-app style="background-color: #F9FAFB;">
    <v-navigation-drawer v-model="drawer" border elevation="0" width="260" color="surface" app>
      <div class="pa-6 d-flex align-center">
        <v-icon color="primary" size="32" class="mr-3">mdi-clock-check-outline</v-icon>
        <span class="text-h5 font-weight-bold text-primary">Timeapp</span>
      </div>

      <v-list class="px-4" nav>
        <v-list-item v-for="item in menuItems" :key="item.title" :prepend-icon="item.icon" :title="item.title"
          :to="item.path" active-color="primary" rounded="lg" class="mb-2 list-item-hover"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar border elevation="0" color="surface" height="72" app>
      <v-app-bar-nav-icon @click="drawer = !drawer" color="grey-darken-2" class="ml-2"></v-app-bar-nav-icon>

      <v-spacer></v-spacer>

      <v-autocomplete v-model="searchSelection" v-model:search="searchQuery" :items="globalSearchResults"
        item-title="title" item-value="id" hide-details prepend-inner-icon="mdi-magnify"
        placeholder="Rechercher un employé, un shift..." variant="solo-filled" flat density="compact"
        class="mx-4 d-none d-sm-block" style="max-width: 350px;" bg-color="#F3F4F6" rounded="lg" return-object
        no-data-text="Aucun résultat" @update:modelValue="handleSearchSelect">
        <template v-slot:item="{ props, item }">
          <v-list-item v-bind="props" :prepend-icon="item?.raw?.icon || 'mdi-magnify'"
            :subtitle="item?.raw?.subtitle || ''"></v-list-item>
        </template>
      </v-autocomplete>

      <v-btn icon color="grey-darken-2" class="mr-3">
        <v-badge color="error" content="3" dot>
          <v-icon>mdi-bell-outline</v-icon>
        </v-badge>

        <v-menu activator="parent" location="bottom end" :close-on-content-click="false" offset="10">
          <v-card rounded="xl" border elevation="0" min-width="320" max-width="360">
            <v-card-title class="text-subtitle-1 font-weight-bold px-4 py-3 border-bottom">Notifications</v-card-title>
            <v-list lines="two" class="pa-0">
              <v-list-item class="px-4 py-2 hover-bg">
                <template v-slot:prepend>
                  <v-avatar color="error-lighten-4" size="40" rounded="lg" class="mr-3">
                    <v-icon color="error" size="small">mdi-alert-circle-outline</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-body-2 font-weight-bold">Shifts non assignés</v-list-item-title>
                <v-list-item-subtitle class="text-caption">4 shifts à combler urgemment ce soir</v-list-item-subtitle>
              </v-list-item>

              <v-list-item class="px-4 py-2 hover-bg">
                <template v-slot:prepend>
                  <v-avatar color="warning-lighten-4" size="40" rounded="lg" class="mr-3">
                    <v-icon color="warning" size="small">mdi-palm-tree</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-body-2 font-weight-bold">Absence en attente</v-list-item-title>
                <v-list-item-subtitle class="text-caption">Sarah Martin a demandé un congé</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <div class="pa-3 text-center border-top">
              <v-btn variant="text" color="primary" size="small" class="font-weight-bold">Tout marquer comme lu</v-btn>
            </div>
          </v-card>
        </v-menu>
      </v-btn>

      <v-avatar color="primary-lighten-4" size="40" class="mr-4 mr-sm-6 cursor-pointer hover-scale">
        <span class="text-primary font-weight-bold">LM</span>
      </v-avatar>
    </v-app-bar>

    <v-main>
      <div class="pa-4 pa-sm-6 pa-md-8 pt-4 pt-md-6">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useEmployeeStore } from './stores/employeeStore'
import { useScheduleStore } from './stores/scheduleStore'

const router = useRouter()
const employeeStore = useEmployeeStore()
const scheduleStore = useScheduleStore()

const drawer = ref(true)

const menuItems = ref([
  { title: 'Tableau de bord', icon: 'mdi-view-dashboard-outline', path: '/' },
  { title: 'Plannings', icon: 'mdi-calendar-month-outline', path: '/plannings' },
  { title: 'Équipe', icon: 'mdi-account-group-outline', path: '/equipe' },
  { title: 'Absences', icon: 'mdi-palm-tree', path: '/absences' },
  { title: 'Paramètres', icon: 'mdi-cog-outline', path: '/parametres' },
])

const searchQuery = ref('')
const searchSelection = ref(null)

const globalSearchResults = computed(() => {
  const results = []

  employeeStore.employees.forEach(emp => {
    results.push({
      id: `emp_${emp.id}`,
      title: `${emp.firstName} ${emp.lastName}`,
      subtitle: `Employé • ${emp.email}`,
      icon: 'mdi-account-outline',
      route: '/equipe'
    })
  })

  scheduleStore.shifts.forEach(shift => {
    results.push({
      id: `shift_${shift.id}`,
      title: shift.employeeName ? `Shift: ${shift.employeeName}` : 'Shift: Non assigné',
      subtitle: `Planning • ${shift.date} • ${shift.roleName}`,
      icon: 'mdi-calendar-clock-outline',
      route: '/plannings'
    })
  })

  return results
})

const handleSearchSelect = (selectedItem) => {
  if (selectedItem && selectedItem.route) {
    router.push(selectedItem.route)

    setTimeout(() => {
      searchSelection.value = null
      searchQuery.value = ''
    }, 150)
  }
}

onMounted(async () => {
  if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()
  if (scheduleStore.shifts.length === 0) await scheduleStore.fetchWeeklyShifts()
})
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

.border-bottom {
  border-bottom: 1px solid #E2E8F0;
}

.border-top {
  border-top: 1px solid #E2E8F0;
}

.hover-bg:hover {
  background-color: #F8FAFC;
  cursor: pointer;
}
</style>