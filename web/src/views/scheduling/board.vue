<template>
    <el-row>
        <el-col :span='24' class="marginBottom" style="fontSize:18px;fontWeight:700;">排产看板</el-col>
        <el-col :span='24'>
          <el-row :gutter='20'>
            <el-col :span='8'>
              <div class="platformContainer">
                <div class="marginBottom">需求完成情况</div>
                <el-row class="marginBottom-10">
                  <el-col :span='8' style="fontSize:14px;">ERP需求数量</el-col>
                  <el-col :span='6' style="fontSize:14px;">122,256</el-col>
                  <el-col :span='10' style="fontSize:14px;"><el-progress :percentage="ProgressConfig[0].percentage" :color="ProgressConfig[0].color"></el-progress></el-col>
                </el-row>
                <el-row class="marginBottom-10">
                  <el-col :span='8' style="fontSize:14px;">紧急插单数量</el-col>
                  <el-col :span='6' style="fontSize:14px;">13</el-col>
                  <el-col :span='10' style="fontSize:14px;"><el-progress :percentage="ProgressConfig[1].percentage" :color="ProgressConfig[1].color"></el-progress></el-col>
                </el-row>
                <el-row class="marginBottom-10">
                  <el-col :span='8' style="fontSize:14px;">计划完成率</el-col>
                  <el-col :span='6' style="fontSize:14px;">69.35%</el-col>
                  <el-col :span='10' style="fontSize:14px;"><el-progress :percentage="ProgressConfig[2].percentage" :color="ProgressConfig[2].color"></el-progress></el-col>
                </el-row>
              </div>
            </el-col>
            <el-col :span='8'>中</el-col>
            <el-col :span='8'>右</el-col>
          </el-row>
        </el-col>
    </el-row>
</template>

<script>
  export default {
    name: "board",
    data(){
      return {
        ProgressConfig:[{
            percentage:80,
            color:'#5cb87a'
        },{
          percentage:20,
          color:'#f56c6c'
        },{
            percentage:60,
            color:'#1989fa'
        },],

      }
    }
  }
</script>

<style scoped>

</style>
