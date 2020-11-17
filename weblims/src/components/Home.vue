<template>
    <el-container>
        <el-aside width="255px" class="bggreen">
            <div class="project">实验室管理系统</div>
            <el-menu default-active="1-4-1" class="bggreen menuform" :collapse="isCollapse">
            <el-submenu index="1">
                <template slot="title">
                <i class="el-icon-location"></i>
                <span slot="title">导航一</span>
                </template>
                <el-menu-item index="1-2">选项2</el-menu-item>
                <el-menu-item index="1-2">选项2</el-menu-item>
                <el-menu-item index="1-2">选项2</el-menu-item>
                <el-menu-item index="1-2">选项2</el-menu-item>
            </el-submenu>
            <el-menu-item index="2">
                <i class="el-icon-menu"></i>
                <span slot="title">导航二</span>
            </el-menu-item>
            <el-menu-item index="3">
                <i class="el-icon-document"></i>
                <span slot="title">导航三</span>
            </el-menu-item>
            <el-menu-item index="4">
                <i class="el-icon-setting"></i>
                <span slot="title">导航四</span>
            </el-menu-item>
            </el-menu>
        </el-aside>
        <el-container>
            <el-header class="bggreen">
                <el-row>
                    <el-col :span='20'>&nbsp;</el-col>
                    <el-col :span='4' class="tools">
                        <ul>
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="全屏" placement="bottom">
                                    <i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
                                </el-tooltip>
                            </li>
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="个人信息" placement="bottom">
                                    <i class="el-icon-user" @click="getPersonInfo"></i>
                                </el-tooltip>
                            </li>
                            <li>
                                <el-tooltip class="head-menu-item cursor" effect="dark" content="退出登录" placement="bottom">
                                    <i class="el-icon-timer" @click="loginOut"></i>
                                </el-tooltip>
                            </li>
                        </ul>
                    </el-col>
                </el-row>
            </el-header>
            <el-main>Main</el-main>
        </el-container>
        <el-dialog title="个人信息" :visible.sync="persondialogTableVisible" width='400px' :modal=false>
            
        </el-dialog>
    </el-container>
</template>
<script>
import screenfull from "screenfull"
var moment = require('moment')
export default {
    data(){
        return {
             isCollapse: false,
             isFullScreen:false,
             persondialogTableVisible:false
        }
    },
    methods: {
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
          this.$router.push('/login')
      }
    },
}
</script>
<style scoped>
    .project{
        font-size: 20px;
        width:168px;
        height: 111px;
        line-height: 111px;
        text-align: center;
        margin:30px 50px 37px 37px;
        color: #fff;
        border-bottom: 1px solid #fff;
    }
    .menuform{
        height: 800px;
        padding-left: 28px;
    }
    .tools ul{
        margin: 0;
        padding: 0;
    }
    .tools ul li{
        list-style: none;
        width:40px;
        text-align: center;
        height:40px;
        line-height: 40px;
        margin: 10px 10px;
        float: left;
    }
    .head-menu-item{
        font-size:20px;
    }
</style>