<template>
    <el-container>
      <el-container>
        <el-aside width="240px" class="bggreen">
            <div class="project cursor">实验室管理系统</div>
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
                    {name:'工艺看板',path:'/ProgressBoard'},
                    {name:'统计分析',path:'/StatisticalAnalysis'},
                    {name:'批次进度',path:'/BatchProgress'},
                 ]},
                 {name:'出入库管理',icon:'el-icon-folder-opened',children:[
                    {name:'动态管理',path:'/DynamicManagement'},
                    {name:'入库管理',path:'/InWarehouse'},
                    {name:'出库管理',path:'/OutWarehouse'},
                    {name:'申请审核',path:'/ApplicationReview'},

                 ]},
                 {name:'样本请验',icon:'el-icon-s-order',children:[
                    {name:'申请检验',path:'/ApplyTest'},
                    {name:'请检审核',path:'/SampleCheck'},
                    {name:'取样登记',path:'/SampleRegistration'},
                    {name:'请验清单',path:'/SampleList'},
                    {name:'报告复查',path:'/ReportReview'},
                ]},
                {name:'样本检验',icon:'el-icon-files',children:[
                    {name:'样本接收',path:'/ReceivingSample'},
                    {name:'样本及记录分发',path:'/SampleRD'},
                    {name:'检验接收',path:'/ReceivingResult'},
                    {name:'检验分发',path:'/SampleTopeople'},
                    {name:'样本台账',path:'/SampleAccount'},
                ]
                },
                 {name:'质检报告',icon:'el-icon-document',children:[
                    {name:'检验记录',path:'/QualitycheckRecord'},
                    {name:'结果审核',path:'/CheckReport'},
                    {name:'整合报告',path:'/MakeReport'},
                    {name:'报告初审',path:'/ReportExamination'},
                    {name:'报告复审',path:'/ReportExaminationed'},
                    {name:'报告发送',path:'/ReportExaminationedSend'},
                    {name:'质检看板',path:'/QualitycheckBoard'},
                 ]},
                 {name:'留样管理',icon:'el-icon-paperclip',children:[
                     {name:'留样接收',path:'/SampleReceiving'},
                     {name:'留样观察记录',path:'/LySampleRecord'},
                     {name:'留样看板',path:'/SampleBoard'},
                 ]},
                 {name:'销毁管理',icon:'el-icon-delete',children:[
                     {name:'销毁审核',path:'/DestroyRequest'},
                    //  {name:'销毁审核',path:'/DestroyAudit'},
                     {name:'销毁清单',path:'/Destroylist'},
                    //  {name:'销毁看板',path:'/DestroyBoard'},
                 ]},
                 {name:'试剂耗材',icon:'el-icon-toilet-paper',children:[
                     {name:'试剂管理',path:'/ReagentManagement'},

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
        width:150px;
        height: 61px;
        text-align: center;
        margin:30px 50px 37px 37px;
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