<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step @click.native="clickStep(0)" class="cursor-pointer" title="批次计划信息"></el-step>
        <el-step @click.native="clickStep(1)" class="cursor-pointer" title="产能定义"></el-step>
        <el-step @click.native="clickStep(2)" class="cursor-pointer" title="其他日程"></el-step>
        <el-step @click.native="clickStep(3)" class="cursor-pointer" title="日计划排产"></el-step>
      </el-steps>
      <el-row>
        <el-col :span="24" v-if="steps == 0">

        </el-col>
        <el-col :span="24" v-if="steps == 1">

        </el-col>
        <el-col :span="24" v-if="steps == 2">

        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "scheduling",
    components:{

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
