import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import home from '@/views/home'
import switchSystem from '@/views/switchSystem'
import Login from '@/components/Login'
import Organization from '@/views/system/Organization'
import EnterpriseManagement from '@/views/system/EnterpriseManagement'
import FactoryManagement from '@/views/system/FactoryManagement'
import Role from '@/views/system/Role'
import TeamGroup from '@/views/system/TeamGroup'
import Personnel from '@/views/system/Personnel'
import Permission from '@/views/system/Permission'
import Log from '@/views/system/Log'
import flowGraph from '@/views/system/flowGraph'

//生产建模
import ProductDefinition from '@/views/ProductionModel/ProductDefinition'
import ProcessSectionDefinition from '@/views/ProductionModel/ProcessSectionDefinition'
import ProductSectionDefinition from '@/views/ProductionModel/ProductSectionDefinition'
import ProductParameter from '@/views/ProductionModel/ProductParameter'
import Area from '@/views/ProductionModel/Area'
import Equipment from '@/views/ProductionModel/Equipment'
import ProductLineDefinition from '@/views/ProductionModel/ProductLineDefinition'
import Unit from '@/views/ProductionModel/Unit'
//排产调度
import schedulingBoard from '@/views/scheduling/board'
import ProductionSchedule from '@/views/scheduling/ProductionSchedule'
import schedulingPlan from '@/views/scheduling/schedulingPlan'
import scheduling from '@/views/scheduling/scheduling'
import planningScheduling from '@/views/scheduling/planningScheduling'
import ProcessPlanTask from '@/views/scheduling/ProcessPlanTask'
//生产数据
import MaterialBalanceStatistics from '@/views/production/MaterialBalanceStatistics'
import MaterialTraceability from '@/views/production/MaterialTraceability'
import TrendQuery from '@/views/production/TrendQuery'
//物料管理
import MaterialInformation from '@/views/material/MaterialInformation'
import MaterialBOM from '@/views/material/MaterialBOM'
//批记录
import ElectronicBatchRecord from '@/views/ElectronicBatchRecord/ElectronicBatchRecord'
import BatchRecordFiles from '@/views/ElectronicBatchRecord/BatchRecordFiles'
//工厂监控
import ProductionMonitoring from '@/views/monitor/ProductionMonitoring'

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
        {path:'/EnterpriseManagement',name:'EnterpriseManagement',meta:{ title:'企业管理',type:"系统管理"},component:EnterpriseManagement},
        {path:'/FactoryManagement',name:'FactoryManagement',meta:{ title:'工厂管理',type:"系统管理"},component:FactoryManagement},
        {path:'/Role',name:'Role',meta:{ title:'角色管理',type:"系统管理"},component:Role},
        {path:'/TeamGroup',name:'TeamGroup',meta:{ title:'班组管理',type:"系统管理"},component:TeamGroup},
        {path:'/Personnel',name:'Personnel',meta:{ title:'人员管理',type:"系统管理"},component:Personnel},
        {path:'/Permission',name:'Permission',meta:{ title:'权限维护',type:"系统管理"},component:Permission},
        {path:'/Log',name:'Log',meta:{ title:'系统日志',type:"系统管理"},component:Log},
        {path:'/flowGraph',name:'flowGraph',meta:{ title:'流程图管理',type:"系统管理"},component:flowGraph},

        {path:'/ProductDefinition',name:'ProductDefinition',meta:{ title:'产品定义',type:"生产建模"},component:ProductDefinition},
        {path:'/ProcessSectionDefinition',name:'ProcessSectionDefinition',meta:{ title:'工艺段定义',type:"生产建模"},component:ProcessSectionDefinition},
        {path:'/ProductSectionDefinition',name:'ProductSectionDefinition',meta:{ title:'产品定义工艺段',type:"生产建模"},component:ProductSectionDefinition},
        {path:'/ProductParameter',name:'ProductParameter',meta:{ title:'产品工艺段参数',type:"生产建模"},component:ProductParameter},
        {path:'/Area',name:'Area',meta:{ title:'区域(车间)定义',type:"生产建模"},component:Area},
        {path:'/Equipment',name:'Equipment',meta:{ title:'生产设备定义',type:"生产建模"},component:Equipment},
        {path:'/ProductLineDefinition',name:'ProductLineDefinition',meta:{ title:'生产线定义',type:"生产建模"},component:ProductLineDefinition},
        {path:'/Unit',name:'Unit',meta:{ title:'生产线定义',type:"生产建模"},component:Unit},

        {path:'/schedulingBoard',name:'schedulingBoard',meta:{ title:'排产看板',type:"排产调度系统"},component:schedulingBoard},
        {path:'/ProductionSchedule',name:'ProductionSchedule',meta:{ title:'排期进度',type:"排产调度系统"},component:ProductionSchedule},
        {path:'/scheduling',name:'scheduling',meta:{ title:'工厂排产',type:"排产调度系统"},component:scheduling},
        {path:'/planningScheduling',name:'planningScheduling',meta:{ title:'生产调度',type:"排产调度系统"},component:planningScheduling},
        {path:'/ProcessPlanTask',name:'ProcessPlanTask',meta:{ title:'调度明细',type:"排产调度系统"},component:ProcessPlanTask},
        {path:'/schedulingPlan',name:'schedulingPlan',meta:{ title:'排产计划',type:"排产调度系统"},component:schedulingPlan},

        {path:'/MaterialBalanceStatistics',name:'MaterialBalanceStatistics',meta:{ title:'物料平衡统计',type:"生产数据系统"},component:MaterialBalanceStatistics},
        {path:'/MaterialTraceability',name:'MaterialTraceability',meta:{ title:'物料追溯',type:"生产数据系统"},component:MaterialTraceability},
        {path:'/TrendQuery',name:'TrendQuery',meta:{ title:'生产数据趋势分析',type:"生产数据系统"},component:TrendQuery},

        {path:'/MaterialInformation',name:'MaterialInformation',meta:{ title:'物料信息',type:"物料系统"},component:MaterialInformation},
        {path:'/MaterialBOM',name:'MaterialBOM',meta:{ title:'物料清单',type:"物料系统"},component:MaterialBOM},

        {path:'/ElectronicBatchRecord',name:'ElectronicBatchRecord',meta:{ title:'批生产记录',type:"电子批记录"},component:ElectronicBatchRecord},
        {path:'/BatchRecordFiles',name:'BatchRecordFiles',meta:{ title:'批记录管理',type:"电子批记录"},component:BatchRecordFiles},

        {path:'/ProductionMonitoring',name:'ProductionMonitoring',meta:{ title:'生产监控',type:"工厂监控"},component:ProductionMonitoring},

      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
