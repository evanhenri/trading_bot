import Vue from 'vue';
import Router from 'vue-router';

import Dashboard from '@/components/Dashboard';
import Login from '@/components/Login';
import Settings from '@/components/Settings';

import BasicRoute from '@/components/BasicRoute';
import BasicRouteFirstChild from '@/components/BasicRouteFirstChild';
import BasicRouteSecondChild from '@/components/BasicRouteSecondChild';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings,
    },
    {
      path: '/basicroute/:name',
      name: 'BasicRoute',
      component: BasicRoute,
      children: [
        {
          path: 'firstchild',
          name: 'BasicRouteFirstChild',
          component: BasicRouteFirstChild,
        },
        {
          path: 'secondchild/:childName',
          name: 'BasicRouteSecondChild',
          component: BasicRouteSecondChild,
        },
      ],
    },
  ],
});
