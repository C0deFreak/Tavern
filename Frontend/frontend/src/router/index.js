import { createRouter, createWebHistory } from 'vue-router';
import MusicUpload from '@/components/Upload.vue';
import SingleMusic from '@/components/SingleMusic.vue';
import LoginComponent from '@/components/Login.vue';
import SignupComponent from '@/components/Signup.vue';

const routes = [
  {
    path: '/upload',
    name: 'MusicUpload',
    component: MusicUpload,
  },
  {
    path: '/music/:name_:id',
    name: 'SingleMusic',
    component: SingleMusic,
    props: true,
  },
  {
    path: '/login',
    name: 'LoginComponent',
    component: LoginComponent,
  },
  {
    path: '/sign-up',
    name: 'SignupComponent',
    component: SignupComponent,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
