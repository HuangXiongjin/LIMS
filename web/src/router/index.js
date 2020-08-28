import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import home from '@/views/home'
import switchSystem from '@/views/switchSystem'
import Login from '@/components/Login'
import Organization from '@/views/system/Organization'
import Role from '@/views/system/Role'
import TeamGroup from '@/views/system/TeamGroup'
import Personnel from '@/views/system/Personnel'
import Permission from '@/views/system/Permission'
import Log from '@/views/system/Log'
import flowGraph from '@/views/system/flowGraph'
import ProductDefinition from '@/views/ProductionModel/ProductDefinition'
import ProductSegmentDefinition from '@/views/ProductionModel/ProductSegmentDefinition'
import ProcessSectionDefinition from '@/views/ProductionModel/ProcessSectionDefinition'
import ProductSegmentConfiguration from '@/views/ProductionModel/ProductSegmentConfiguration'
import ProcessParameterConfiguration from '@/views/ProductionModel/ProcessParameterConfiguration'
import ProcessRoute from '@/views/ProductionModel/ProcessRoute'
import ProcessPlanTask from '@/views/dispatching/ProcessPlanTask'

import ProductionSchedule from '@/views/scheduling/ProductionSchedule'
import schedulingPlan from '@/views/scheduling/schedulingPlan'
import scheduling from '@/views/scheduling/scheduling'
import calendar from '@/views/scheduling/calendar'
import schedulingLog from '@/views/scheduling/schedulingLog'

import GeneratePlan from '@/views/dispatching/GeneratePlan'
import AuditPlan from '@/views/dispatching/AuditPlan'
import ImplementationPlan from '@/views/dispatching/ImplementationPlan'
import SendWMS from '@/views/dispatching/SendWMS'
import MaterialPreparation from '@/views/dispatching/MaterialPreparation'
import MaterialBalanceStatistics from '@/views/production/MaterialBalanceStatistics'
import MaterialTraceability from '@/views/production/MaterialTraceability'
import TrendQuery from '@/views/production/TrendQuery'

import MaterialInformation from '@/views/material/MaterialInformation'
import MaterialBOM from '@/views/material/MaterialBOM'
import ElectronicBatchRecord from '@/views/ElectronicBatchRecord/ElectronicBatchRecord'
import BatchRecordFiles from '@/views/ElectronicBatchRecord/BatchRecordFiles'

Vue.use(Router)
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      redirect:'/home', //index主页默认加载home页面
      children:[
        {path:'/home',name:'home',meta:{ title:'工作台'},component:home},
        {path:'/switchSystem',name:'switchSystem',meta:{ title:'系统切换',type:"系统管理"},component:switchSystem},
        {path:'/Organization',name:'Organization',meta:{ title:'组织架构',type:"系统管理"},component:Organization},
        {path:'/Role',name:'Role',meta:{ title:'角色管理',type:"系统管理"},component:Role},
        {path:'/TeamGroup',name:'TeamGroup',meta:{ title:'班组管理',type:"系统管理"},component:TeamGroup},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理',type:"系统管理"},component:Personnel},
        {path:'/Permission',name:'Permission',meta:{ title:'权限维护',type:"系统管理"},component:Permission},
        {path:'/Log',name:'Log',meta:{ title:'系统日志',type:"系统管理"},component:Log},
        {path:'/flowGraph',name:'flowGraph',meta:{ title:'流程图管理',type:"系统管理"},component:flowGraph},

        {path:'/ProductDefinition',name:'ProductDefinition',meta:{ title:'产品定义',type:"生产建模"},component:ProductDefinition},
        {path:'/ProductSegmentDefinition',name:'ProductSegmentDefinition',meta:{ title:'产品段定义',type:"生产建模"},component:ProductSegmentDefinition},
        {path:'/ProcessSectionDefinition',name:'ProcessSectionDefinition',meta:{ title:'工艺段定义',type:"生产建模"},component:ProcessSectionDefinition},
        {path:'/ProductSegmentConfiguration',name:'ProductSegmentConfiguration',meta:{ title:'产品段任务配置',type:"生产建模"},component:ProductSegmentConfiguration},
        {path:'/ProcessParameterConfiguration',name:'ProcessParameterConfiguration',meta:{ title:'工艺参数配置',type:"生产建模"},component:ProcessParameterConfiguration},
        {path:'/ProcessRoute',name:'ProcessRoute',meta:{ title:'工艺路线',type:"生产建模"},component:ProcessRoute},

        {path:'/ProcessPlanTask',name:'ProcessPlanTask',meta:{ title:'生产调度信息',type:"排产调度系统"},component:ProcessPlanTask},
        {path:'/GeneratePlan',name:'GeneratePlan',meta:{ title:'生成计划',type:"排产调度系统"},component:GeneratePlan},
        {path:'/AuditPlan',name:'AuditPlan',meta:{ title:'审核计划',type:"排产调度系统"},component:AuditPlan},
        {path:'/ImplementationPlan',name:'ImplementationPlan',meta:{ title:'执行计划',type:"排产调度系统"},component:ImplementationPlan},
        {path:'/SendWMS',name:'SendWMS',meta:{ title:'发送WMS',type:"排产调度系统"},component:SendWMS},
        {path:'/MaterialPreparation',name:'MaterialPreparation',meta:{ title:'物料调度管理',type:"排产调度系统"},component:MaterialPreparation},
        {path:'/ProductionSchedule',name:'ProductionSchedule',meta:{ title:'排产进度表',type:"排产调度系统"},component:ProductionSchedule},
        {path:'/schedulingPlan',name:'schedulingPlan',meta:{ title:'排产计划',type:"排产调度系统"},component:schedulingPlan},
        {path:'/scheduling',name:'scheduling',meta:{ title:'工厂排产',type:"排产调度系统"},component:scheduling},
        {path:'/calendar',name:'calendar',meta:{ title:'排期管理',type:"排产调度系统"},component:calendar},
        {path:'/schedulingLog',name:'schedulingLog',meta:{ title:'排产记录',type:"排产调度系统"},component:schedulingLog},

        {path:'/MaterialBalanceStatistics',name:'MaterialBalanceStatistics',meta:{ title:'物料平衡统计',type:"生产数据系统"},component:MaterialBalanceStatistics},
        {path:'/MaterialTraceability',name:'MaterialTraceability',meta:{ title:'物料追溯',type:"生产数据系统"},component:MaterialTraceability},
        {path:'/TrendQuery',name:'TrendQuery',meta:{ title:'生产数据趋势分析',type:"生产数据系统"},component:TrendQuery},

        {path:'/MaterialInformation',name:'MaterialInformation',meta:{ title:'物料信息',type:"物料系统"},component:MaterialInformation},
        {path:'/MaterialBOM',name:'MaterialBOM',meta:{ title:'物料清单',type:"物料系统"},component:MaterialBOM},

        {path:'/ElectronicBatchRecord',name:'ElectronicBatchRecord',meta:{ title:'批生产记录',type:"电子批记录"},component:ElectronicBatchRecord},
        {path:'/BatchRecordFiles',name:'BatchRecordFiles',meta:{ title:'批记录管理',type:"电子批记录"},component:BatchRecordFiles},



      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
