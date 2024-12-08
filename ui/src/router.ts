import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
  type RouteLocationNamedRaw,
} from 'vue-router';
import { usePageStore } from './core/page-store';

export const Route = {
  HOME: 'MAIN',
  SEARCH_RESULTS: 'SEARCH_RESULTS',
  ADMIN: 'ADMIN',
};

const makeRoute = (
  name: string,
  path: string,
  component: () => Promise<unknown>,
): RouteRecordRaw => {
  return { path, name, component };
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/BlankLayout.vue'),
      children: [
        { path: '', redirect: { name: Route.HOME } },
        makeRoute(Route.HOME, 'home', () => import('@/classifier/views/LandingPage.vue')),
        makeRoute(
          Route.SEARCH_RESULTS,
          'search',
          () => import('@/classifier/views/SearchResultsPage.vue'),
        ),
        makeRoute(
          Route.ADMIN,
          'admin',
          () => import('@/classifier/views/AdminPage.vue'),
        ),
      ],
    },
  ],
});

router.beforeEach(() => {
  const store = usePageStore();
  store.isLoading = true;
});

router.afterEach(() => {
  const store = usePageStore();
  store.isLoading = false;
});

export const linkFactory = {
  toHome: () => ({ name: Route.HOME }),
  toAdmin: () => ({ name: Route.ADMIN }),
  toSearchResults: (query?: string) =>
    ({
      name: Route.SEARCH_RESULTS,
      ...(query ? { query: { q: query } } : {}),
    } satisfies RouteLocationNamedRaw),
};

export default router;
