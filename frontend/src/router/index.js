import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "../components/LandingPage.vue";
import DashboardView from "../components/DashboardView.vue";
import LoginPage from "../components/LoginPage.vue";

const routes = [
  {
    path: "/",
    name: "Landing",
    component: LandingPage,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
  },
  {
    path: "/plannings",
    name: "Plannings",
    component: () => import("../components/PlanningsView.vue"),
  },
  {
    path: "/equipe",
    name: "Equipe",
    component: () => import("../components/EquipeView.vue"),
  },
  {
    path: "/absences",
    name: "Absences",
    component: () => import("../components/AbsencesView.vue"),
  },
  {
    path: "/parametres",
    name: "Parametres",
    component: () => import("../components/ParametresView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: "smooth" };
    }
    return savedPosition || { top: 0 };
  },
});

export default router;
