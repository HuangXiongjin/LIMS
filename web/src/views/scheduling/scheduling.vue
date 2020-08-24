<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step @click.native="clickStep(0)" class="cursor-pointer" title="生产计划"></el-step>
        <el-step @click.native="clickStep(1)" class="cursor-pointer" title="产能定义"></el-step>
        <el-step @click.native="clickStep(2)" class="cursor-pointer" title="其他日程"></el-step>
        <el-step @click.native="clickStep(3)" class="cursor-pointer" title="日计划排产"></el-step>
      </el-steps>
      <InformationEntry v-if="steps == 0"></InformationEntry>
      <ConfigPlan v-if="steps == 1"></ConfigPlan>
      <ScheduleManagement v-if="steps == 2"></ScheduleManagement>
      <CalendarScheduling v-if="steps == 3"></CalendarScheduling>
    </el-col>
  </el-row>
</template>

<script>
  import InformationEntry from '@/views/scheduling/InformationEntry'
  import ConfigPlan from '@/views/scheduling/ConfigPlan'
  import ScheduleManagement from '@/views/scheduling/ScheduleManagement'
  import CalendarScheduling from '@/views/scheduling/CalendarScheduling'
  export default {
    name: "scheduling",
    components:{
      InformationEntry,ConfigPlan,ScheduleManagement,CalendarScheduling
    },
    data(){
      return{
        steps:0
      }
    },
    mounted(){

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
