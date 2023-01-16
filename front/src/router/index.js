import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignUp from "../views/SignUp.vue";
import SignIn from "../views/SignIn.vue";
import MyPage from "../views/MyPage.vue";
import Ranking from "../views/Ranking.vue";
import Notices from "../views/Notices.vue";
import SignUPOnlyRealName from "../views/SignUpOnlyRealName.vue";
import Question from "../components/Question.vue";
import QuestionView from "../components/QuestionView.vue";
import NotFoundComponent from "../components/NotFoundComponent.vue";
import ResolvedQuestion from "../components/ResolvedQuestion.vue";
import ResolvedQuestionView from "../components/ResolvedQuestionView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/signup",
    component: SignUp,
  },
  {
    path: "/signin",
    component: SignIn,
  },
  {
    path: "/create-question",
    component: Question,
  },
  {
    path: "/resolved-questions",
    component: ResolvedQuestion,
  },
  //動的に質問閲覧ページを表示する必要がある
  {
    path: "/question/:id",
    component: QuestionView,
    props: true,
    name: "question-detail",
  },
  {
    path: "/resolved-question/:id",
    component: ResolvedQuestionView,
    props: true,
    name: "resolved-question-detail",
  },
  {
    path: "/mypage",
    component: MyPage,
    props: true,
    name: "mypage",
  },
  {
    path: "/ranking",
    component: Ranking,
    name: "ranking",
  },
  {
    path: "/notices",
    component: Notices,
    name: "notices",
  },
  {
    path: "/signup-only-realname",
    component: SignUPOnlyRealName,
    name: "signup-only-realname",
  },
  {
    path: "*",
    component: NotFoundComponent,
    name: "notFound",
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: { name: "home" },
    meta: { isPublic: true },
  },
];

const router = new VueRouter({
  routes,
});

export default router;
