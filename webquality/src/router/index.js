import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/Login'
import Home from '@/components/Home'
import Nopermission from '@/components/Nopermission'

import Board from '@/views/Board/Board'

//原料质量
import StatisticalAnalysis from '@/views/MaterialQuality/StatisticalAnalysis'
import ListProgress from '@/views/MaterialQuality/ListProgress'
import InspectionDetails from '@/views/MaterialQuality/InspectionDetails'

//过程质量
import ProgressStatisticalAnalysis from '@/views/ProgressQuality/ProgressStatisticalAnalysis'
import ProgressListProgress from '@/views/ProgressQuality/ProgressListProgress'
import ProgressInspectionDetails from '@/views/ProgressQuality/ProgressInspectionDetails'

//成品质量
import ProductStatisticalAnalysis from '@/views/FinishedProduct/ProductStatisticalAnalysis'
import ProductListProgress from '@/views/FinishedProduct/ProductListProgress'
import ProductInspectionDetails from '@/views/FinishedProduct/ProductInspectionDetails'

//退货管理
import ReturnsStatisticalAnalysis from '@/views/ReturnsManagement/ReturnsStatisticalAnalysis'
import ReturnsListProgress from '@/views/ReturnsManagement/ReturnsListProgress'
import ReturnsInspectionDetails from '@/views/ReturnsManagement/ReturnsInspectionDetails'

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
      redirect:'/Board',
      children:[
        {path:'/Board',component:Board},
         
        //原料质量
        {path:'/StatisticalAnalysis',component:StatisticalAnalysis},
        {path:'/ListProgress',component:ListProgress},
        {path:'/InspectionDetails',component:InspectionDetails},

        //过程质量
        {path:'/ProgressStatisticalAnalysis',component:ProgressStatisticalAnalysis},
        {path:'/ProgressListProgress',component:ProgressListProgress},
        {path:'/ProgressInspectionDetails',component:ProgressInspectionDetails},
        
        //成品质量
        {path:'/ProductStatisticalAnalysis',component:ProductStatisticalAnalysis},
        {path:'/ProductListProgress',component:ProductListProgress},
        {path:'/ProductInspectionDetails',component:ProductInspectionDetails},
        
        //退货管理
        {path:'/ReturnsInspectionDetails',component:ReturnsInspectionDetails},
        {path:'/ReturnsListProgress',component:ReturnsListProgress},
        {path:'/ReturnsStatisticalAnalysis',component:ReturnsStatisticalAnalysis},
        
        //系统管理
        {path:'/CategoryManage',component:CategoryManage},
        {path:'/DocumentManage',component:DocumentManage},
        {path:'/RightDistribute',component:RightDistribute},
        {path:'/RecordBar',component:RecordBar},
        {path:'/SystemLog',component:SystemLog},

        //404页面
        {path: '/Nopermission',name: 'Nopermissionn',component: Nopermission},
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