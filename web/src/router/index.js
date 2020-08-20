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
import MaterialBalanceStatistics from '@/views/production/MaterialBalanceStatistics'
import MaterialTraceability from '@/views/production/MaterialTraceability'
import DeviceInformation from '@/views/Device/DeviceInformation'
import EquipmentpartsManage from '@/views/Device/EquipmentpartsManage'
import InstrumentDataManagement from '@/views/Device/InstrumentDataManagement'
import InstrumentMaintenanceManagement from '@/views/Device/InstrumentMaintenanceManagement'
import EquipmentFailureManagement from '@/views/Device/EquipmentFailureManagement'
import EquipmentOperationRecord from '@/views/Device/EquipmentOperationRecord'
import MaterialInformation from '@/views/material/MaterialInformation'
import MaterialBOM from '@/views/material/MaterialBOM'
import ElectronicBatchRecord from '@/views/ElectronicBatchRecord/ElectronicBatchRecord'

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
        {path:'/MaterialBOM',name:'MaterialBOM',meta:{ title:'工艺参数配置',type:"生产建模"},component:MaterialBOM},
        {path:'/ProcessRoute',name:'ProcessRoute',meta:{ title:'工艺路线',type:"生产建模"},component:ProcessRoute},

        {path:'/ProductPlan',name:'ProductPlan',meta:{ title:'生产计划',type:"调度系统"},component:ProductPlan},
        {path:'/ProductProcessPlan',name:'ProductProcessPlan',meta:{ title:'工艺段生产计划',type:"调度系统"},component:ProductProcessPlan},
        {path:'/ProcessPlanTask',name:'ProcessPlanTask',meta:{ title:'工艺段计划任务',type:"调度系统"},component:ProcessPlanTask},
        {path:'/GeneratePlan',name:'GeneratePlan',meta:{ title:'生成计划',type:"调度系统"},component:GeneratePlan},
        {path:'/AuditPlan',name:'AuditPlan',meta:{ title:'审核计划',type:"调度系统"},component:AuditPlan},
        {path:'/ImplementationPlan',name:'ImplementationPlan',meta:{ title:'执行计划',type:"调度系统"},component:ImplementationPlan},
        {path:'/SendWMS',name:'SendWMS',meta:{ title:'发送WMS',type:"调度系统"},component:SendWMS},
        {path:'/MaterialPreparation',name:'MaterialPreparation',meta:{ title:'备料',type:"调度系统"},component:MaterialPreparation},

        {path:'/SchedulePreview',name:'SchedulePreview',meta:{ title:'排期预览',type:"排产系统"},component:SchedulePreview},
        {path:'/InformationEntry',name:'InformationEntry',meta:{ title:'物料信息录入',type:"排产系统"},component:InformationEntry},
        {path:'/ConfigPlan',name:'ConfigPlan',meta:{ title:'排产配置',type:"排产系统"},component:ConfigPlan},
        {path:'/ScheduleManagement',name:'ScheduleManagement',meta:{ title:'日程管理',type:"排产系统"},component:ScheduleManagement},
        {path:'/CalendarScheduling',name:'CalendarScheduling',meta:{ title:'日历排产',type:"排产系统"},component:CalendarScheduling},
        {path:'/PlannedMaintenance',name:'PlannedMaintenance',meta:{ title:'计划维护',type:"排产系统"},component:PlannedMaintenance},
        {path:'/PlanningReport',name:'PlanningReport',meta:{ title:'计划报表',type:"排产系统"},component:PlanningReport},

        {path:'/MaterialBalanceStatistics',name:'MaterialBalanceStatistics',meta:{ title:'物料平衡统计',type:"生产数据系统"},component:MaterialBalanceStatistics},
        {path:'/MaterialTraceability',name:'MaterialTraceability',meta:{ title:'物料追溯',type:"生产数据系统"},component:MaterialTraceability},
        
        {path:'/MaterialInformation',name:'MaterialInformation',meta:{ title:'物料信息',type:"物料系统"},component:MaterialInformation},
        {path:'/MaterialBOM',name:'MaterialBOM',meta:{ title:'物料清单',type:"物料系统"},component:MaterialBOM},

        {path:'/ElectronicBatchRecord',name:'ElectronicBatchRecord',meta:{ title:'电子批记录',type:"电子批记录"},component:ElectronicBatchRecord},
        
        {path:'/DeviceInformation',name:'DeviceInformation',meta:{ title:'设备信息',type:"设备管理"},component:DeviceInformation},
        {path:'/EquipmentpartsManage',name:'EquipmentpartsManage',meta:{ title:'设备备件管理',type:"设备管理"},component:EquipmentpartsManage},
        {path:'/InstrumentDataManagement',name:'InstrumentDataManagement',meta:{ title:'仪表仪器数据管理',type:"设备管理"},component:InstrumentDataManagement},
        {path:'/InstrumentMaintenanceManagement',name:'InstrumentMaintenanceManagement',meta:{ title:'仪表仪器检修管理',type:"设备管理"},component:InstrumentMaintenanceManagement},
        {path:'/EquipmentFailureManagement',name:'EquipmentFailureManagement',meta:{ title:'设备故障管理',type:"设备管理"},component:EquipmentFailureManagement},
        {path:'/EquipmentOperationRecord',name:'EquipmentOperationRecord',meta:{ title:'设备运行记录',type:"设备管理"},component:EquipmentOperationRecord},


      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ]
})
