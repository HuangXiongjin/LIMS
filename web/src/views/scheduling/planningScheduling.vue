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
      <CheckscPlan v-show="steps===0" ref="child1"></CheckscPlan>
      <EquipmentChoose v-show="steps===1" ref="child2"></EquipmentChoose>
      <DistributionPlan v-show="steps===2" ref="child3"></DistributionPlan>
      <sendPlan v-show="steps===3" ref="child4"></sendPlan>
    </el-col>
    <el-col :span="24" style="textAlign:right">
      <el-button type="primary" v-show="steps != 0" @click="LastStep">上一步</el-button>
      <el-button type="primary" v-show="steps != 4" @click="NextStep">下一步</el-button>
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
    mounted(){
     this.$refs.child1.getPlanManager()
    },
    methods:{
      NextStep(){
        this.steps++
        if(this.steps===1){
          this.$refs.child2.getConfigbatch() 
          this.$refs.child2.chConfigbatch() 
          this.$refs.child2.getSelectedEq()
        }else if(this.steps===2){
          this.$refs.child3.getSelectedEq()
          this.$refs.child3.getYxfBatch()
        }else if(this.steps===3){
          this.$refs.child4.getPlanManagerTableData()
        }else if(this.steps===4){
          this.$router.push('/planProgress')
        }
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
