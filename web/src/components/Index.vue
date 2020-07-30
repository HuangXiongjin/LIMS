<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="220px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head blackComponents" v-if="!menuIsCollapse">
            <el-select v-model="systemActive" placeholder="请选择" @change="selectSystem">
              <el-option v-for="(item,index) in systemOptions" :key="index" :label="item.label" :value="item.label">
              </el-option>
            </el-select>
          </div>
          <div class="aside-head blackComponents" v-if="menuIsCollapse">
            <el-dropdown trigger="click" @command="selectSystem">
              <span class="el-dropdown-link">
                <i class="el-icon-arrow-down"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="(item,index) in systemOptions" :key="index" :command="item.label">{{ item.label }}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
          <div class="aside-main-nav">
            <el-row :gutter="10">
              <el-col :span="24">
                <el-col :span="8" v-for="(item,index) in mainMenu" :key="index" v-if="!menuIsCollapse">
                  <div class="main-nav-block" :class="{active:index===mainMenuActive}" @click="selectMainNav(index,item.url)" :title="item.title">
                    <p class="text-size-20"><i :class="item.icon"></i></p>
                    <p class="text-size-12">{{ item.title }}</p>
                  </div>
                </el-col>
                <el-col :span="24" v-for="(item,index) in mainMenu" :key="index" v-if="menuIsCollapse">
                  <div class="main-nav-block" :class="{active:index===mainMenuActive}" @click="selectMainNav(index,item.url)" :title="item.title">
                    <p class="text-size-20"><i :class="item.icon"></i></p>
                  </div>
                </el-col>
              </el-col>
            </el-row>
          </div>
          <div class="aside-foot">
            <el-button :icon="sideIcon" size="mini" circle @click="iconToggle"></el-button>
          </div>
        </el-col>
      </el-row>
    </el-aside>
    <!-- 右侧部分 -->
    <el-container>
      <!-- 头部 -->
      <el-header>
        <div class="head-menu floatLeft">
          <ul>
            <li></li>
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
                  {{ this.$store.state.UserName }}<i class="el-icon-arrow-down el-icon--right text-size-12"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">个人信息</el-dropdown-item>
                  <el-dropdown-item command="b" style="text-align: center"><i class="fa fa-power-off"></i></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
          </ul>
        </div>
      </el-header>
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
          {title:"设备管理",icon:"el-icon-box"},
          {title:"维修管理",icon:"el-icon-location-outline"},
          {title:"保养管理",icon:"el-icon-goods"},
          {title:"巡检管理",icon:"el-icon-goods"},
          {title:"备件管理",icon:"el-icon-setting"},
          {title:"统计分析",icon:"el-icon-setting"},
          ]},
        {label: '系统管理',mainMenu:[
          {title:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
          {title:"角色管理",icon:"el-icon-s-check",url:"/Role"},
          {title:"班组管理",icon:"el-icon-receiving",url:"/TeamGroup"},
          {title:"人员管理",icon:"el-icon-user",url:"/Personnel"},
          {title:"权限维护",icon:"el-icon-lock",url:"/Permission"},
          {title:"系统日志",icon:"el-icon-notebook-1",url:"/Log"}
          ]},
      ],
      AreaArr:[
        {title:"提取二车间"},{title:"综合车间"},{title:"新建综合制剂"}
      ],
      mainMenuActive:0,
      mainMenu:[],
      defaultActiveUrl:"",
      dialogUserVisible:false, //是否弹出个人信息
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
      this.axios.get("/api/CUID",{
        params: {
          tableName: "User",
          field:"WorkNumber",
          fieldvalue:sessionStorage.getItem('WorkNumber'),
          limit:1,
          offset:0
        }
      }).then(res =>{
        var data = JSON.parse(res.data)
        this.UserInfo =  data.rows[0]
      })
    }else{
      this.$router.push("/login");
    }
    this.selectSystem(this.systemActive) //默认切换第一个系统
  },
  destroyed() {

  },
  methods:{
    getMenuHeight(){
      if(this.menuIsCollapse){
        this.selfHeight.height = window.innerHeight - 490+'px';
      }else{
        this.selfHeight.height = window.innerHeight - 360+'px';
      }
    },
    selectSystem(a){ //切换系统
      this.systemOptions.forEach(item =>{
        if(item.label === a){
          this.mainMenu = item.mainMenu
        }
      })
    },
    selectMainNav(index,url){  //系统内菜单导航跳转
      this.mainMenuActive = index
      if(url){
        this.$router.replace({
          path:url,
          query: {time:moment()}
        })
      }
    },
    handleCommand(command) {  //判断用户下拉点击
      if(command === "a"){
        this.dialogUserVisible = true
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
  .el-container,.el-aside,.el-aside .el-row,.el-aside .el-row .el-col{
    position: relative;
    height: 100%;
  }
  .el-header{
    overflow: hidden;
  }
  .body-container{
    background: rgba(30,34,43,1);
  }
  .left-aside{
    background: rgba(30,34,43,1);
    box-shadow:5px 0px 7px rgba(255,255,255,0.16);
  }
  .aside-head{
    width: 100%;
    text-align: center;
    padding: 20px;
  }
  .aside-head a{
    color: #fff;
  }
  .aside-main-nav{
    border-top: 2px solid rgba(88,91,98,0.48);
    border-bottom: 2px solid rgba(88,91,98,0.48);
    padding: 20px 0;
    color: #fff;
    text-align: center;
    clear: both;
    overflow: hidden;
  }
  .main-nav-block{
    display: block;
    padding: 10px 0;
    border-radius:4px;
    cursor: pointer;
  }
  .main-nav-block.active{
    background: #00FAE7;
    color: #585B62;
  }
  .aside-foot{
    position: absolute;
    bottom: 0;
    height:110px;
    width: 100%;
    text-align: center;
    font-size: 18px;
    padding-top: 20px;
  }
  .head-menu{
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .head-menu li{
    display: inline-block;
    margin-right: 15px;
    color: #ffffff;
    font-size: 20px;
    text-decoration: none;
    padding: 8px 15px;
    cursor: pointer;
  }
  .head-menu-item{
    color: #ffffff;
    font-size: 18px;
    cursor:pointer;
  }
</style>
