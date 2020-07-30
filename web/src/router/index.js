import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Home from '@/views/home'
import Login from '@/components/Login'
import Organization from '@/views/system/Organization'
import Role from '@/views/system/Role'
import TeamGroup from '@/views/system/TeamGroup'
import Personnel from '@/views/system/Personnel'
import Permission from '@/views/system/Permission'
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
        {path:'/TeamGroup',name:'TeamGroup',meta:{ title:'班组管理'},component:TeamGroup},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理'},component:Personnel},
        {path:'/Permission',name:'Permission',meta:{ title:'权限维护'},component:Permission},
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
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}
