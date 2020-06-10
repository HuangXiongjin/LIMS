import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Home from '@/views/home'
import config from '@/components/config'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:'/home', //index主页默认加载home页面
      children:[{
        path:'/home',
        name:'home',
        meta:{ title:'工作台'},
        component:Home
      }]
    },
    {
      path: '/config',
      name: 'config',
      component: config,
    },
  ]
})
