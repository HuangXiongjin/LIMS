import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/Login'
import Home from '@/components/Home'

import Board from '@/views/Board/Board'
import StatisticalAnalysis from '@/views/Board/StatisticalAnalysis'
import ProgressBoard from '@/views/Board/ProgressBoard'
import BatchProgress from '@/views/Board/BatchProgress'

import SampleRegistration from '@/views/Sample/SampleRegistration'
import SampleTest from '@/views/Sample/SampleTest'
import ApplyTest from '@/views/Sample/ApplyTest'
import SampleCheck from '@/views/Sample/SampleCheck'
import ReportReview from '@/views/Sample/ReportReview'

import DynamicManagement from '@/views/OutIn/DynamicManagement'
import InWarehouse from '@/views/OutIn/InWarehouse'
import OutWarehouse from '@/views/OutIn/OutWarehouse'
import ApplicationReview from '@/views/OutIn/ApplicationReview'


import ReceivingSample from '@/views/SampleTesting/ReceivingSample'
import SampleRD from '@/views/SampleTesting/SampleRD'
import ReceivingResult from '@/views/SampleTesting/ReceivingResult'
import SampleTopeople from '@/views/SampleTesting/SampleTopeople'
import SampleAccount from '@/views/SampleTesting/SampleAccount'

import QualitycheckBoard from '@/views/QualityCheck/QualitycheckBoard'
import QualitycheckRecord from '@/views/QualityCheck/QualitycheckRecord'
import CheckReport from '@/views/QualityCheck/CheckReport'
import ReportExamination from '@/views/QualityCheck/ReportExamination'
import ReportExaminationed from '@/views/QualityCheck/ReportExaminationed'
import MakeReport from '@/views/QualityCheck/MakeReport'
import ReportExaminationedSend from '@/views/QualityCheck/ReportExaminationedSend'

import DestroyBoard from '@/views/Destroy/DestroyBoard'
import DestroyRequest from '@/views/Destroy/DestroyRequest'
import DestroyAudit from '@/views/Destroy/DestroyAudit'
import Destroylist from '@/views/Destroy/Destroylist'

import ReagentManagement from '@/views/Reagent/ReagentManagement'

import SampleBoard from '@/views/SampleManagement/SampleBoard'
import SampleReceiving from '@/views/SampleManagement/SampleReceiving'
import LySampleRecord from '@/views/SampleManagement/LySampleRecord'

import CategoryManage from '@/views/System/CategoryManage'
import DocumentManage from '@/views/System/DocumentManage'
import RightDistribute from '@/views/System/RightDistribute'
import RecordBar from '@/views/System/RecordBar'
import SystemLog from '@/views/System/SystemLog'


const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(Router)

const router=new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/',
      name: 'home',
      component:Home,
      redirect:'/ProgressBoard',
      children:[
        {path:'/Board',component:Board},
        {path:'/StatisticalAnalysis',component:StatisticalAnalysis},
        {path:'/ProgressBoard',component:ProgressBoard},
        {path:'/BatchProgress',component:BatchProgress},

        {path:'/DynamicManagement',component:DynamicManagement},
        {path:'/InWarehouse',component:InWarehouse},
        {path:'/OutWarehouse',component:OutWarehouse},
        {path:'/ApplicationReview',component:ApplicationReview},
        // 样品
        {path:'/SampleRegistration',component:SampleRegistration},
        {path:'/ApplyTest',component:ApplyTest},
        {path:'/SampleList',component:SampleTest},
        {path:'/SampleCheck',component:SampleCheck},
        {path:'/ReportReview',component:ReportReview},
        
        {path:'/ReceivingSample',component:ReceivingSample},
        {path:'/SampleRD',component:SampleRD},
        {path:'/ReceivingResult',component:ReceivingResult},
        {path:'/SampleTopeople',component:SampleTopeople},
        {path:'/SampleAccount',component:SampleAccount},
        
        // 质检报告
        {path:'/QualitycheckBoard',component:QualitycheckBoard},
        {path:'/QualitycheckRecord',component:QualitycheckRecord},
        {path:'/CheckReport',component:CheckReport},
        {path:'/MakeReport',component:MakeReport},
        {path:'/ReportExamination',component:ReportExamination},
        {path:'/ReportExaminationed',component:ReportExaminationed},
        {path:'/ReportExaminationedSend',component:ReportExaminationedSend},
        
        //销毁看板
        {path:'/DestroyBoard',component:DestroyBoard},
        {path:'/DestroyRequest',component:DestroyRequest},
        {path:'/DestroyAudit',component:DestroyAudit},
        {path:'/Destroylist',component:Destroylist},
        
        //试剂管理
        {path:'/ReagentManagement',component:ReagentManagement},

        //留样
        {path:'/SampleReceiving',component:SampleReceiving},
        {path:'/LySampleRecord',component:LySampleRecord},
        {path:'/SampleBoard',component:SampleBoard},
        
        //系统管理
        {path:'/CategoryManage',component:CategoryManage},
        {path:'/DocumentManage',component:DocumentManage},
        {path:'/RightDistribute',component:RightDistribute},
        {path:'/RecordBar',component:RecordBar},
        {path:'/SystemLog',component:SystemLog},

      ]
    }
  ]
})

router.beforeEach((to,from,next)=>{
  if(to.path==='/login'){
    next()
    return;
  }else{
    var token=sessionStorage.getItem('WorkNumber')
    if(!token){
      next('/login')
    }else{
      next()
    }

  }
})

export default router