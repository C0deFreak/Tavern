import { createRouter, createWebHistory } from 'vue-router';
import MusicUpload from '@/components/Upload.vue';
import SingleMusic from '@/components/SingleMusic.vue';

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
    props: true, // Pass route params as props to the component
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
