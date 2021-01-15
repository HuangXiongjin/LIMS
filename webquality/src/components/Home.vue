<template>
    <el-container>
      <el-container>
        <el-aside width="240px" class="bggreen">
            <div class="project cursor">希尔安质量管理系统</div>
            <el-menu class="bggreen menuform" text-color="#d4d4d4"  active-text-color="#323232" :style="conheight">
            <el-menu-item v-for="(item,index) in mneulist" :key='index' :index='index.toString()' @click="getSonMenuList(item,index)" :class="{'ActiveMenucss':index==ActiveMenu}">
                <i :class="item.icon" style="color:#ccc;"></i>
                <span slot="title">{{item.name}}</span>
            </el-menu-item>
            </el-menu>
        </el-aside>
        <el-container>
            <el-header class="bgwhite " style="paddingTop:20px;backgroundColor:#0A9168;">
                    <el-row>
                    <el-col :span='20' class="sonMenucss">
                        <el-menu  class="bgwhite selfradius" mode="horizontal"  :default-active="SonMenuIndex" active-text-color="#323232" text-color="#d4d4d4">
                            <el-menu-item  v-for="(item,index1) in SonMenuList" :key='index1' :index='index1.toString()' @click="getCurrentSonList(item,index1)" >{{item.name}}</el-menu-item>
                        </el-menu>
                    </el-col>
                    <el-col :span='4' class="tools" style="float:right;">
                        <ul style="height:100%;">
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="全屏" placement="bottom">
                                    <i :class="isFullScreen?'fa fa-compress':'fa fa-expand'" @click="getFullCreeen"></i>
                                </el-tooltip>
                            </li>
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="个人信息" placement="bottom">
                                    <i class="fa  fa-user" @click="getPersonInfo"></i>
                                </el-tooltip>
                            </li>
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="退出登录" placement="bottom">
                                    <i class="fa fa-power-off" @click="loginOut"></i>
                                </el-tooltip>
                            </li>
                        </ul>
                    </el-col>
                </el-row>
            </el-header>
            <el-main style="paddingTop:30px;">
                <router-view></router-view>
            </el-main>
        </el-container>
        <el-dialog title="个人信息" :visible.sync="persondialogTableVisible" width='320px' :modal=false>
             <el-form>
                <el-form-item label="登录名称：">{{ userInfo.Name }}</el-form-item>
                <el-form-item label="登录密码：">{{ userInfo.WorkNumber }}</el-form-item>
                <el-form-item label="登录时间：">{{ userInfo.LastLoginTime }}</el-form-item>
                <el-form-item label="拥有权限：">{{ userInfo.Permissions }}</el-form-item>
              </el-form>
        </el-dialog>
      </el-container>
      <el-footer style="textAlign:center;height:30px;lineHeight:30px;fontSize:12px;" class="bggreen">Copyright &copy;温兄昆川科技</el-footer>
    </el-container>
</template>
<script>
import screenfull from "screenfull"
var moment = require('moment')
export default {
    data(){
        return {
             MenuIndex:'0',
             SonMenuIndex:localStorage.getItem('SonMenuIndex'),
             isCollapse: false,
             isFullScreen:false,
             persondialogTableVisible:false,
             userInfo:{
                 Name:sessionStorage.getItem('Name'),
                 WorkNumber:sessionStorage.getItem('WorkNumber'),
                 LastLoginTime:sessionStorage.getItem('LastLoginTime'),
                 Permissions:JSON.parse(sessionStorage.getItem('Rights').replace(/'/g, '"'))
             },
             SonMenuList:JSON.parse(localStorage.getItem('sonMenu')),
             ActiveMenu:100,
             conheight:{
                height:''
            },
             mneulist:[
                 {name:'功能看板',icon:'el-icon-data-analysis',children:[
                    {name:'系统首页',path:'/Board'},
                    {name:'折线图',path:'/BatchProgress'}
                   
                 ]},
                 {name:'原料质量',icon:'el-icon-star-off',children:[
                    {name:'统计分析',path:'/StatisticalAnalysis'},
                    {name:'清单进度',path:'/ListProgress'},
                    {name:'检验详情',path:'/InspectionDetails'},

                 ]},
                 {name:'在制品质量',icon:'el-icon-s-claim',children:[
                    {name:'统计分析',path:'/ProgressStatisticalAnalysis'},
                    {name:'清单进度',path:'/ProgressListProgress'},
                    {name:'检验详情',path:'/ProgressInspectionDetails'},

                 ]},
                 {name:'成品质量',icon:'el-icon-star-on',children:[
                    {name:'统计分析',path:'/ProductStatisticalAnalysis'},
                    {name:'清单进度',path:'/ProductListProgress'},
                    {name:'检验详情',path:'/ProductInspectionDetails'},
                 ]},
                 {name:'退货管理',icon:'el-icon-s-home',children:[
                    {name:'统计分析',path:'/ReturnsStatisticalAnalysis'},
                    {name:'清单进度',path:'/ReturnsListProgress'},
                    {name:'检验详情',path:'/ReturnsInspectionDetails'},
                 ]},
                 {name:'系统管理',icon:'el-icon-setting',children:[
                     {name:'类目模板',path:'/CategoryManage'},
                     {name:'系统日志',path:'/SystemLog'},
                     {name:'记录模板',path:'/RecordBar'},
                     {name:'文档管理',path:'/DocumentManage'},
                     {name:'权限分配',path:'/RightDistribute'},
                 ]},
                ]
        }
    },
    created(){
        window.addEventListener('resize', this.getHeight);
        this.getHeight()
    },
    methods: {
        getHeight(){
          this.conheight.height=(window.innerHeight-160)+'px'
       },
        getCurrentSonList(obj,index){
            localStorage.setItem('SonMenuIndex',index)
            this.$nextTick(()=>{
               this.SonMenuIndex=localStorage.getItem('SonMenuIndex')
            })
            this.$router.push(obj.path)

        },
         getFullCreeen () {  //全屏
            if (screenfull.isEnabled) {
            screenfull.toggle()
            if(screenfull.isFullscreen){
                this.isFullScreen = false
            }else{
                this.isFullScreen = true
            }
            }
      },
      getPersonInfo(){
          this.persondialogTableVisible=true
      },
      loginOut(){
          sessionStorage.clear()
          this.$router.push('/login')
          localStorage.removeItem('sonMenu')
          localStorage.removeItem('SonMenuIndex')
      },
      getSonMenuList(obj,index){
          this.ActiveMenu=index
          if(obj.hasOwnProperty('children')){
              localStorage.setItem('sonMenu',JSON.stringify(obj.children))
              this.SonMenuList=JSON.parse(localStorage.getItem('sonMenu'))
              this.getCurrentSonList(this.SonMenuList[0],0)
          }else{
             this.$router.push(obj.path)
             this.SonMenuList=[]
          }
      }
    },
}
</script>
<style scoped>
    .project{
        font-size: 20px;
        width:200px;
        height: 48px;
        text-align: center;
        margin:30px 50px 37px 20px;
        color: #fff;
        border-bottom: 1px solid #fff;
    }
    .menuform{
        padding-left: 20px;
    }
    .tools ul{
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #fff;
        border-radius: 0 25px 0 0;
    }
    .tools ul li{
        list-style: none;
        width:40px;
        text-align: center;
        height:100%;
        line-height: 100%;
        margin: 20px 10px;
        float: left;
    }
    .head-menu-item{
        font-size:20px;
        color: #222;
    }
    .ActiveMenucss{
       background-color:#fff;
       border-radius: 30px 0 0 30px;
    }
    .menuform .el-menu-item:hover{
        background-color: #00FA9A;
        color:#fff!important;
    }
    .sonMenucss .el-menu-item:hover{
        border-radius: 25px 0 0 0;
    }
    .sonMenucss .el-menu.el-menu--horizontal {
        border-bottom: solid 0px #e6e6e6;
    }
</style>