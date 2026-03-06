import { createRouter, createWebHistory } from "vue-router";
import JdMatchPage from "@/feature/jdmatch/pages/JdMatchPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: JdMatchPage,
    },
    {
      path: "/jdmatch/:jdMatchId",
      name: "jdmatch-report",
      component: () => import("@/feature/jdmatch/pages/JdMatchReportPage.vue"),
      props: true,
    },
  ],
});

export default router;
