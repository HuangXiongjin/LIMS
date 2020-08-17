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
import ProductDefinition from '@/views/ProductionModel/ProductDefinition'
import ProductSegmentDefinition from '@/views/ProductionModel/ProductSegmentDefinition'
import ProductSegmentConfiguration from '@/views/ProductionModel/ProductSegmentConfiguration'
import ProcessParameterConfiguration from '@/views/ProductionModel/ProcessParameterConfiguration'
import MaterialBOM from '@/views/ProductionModel/MaterialBOM'
import ProcessRoute from '@/views/ProductionModel/ProcessRoute'
import ProductPlan from '@/views/dispatching/ProductPlan'
import ProductProcessPlan from '@/views/dispatching/ProductProcessPlan'
import ProcessPlanTask from '@/views/dispatching/ProcessPlanTask'
import SchedulePreview from '@/views/scheduling/SchedulePreview'
import InformationEntry from '@/views/scheduling/InformationEntry'
import ConfigPlan from '@/views/scheduling/ConfigPlan'
import ScheduleManagement from '@/views/scheduling/ScheduleManagement'
import CalendarScheduling from '@/views/scheduling/CalendarScheduling'
import PlannedMaintenance from '@/views/scheduling/PlannedMaintenance'
import PlanningReport from '@/views/scheduling/PlanningReport'
import GeneratePlan from '@/views/dispatching/GeneratePlan'
import AuditPlan from '@/views/dispatching/AuditPlan'
import ImplementationPlan from '@/views/dispatching/ImplementationPlan'
import SendWMS from '@/views/dispatching/SendWMS'
import MaterialPreparation from '@/views/dispatching/MaterialPreparation'
import ElectronicBatchRecord from '@/views/production/ElectronicBatchRecord'
import MaterialBalanceStatistics from '@/views/production/MaterialBalanceStatistics'
import MaterialTraceability from '@/views/production/MaterialTraceability'

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
        {path:'/ProductDefinition',name:'ProductDefinition',meta:{ title:'产品定义'},component:ProductDefinition},
        {path:'/ProductSegmentDefinition',name:'ProductSegmentDefinition',meta:{ title:'产品段定义'},component:ProductSegmentDefinition},
        {path:'/ProductSegmentConfiguration',name:'ProductSegmentConfiguration',meta:{ title:'产品段任务配置'},component:ProductSegmentConfiguration},
        {path:'/ProcessParameterConfiguration',name:'ProcessParameterConfiguration',meta:{ title:'工艺参数配置'},component:ProcessParameterConfiguration},
        {path:'/MaterialBOM',name:'MaterialBOM',meta:{ title:'工艺参数配置'},component:MaterialBOM},
        {path:'/ProcessRoute',name:'ProcessRoute',meta:{ title:'工艺路线'},component:ProcessRoute},
        {path:'/ProductPlan',name:'ProductPlan',meta:{ title:'生产计划'},component:ProductPlan},
        {path:'/ProductProcessPlan',name:'ProductProcessPlan',meta:{ title:'生产计划'},component:ProductProcessPlan},
        {path:'/ProcessPlanTask',name:'ProcessPlanTask',meta:{ title:'生产计划'},component:ProcessPlanTask},
        {path:'/SchedulePreview',name:'SchedulePreview',meta:{ title:'排期预览'},component:SchedulePreview},
        {path:'/InformationEntry',name:'InformationEntry',meta:{ title:'物料信息录入'},component:InformationEntry},
        {path:'/ConfigPlan',name:'ConfigPlan',meta:{ title:'配置计划'},component:ConfigPlan},
        {path:'/ScheduleManagement',name:'ScheduleManagement',meta:{ title:'日程管理'},component:ScheduleManagement},
        {path:'/CalendarScheduling',name:'CalendarScheduling',meta:{ title:'日历排产'},component:CalendarScheduling},
        {path:'/PlannedMaintenance',name:'PlannedMaintenance',meta:{ title:'计划维护'},component:PlannedMaintenance},
        {path:'/PlanningReport',name:'PlanningReport',meta:{ title:'计划报表'},component:PlanningReport},
        {path:'/GeneratePlan',name:'GeneratePlan',meta:{ title:'生成计划'},component:GeneratePlan},
        {path:'/AuditPlan',name:'AuditPlan',meta:{ title:'审核计划'},component:AuditPlan},
        {path:'/ImplementationPlan',name:'ImplementationPlan',meta:{ title:'执行计划'},component:ImplementationPlan},
        {path:'/SendWMS',name:'SendWMS',meta:{ title:'发送WMS'},component:SendWMS},
        {path:'/MaterialPreparation',name:'MaterialPreparation',meta:{ title:'备料'},component:MaterialPreparation},
        {path:'/ElectronicBatchRecord',name:'ElectronicBatchRecord',meta:{ title:'电子批记录'},component:ElectronicBatchRecord},
        {path:'/MaterialBalanceStatistics',name:'MaterialBalanceStatistics',meta:{ title:'物料平衡统计'},component:MaterialBalanceStatistics},
        {path:'/MaterialTraceability',name:'MaterialTraceability',meta:{ title:'物料追溯'},component:MaterialTraceability},
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
