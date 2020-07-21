import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Home from '@/views/home'
import Login from '@/components/Login'
import Organization from '@/views/system/Organization'
import Role from '@/views/system/Role'
import Personnel from '@/views/system/Personnel'
import Calendar from '@/views/system/Calendar'
import Log from '@/views/system/Log'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:'/home', //index主页默认加载home页面
      children:[
        {path:'/home',name:'home',meta:{ title:'工作台'},component:Home},
        {path:'/Organization',name:'Organization',meta:{ title:'组织架构'},component:Organization},
        {path:'/Role',name:'Role',meta:{ title:'角色管理'},component:Role},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理'},component:Personnel},
        {path:'/Calendar',name:'Calendar',meta:{ title:'工作日历'},component:Calendar},
        {path:'/Log',name:'Log',meta:{ title:'系统日志'},component:Log},
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
