<template>
  <v-app :style="isLanding ? 'background: white' : 'background-color: #F9FAFB'">

    <template v-if="isLanding">
      <router-view></router-view>
    </template>

    <template v-else>
      <v-navigation-drawer v-model="drawer" border elevation="0" width="260" color="surface" app>
        <div class="pa-5 d-flex align-center">
          <v-icon color="primary" size="30" class="mr-2">mdi-clock-time-four-outline</v-icon>
          <span class="text-h6 font-weight-bold">Timeapp</span>
        </div>

        <v-list class="px-4" nav>
          <v-list-item v-for="item in menuItems" :key="item.title" :prepend-icon="item.icon" :title="item.title"
            :to="item.path" active-color="primary" rounded="lg" class="mb-2 list-item-hover"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-app-bar border elevation="0" color="surface" height="72" app>
        <v-app-bar-nav-icon @click="drawer = !drawer" color="grey-darken-2" class="ml-2"></v-app-bar-nav-icon>

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

        <v-spacer></v-spacer>

        <v-btn icon color="grey-darken-2" class="mr-3">
          <v-badge :color="activeNotifications.length > 0 ? 'error' : 'transparent'"
            :content="activeNotifications.length" :dot="activeNotifications.length > 0">
            <v-icon>mdi-bell-outline</v-icon>
          </v-badge>

          <v-menu activator="parent" location="bottom end" :close-on-content-click="false" offset="10">
            <v-card rounded="xl" border elevation="0" min-width="320" max-width="360">
              <v-card-title class="text-subtitle-1 font-weight-bold px-4 py-3 border-bottom">
                Notifications ({{ activeNotifications.length }})
              </v-card-title>

              <v-list lines="two" class="pa-0" v-if="activeNotifications.length > 0">
                <v-list-item v-for="(notif, idx) in activeNotifications" :key="idx" class="px-4 py-2 hover-bg"
                  @click="handleNotifClick(notif)">
                  <template v-slot:prepend>
                    <v-avatar :color="notif.color + '-lighten-4'" size="40" rounded="lg" class="mr-3">
                      <v-icon :color="notif.color" size="small">{{ notif.icon }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-2 font-weight-bold">{{ notif.title }}</v-list-item-title>
                  <v-list-item-subtitle class="text-caption">{{ notif.subtitle }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>

              <div v-else class="pa-6 text-center text-grey-darken-1 text-body-2">
                Aucune nouvelle notification
              </div>

              <div class="pa-3 text-center border-top" v-if="activeNotifications.length > 0">
                <v-btn variant="text" color="primary" size="small" class="font-weight-bold" @click="clearNotifications">
                  Tout marquer comme lu
                </v-btn>
              </div>
            </v-card>
          </v-menu>
        </v-btn>

        <v-menu location="bottom end" offset="10">
          <template v-slot:activator="{ props }">
            <v-avatar v-bind="props" color="primary-lighten-4" size="40"
              class="mr-4 mr-sm-6 cursor-pointer hover-scale">
              <span class="text-primary font-weight-bold">{{ authStore.userInitials }}</span>
            </v-avatar>
          </template>
          <v-list rounded="lg" elevation="2" min-width="150">
            <v-list-item @click="authStore.logout()" prepend-icon="mdi-logout" title="Déconnexion" class="text-error">
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>

      <v-main>
        <div class="pa-4 pa-sm-6 pa-md-8 pt-4 pt-md-6">
          <router-view></router-view>
        </div>
      </v-main>
    </template>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEmployeeStore } from './stores/employeeStore'
import { useScheduleStore } from './stores/scheduleStore'
import { useAbsenceStore } from './stores/absenceStore'
import { useAuthStore } from './stores/authStore'

const router = useRouter()
const route = useRoute()
const employeeStore = useEmployeeStore()
const scheduleStore = useScheduleStore()
const absenceStore = useAbsenceStore()
const authStore = useAuthStore()

const drawer = ref(true)
const notificationsClearedAt = ref(Date.now() - 10000)

const isLanding = computed(() => {
  return route.path === '/' || route.path === '/login' || route.path === '/register'
})

const menuItems = computed(() => {
  const baseItems = [
    { title: 'Tableau de bord', icon: 'mdi-view-dashboard-outline', path: '/dashboard' },
    { title: 'Plannings', icon: 'mdi-calendar-month-outline', path: '/plannings' },
    { title: 'Équipe', icon: 'mdi-account-group-outline', path: '/equipe' },
    { title: 'Absences', icon: 'mdi-palm-tree', path: '/absences' },
  ]

  if (authStore.isManager) {
    baseItems.push({ title: 'Paramètres', icon: 'mdi-cog-outline', path: '/parametres' })
  }

  return baseItems
})

const hiddenNotifIds = ref([])

const activeNotifications = computed(() => {
  const notifs = [];

  if (authStore.isManager) {
    const unassignedCount = scheduleStore.shifts.filter(s => !s.employeeId).length;
    if (unassignedCount > 0) {
      notifs.push({
        id: `unassigned_shifts_${unassignedCount}`,
        title: 'Shifts non assignés',
        subtitle: `${unassignedCount} shift(s) nécessitent une assignation urgente.`,
        icon: 'mdi-alert-circle-outline',
        color: 'error',
        route: '/plannings'
      });
    }

    const pendingAbsCount = absenceStore.pendingAbsences.length;
    if (pendingAbsCount > 0) {
      notifs.push({
        id: `pending_absences_${pendingAbsCount}`,
        title: 'Absences en attente',
        subtitle: `${pendingAbsCount} demande(s) en attente de validation.`,
        icon: 'mdi-palm-tree',
        color: 'warning',
        route: '/absences'
      });
    }
  } else {
    const myApproved = absenceStore.absences.filter(a => a.status === 'Approuvé' && !a.viewed);
    if (myApproved.length > 0) {
      notifs.push({
        id: `approved_abs_${myApproved.length}`,
        title: 'Absence approuvée',
        subtitle: `Votre demande d'absence a été validée.`,
        icon: 'mdi-check-circle-outline',
        color: 'success',
        route: '/absences'
      });
    }

    const myRejected = absenceStore.absences.filter(a => a.status === 'Refusé' && !a.viewed);
    if (myRejected.length > 0) {
      notifs.push({
        id: `rejected_abs_${myRejected.length}`,
        title: 'Absence refusée',
        subtitle: `Votre demande d'absence a été refusée.`,
        icon: 'mdi-close-circle-outline',
        color: 'error',
        route: '/absences'
      });
    }
  }

  return notifs.filter(n => !hiddenNotifIds.value.includes(n.id));
})

const clearNotifications = () => {
  const currentIds = activeNotifications.value.map(n => n.id);
  hiddenNotifIds.value = [...hiddenNotifIds.value, ...currentIds];

  if (!authStore.isManager) {
    absenceStore.absences.forEach(a => {
      if (a.status !== 'En attente') a.viewed = true;
    })
  }
}

const handleNotifClick = (notif) => {
  if (notif.route) {
    router.push(notif.route)
  }
}

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
  if (!isLanding.value) {
    await authStore.fetchCurrentUser()
    if (employeeStore.employees.length === 0) await employeeStore.fetchEmployees()

    if (authStore.isManager) {
      if (scheduleStore.shifts.length === 0) await scheduleStore.fetchWeeklyShifts()
      if (absenceStore.absences.length === 0) await absenceStore.fetchAbsences()
    } else {
      if (scheduleStore.shifts.length === 0) await scheduleStore.fetchMyShifts()
      if (absenceStore.absences.length === 0) await absenceStore.fetchMyAbsences()
    }
  }
})

watch(isLanding, async (newVal) => {
  if (!newVal && !authStore.isAuthenticated) {
    await authStore.fetchCurrentUser()
  }
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