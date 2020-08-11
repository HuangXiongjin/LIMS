<template>
  <el-container class="body-container">
    <!-- 头部 -->
    <el-header class="body-head">
      <div class="head-menu floatLeft">
        <router-link to='/home'><span class="color-black">希尔安智能管理系统</span></router-link>
      </div>
      <div class="head-menu floatLeft" style="margin-left: 50px;">
        <ul>
          <li class="mainMenuList" v-for="(item,index) in systemOptions" :key="index" @click="selectSystem(item.label)" v-bind:class="{active:item.label===systemActive}">{{ item.label }}</li>
        </ul>
      </div>
      <div class="head-menu floatRight">
        <ul>
          <li>
            <el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom">
              <i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
            </el-tooltip>
          </li>
          <li>
            <el-dropdown class="head-menu-item" trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                <i class="dotState bg-lightgreen"></i>{{ this.$store.state.UserName }}<i class="el-icon-arrow-down el-icon--right text-size-12"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">个人信息</el-dropdown-item>
                <el-dropdown-item command="b" style="text-align: center"><i class="fa fa-power-off"></i></el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-dialog title="用户信息" :visible.sync="dialogUserVisible" :append-to-body="true" width="50%">
              <el-form>
                <el-form-item label="用户名：">{{ userInfo.Name }}</el-form-item>
                <el-form-item label="工号：">{{ userInfo.WorkNumber }}</el-form-item>
                <el-form-item label="最近登录时间：">{{ userInfo.LastLoginTime }}</el-form-item>
                <el-form-item label="权限：">{{ userInfo.Permissions }}</el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogUserVisible = false">取 消</el-button>
              </span>
            </el-dialog>
          </li>
        </ul>
      </div>
    </el-header>
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="220px" class="left-aside">
        <el-row>
          <el-col :span="24">
            <div :style="selfHeight" class="aside-menu">
            <el-menu class="menu-ul" :default-active="defaultActiveUrl" :collapse="menuIsCollapse" :router="true" @select="menuSelect">
              <template v-for="item in mainMenu">
                <el-menu-item v-if="!item.children" :index="item.url"><i :class="item.icon"></i><span slot="title">{{ item.title }}</span></el-menu-item>
                <el-submenu v-if="item.children" :index="item.title">
                  <template slot="title"><i :class="item.icon"></i><span>{{ item.name }}</span></template>
                  <el-menu-item v-for="(child,childIndex) in item.children" :key="childIndex" :index="child.url" @click="clickSubMenu(child.title)"><span style="margin-left:10px;">{{child.name}}</span></el-menu-item>
                </el-submenu>
              </template>
            </el-menu>
          </div>
            <div class="aside-foot">
              <el-button :icon="sideIcon" size="mini" circle @click="iconToggle"></el-button>
            </div>
          </el-col>
        </el-row>
      </el-aside>
      <!-- 页面主体 -->
      <el-main style="clear: both;">
        <transition name="move" mode="out-in">
         <!--渲染子页面-->
          <router-view :key="$route.fullPath"></router-view>
       </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
var moment = require('moment');
import screenfull from "screenfull"
export default {
  name: 'Index',
  data () {
    return {
      selfHeight:{ //自适应高度
        height:''
      },
      menuIsCollapse: false, //左侧菜单栏是否缩进了
      sideIcon:'el-icon-arrow-left', //左侧菜单栏缩进点击切换图标
      systemActive:"设备管理",
      systemOptions:[
        {label: '设备管理',mainMenu:[
          {title:"设备管理",icon:"el-icon-box",url:""},
          ]},
        {label: '系统管理',mainMenu:[
          {title:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
          {title:"角色管理",icon:"el-icon-s-check",url:"/Role"},
          {title:"班组管理",icon:"el-icon-receiving",url:"/TeamGroup"},
          {title:"人员管理",icon:"el-icon-user",url:"/Personnel"},
          {title:"权限维护",icon:"el-icon-lock",url:"/Permission"},
          {title:"流程管理",icon:"el-icon-share",url:"/flowGraph"},
          {title:"系统日志",icon:"el-icon-notebook-1",url:"/Log"}
          ]},
        {label: '能耗管理',mainMenu:[
          {title:"希尔安厂区",icon:"el-icon-s-grid",url:"/Factory",name:'希尔安厂区',children:[{name:'综合车间',title:'综合车间',url:'/Factory?area=综合车间'},{name:'新建综合制剂楼',title:'新建综合制剂楼',url:'/Factory?area=新建综合制剂楼'}]},
          {title:"能效分析",icon:"el-icon-files",url:"/EnergyAnalysis"},
          {title:"综合报表",icon:"el-icon-tickets",url:"/ComprehensiveReport"},
          {title:"数据录入",icon:"el-icon-s-marketing",url:"DataRecord"},
          ]},
      ],
      mainMenuActive:0,
      mainMenu:[],
      defaultActiveUrl:"",
      dialogUserVisible:false, //是否弹出个人信息
      userInfo:{},
      isFullScreen:false, //是否全屏
      areaObj:{
        areaName:""
      },
    }
  },
  //依赖注入传值
  provide(){
    return{
      newAreaName:this.areaObj
    }
  },
  mounted(){

  },
  created(){
    window.addEventListener('resize', this.getMenuHeight);
    this.getMenuHeight()
    if(sessionStorage.getItem("LoginStatus")) {
      this.$store.commit('setUser',sessionStorage.getItem('WorkNumber'))
    }else{
      this.$router.push("/login");
    }
    this.selectSystem(this.systemActive) //默认切换第一个系统
  },
  destroyed() {

  },
  methods:{
    clickSubMenu(a){

    },
    getMenuHeight(){
      if(this.menuIsCollapse){
        this.selfHeight.height = window.innerHeight - 490+'px';
      }else{
        this.selfHeight.height = window.innerHeight - 360+'px';
      }
    },
    menuSelect(key,keyPath){  //点击菜单跳转时  添加query参数避免相同路由跳转时报错
      this.$router.push({
        query:moment()
      })
    },
    selectSystem(a){ //切换系统
      this.systemActive = a
      this.systemOptions.forEach(item =>{
        if(item.label === a){
          this.mainMenu = item.mainMenu
        }
      })
    },
    handleCommand(command) {  //判断用户下拉点击
      if(command === "a"){
        this.dialogUserVisible = true
        this.userInfo.LastLoginTime = sessionStorage.getItem('LastLoginTime')
        this.userInfo.WorkNumber = sessionStorage.getItem('WorkNumber')
        this.userInfo.Name = sessionStorage.getItem('UserName')
        this.userInfo.Permissions = JSON.parse(sessionStorage.getItem('Permissions')).join('，')
      }else if(command === "b"){
        this.$store.commit('removeUser')
        this.$router.replace("/login")
      }
    },
    iconToggle() {  //折叠菜单
      this.menuIsCollapse = !this.menuIsCollapse
      this.getMenuHeight()
      if(this.menuIsCollapse){
        this.sideIcon = 'el-icon-arrow-right'
        $(".left-aside").animate({"width":"64px"})
      }else{
        this.sideIcon = 'el-icon-arrow-left'
        $(".left-aside").animate({"width":"220px"})
      }
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
  }
}
</script>
<style>

</style>
