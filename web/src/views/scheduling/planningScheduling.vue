<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="success" align-center class="marginBottom">
        <el-step title="审核计划"></el-step>
        <el-step title="工艺配置"></el-step>
        <el-step title="下发计划"></el-step>
        <el-step title="发送投料计划"></el-step>
      </el-steps>
    </el-col>
    <el-col :span="24" class="marginTop">
      <CheckscPlan v-show="steps===0"></CheckscPlan>
      <EquipmentChoose v-show="steps===1"></EquipmentChoose>
      <DistributionPlan v-show="steps===2"></DistributionPlan>
      <sendPlan v-show="steps===3"></sendPlan>
    </el-col>
    <el-col :span="24" style="textAlign:right">
      <el-button type="primary" v-show="steps != 0" @click="LastStep">上一步</el-button>
      <el-button type="primary" v-show="steps != 3" @click="NextStep">下一步</el-button>
    </el-col>
  </el-row>
</template>

<script>
import CheckscPlan from './CheckscPlan.vue'
import EquipmentChoose from './EquipmentChoose.vue'
import DistributionPlan from './DistributionPlan.vue'
import sendPlan from './sendPlan.vue'
  export default {
    name: "planningScheduling",
    data(){
      return{
          steps:0,

      }
    },
    components:{CheckscPlan,EquipmentChoose,DistributionPlan,sendPlan},
    created(){
     
    },
    methods:{
        NextStep(){
          this.steps++
        },
        LastStep(){
          this.steps--
        }
    }
  }
</script>

<style scoped>
  .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
</style>
