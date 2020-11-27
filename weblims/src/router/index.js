import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/Login'
import Home from '@/components/Home'
import Board from '@/views/Board'
import SampleRegistration from '@/views/Sample/SampleRegistration'
import SampleTest from '@/views/Sample/SampleTest'
import ApplyTest from '@/views/Sample/ApplyTest'
import SampleCheck from '@/views/Sample/SampleCheck'
import ReportReview from '@/views/Sample/ReportReview'
import OutInBar from '@/views/OutIn/OutInBar'

import QualitycheckBoard from '@/views/QualityCheck/QualitycheckBoard'
import QualitycheckRecord from '@/views/QualityCheck/QualitycheckRecord'

import DestroyBoard from '@/views/Destroy/DestroyBoard'
import DestroyRequest from '@/views/Destroy/DestroyRequest'
import DestroyAudit from '@/views/Destroy/DestroyAudit'
import Destroylist from '@/views/Destroy/Destroylist'

import SampleBoard from '@/views/SampleManagement/SampleBoard'
import SampleReceiving from '@/views/SampleManagement/SampleReceiving'

import CategoryManage from '@/views/System/CategoryManage'
import DocumentManage from '@/views/System/DocumentManage'
import RightDistribute from '@/views/System/RightDistribute'
import RecordBar from '@/views/System/RecordBar'


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
      children:[
        {path:'/Board',component:Board},

        {path:'/OutInBar',component:OutInBar},
        // 样品
        {path:'/SampleRegistration',component:SampleRegistration},
        {path:'/ApplyTest',component:ApplyTest},
        {path:'/SampleTest',component:SampleTest},
        {path:'/SampleCheck',component:SampleCheck},
        {path:'/ReportReview',component:ReportReview},
        
        // 质检报告
        {path:'/QualitycheckBoard',component:QualitycheckBoard},
        {path:'/QualitycheckRecord',component:QualitycheckRecord},
        
        //销毁看板
        {path:'/DestroyBoard',component:DestroyBoard},
        {path:'/DestroyRequest',component:DestroyRequest},
        {path:'/DestroyAudit',component:DestroyAudit},
        {path:'/Destroylist',component:Destroylist},

        //留样
        {path:'/SampleReceiving',component:SampleReceiving},
        {path:'/SampleBoard',component:SampleBoard},
        
        //系统管理
        {path:'/CategoryManage',component:CategoryManage},
        {path:'/DocumentManage',component:DocumentManage},
        {path:'/RightDistribute',component:RightDistribute},
        {path:'/RecordBar',component:RecordBar},

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