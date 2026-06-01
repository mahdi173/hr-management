<template>
  <v-app :style="isLanding ? 'background: white' : 'background-color: #F9FAFB'">

    <!-- App shell: sidebar + topbar only for authenticated views -->
    <template v-if="!isLanding">
      <v-navigation-drawer v-model="drawer" border elevation="0" width="260" color="surface" app>
        <div class="pa-5 d-flex align-center">
          <AppLogo :icon-size="30" :font-size="17" :gap="8" />
        </div>

        <v-list class="px-4" nav>
          <v-list-item
            v-for="item in menuItems"
            :key="item.title"
            :prepend-icon="item.icon"
            :title="item.title"
            :to="item.path"
            active-color="primary"
            rounded="lg"
            class="mb-2 list-item-hover"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-app-bar border elevation="0" color="surface" height="72" app>
        <v-app-bar-nav-icon @click="drawer = !drawer" color="grey-darken-2" class="ml-2"></v-app-bar-nav-icon>

        <v-spacer></v-spacer>

        <v-text-field
          hide-details
          prepend-inner-icon="mdi-magnify"
          placeholder="Rechercher un employé, un planning..."
          variant="solo-filled"
          flat
          density="compact"
          class="mx-4"
          style="max-width: 350px;"
          bg-color="#F3F4F6"
          rounded="lg"
        ></v-text-field>

        <v-btn icon color="grey-darken-2" class="mr-3">
          <v-badge color="error" content="3" dot>
            <v-icon>mdi-bell-outline</v-icon>
          </v-badge>
        </v-btn>

        <v-avatar color="primary-lighten-4" size="40" class="mr-6 cursor-pointer hover-scale">
          <span class="text-primary font-weight-bold">LM</span>
        </v-avatar>
      </v-app-bar>
    </template>

    <v-main :class="isLanding ? 'pa-0' : ''">
      <div :class="isLanding ? '' : 'pa-6 pa-md-8 pt-4 pt-md-6'">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLogo from './components/AppLogo.vue'

const route = useRoute()
const isLanding = computed(() => route.name === 'Landing' || route.name === 'Login')

const drawer = ref(true)

const menuItems = ref([
  { title: 'Tableau de bord', icon: 'mdi-view-dashboard-outline', path: '/dashboard' },
  { title: 'Plannings', icon: 'mdi-calendar-month-outline', path: '/plannings' },
  { title: 'Équipe', icon: 'mdi-account-group-outline', path: '/equipe' },
  { title: 'Absences', icon: 'mdi-palm-tree', path: '/absences' },
  { title: 'Paramètres', icon: 'mdi-cog-outline', path: '/parametres' },
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
