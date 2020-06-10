<template>
  <div class="home-container">
     <div class="second-header">
        <el-row type="flex" class="row-bg">
              <el-col :span="2"><el-button type="info" plain>大系统</el-button></el-col>
              <el-col :span="2"><el-button type="info" plain>小系统</el-button></el-col>
              <el-col :span="2"><el-button type="info" plain>冷却系统</el-button></el-col>
        </el-row>
      </div>
    <el-row :gutter="15">
        <el-col :span="24">
         首页面
         <br>
          首页面
         <br>
        </el-col>
    </el-row>
  </div>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "Home",
    data(){
      return {

      }
    },
    created(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {

    }
  }
</script>
<style>
 .second-header{
    background-color: skyblue;
    height: 57px;
    width:100%;
    background:rgba(52,56,62,1);
    border-radius:4px;
  }
.home-container{
  background-color: #1B1E27;
}
</style>
