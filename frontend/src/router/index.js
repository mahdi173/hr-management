import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../components/DashboardView.vue";

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: DashboardView,
  },
//   {
//     path: "/plannings",
//     name: "Plannings",
//     component: () => import("../components/PlanningsView.vue"),
//   },
//   {
//     path: "/equipe",
//     name: "Equipe",
//     component: () => import("../components/EquipeView.vue"),
//   },
//   {
//     path: "/absences",
//     name: "Absences",
//     component: () => import("../components/AbsencesView.vue"),
//   },
//   {
//     path: "/parametres",
//     name: "Parametres",
//     component: () => import("../components/ParametresView.vue"),
//   },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
