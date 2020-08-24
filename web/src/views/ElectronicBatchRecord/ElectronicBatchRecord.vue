<template>
  <el-row>
    <el-col :span="24">
<<<<<<< HEAD
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">电子批记录</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
      </div>
=======
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step @click.native="clickStep(0)" class="cursor-pointer" title="备料"></el-step>
        <el-step @click.native="clickStep(1)" class="cursor-pointer" title="煎煮"></el-step>
        <el-step @click.native="clickStep(2)" class="cursor-pointer" title="浓缩"></el-step>
      </el-steps>
>>>>>>> c7c9a2154f8743553118f8a4290b87b0c0de957f
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"ElectronicBatchRecord",
    data(){
      return {
        steps:0,
      }
    },
    created(){

    },
    methods:{
      clickStep(index){
        this.steps = index
      }
    }
  }
</script>

<style scoped>

</style>
