import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionPage from '../views/QuestionPage.vue'
import ScorePage from '../views/ScorePage.vue'
import Admin from '../views/Admin.vue'
import QuestionAdminDisplay from '../views/QuestionAdminDisplay.vue'
import QuestionEdition from '../views/QuestionEdition.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/start-new-quiz-page',
      name: 'NewQuizPage',
      component: NewQuizPage
    },
    {
      path: '/questions',
      name: 'QuestionPage',
      component: QuestionPage
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: ScorePage
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin
    },
    {
      path: '/adminQuestion/:position',
      name: 'QuestionAdminDisplay',
      component: QuestionAdminDisplay
    },
    {
      path: '/questionEdition/:position?',
      name: 'QuestionEdition',
      component: QuestionEdition
    }
  ]
})

export default router
