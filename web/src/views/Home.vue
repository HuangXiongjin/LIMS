<template>
  <el-row :gutter="15">
      <el-col :span="24">

      </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "Home",
    data(){
      return {
        navOptionsCurrent:1,
        navOptions:[
          {name:"大系统",value:1},
          {name:"小系统",value:2},
          {name:"冷却系统",value:3}
        ],
      }
    },
    created(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      showPage(index) {
        this.navOptionsCurrent = index
      }
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
