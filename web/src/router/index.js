import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import home from '@/views/home'
import Login from '@/components/Login'
import Organization from '@/views/system/Organization'
import Role from '@/views/system/Role'
import TeamGroup from '@/views/system/TeamGroup'
import Personnel from '@/views/system/Personnel'
import Permission from '@/views/system/Permission'
import Log from '@/views/system/Log'
import flowGraph from '@/views/system/flowGraph'
import Factory from '@/views/energy/Factory'
import EnergyAnalysis from '@/views/energy/EnergyAnalysis'
import ComprehensiveReport from '@/views/energy/ComprehensiveReport'
import DataRecord from '@/views/energy/DataRecord'
import BrandMaintain from '@/views/ProductionModel/BrandMaintain'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:'/home', //index主页默认加载home页面
      children:[
        {path:'/home',name:'home',meta:{ title:'工作台'},component:home},
        {path:'/Organization',name:'Organization',meta:{ title:'组织架构'},component:Organization},
        {path:'/Role',name:'Role',meta:{ title:'角色管理'},component:Role},
        {path:'/TeamGroup',name:'TeamGroup',meta:{ title:'班组管理'},component:TeamGroup},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理'},component:Personnel},
        {path:'/Permission',name:'Permission',meta:{ title:'权限维护'},component:Permission},
        {path:'/Log',name:'Log',meta:{ title:'系统日志'},component:Log},
        {path:'/flowGraph',name:'flowGraph',meta:{ title:'流程图管理'},component:flowGraph},
        {path:'/Factory',name:'Factory',meta:{ title:'希尔安厂区'},component:Factory},
        {path:'/EnergyAnalysis',name:'EnergyAnalysis',meta:{ title:'能效分析'},component:EnergyAnalysis},
        {path:'/ComprehensiveReport',name:'ComprehensiveReport',meta:{ title:'综合报表'},component:ComprehensiveReport},
        {path:'/DataRecord',name:'DataRecord',meta:{ title:'数据录入'},component:DataRecord},
        {path:'/BrandMaintain',name:'BrandMaintain',meta:{ title:'数据录入'},component:BrandMaintain},
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
