<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" align-center class="marginBottom">
        <el-step title="物料信息录入"></el-step>
        <el-step title="参数配置"></el-step>
        <el-step title="其他日程"></el-step>
        <el-step title="排产"></el-step>
      </el-steps>
      <InformationEntry v-if="steps == 0"></InformationEntry>
      <ConfigPlan v-if="steps == 1"></ConfigPlan>
      <ScheduleManagement v-if="steps == 2"></ScheduleManagement>
      <CalendarScheduling v-if="steps == 3"></CalendarScheduling>
      <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
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
      next() {
        if (this.steps++ >= 3){
          this.$router.push("/calendar")
        }
      }
    }
  }
</script>

<style scoped>

</style>
