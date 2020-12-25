<template>
  <el-row>
    <el-col :span='24' class="platformContainer">批次设备运行统计</el-col>
    <el-col :span='24' class="platformContainer">
      <div>
          <el-tag class="marginBottom marginRight cursor-pointer" v-bind:effect="''===PUCode?'dark':'plain'" @click="getTask('')">全部</el-tag>
          <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in ProcessData" :key="index" v-bind:effect="item.PUCode===PUCode?'dark':'plain'" @click="getTask(item.PUCode)">{{item.PUName}}</el-tag>
      </div>
      <ve-histogram :data="chartData" :extend="chartExtend"></ve-histogram>
    </el-col>
  </el-row>
</template>
<script>
var moment=require("moment")
export default {
  data(){
    return {
      PUCode:"",
      ProcessData:[],
      chartExtend:{
        'yAxis.0':{
          name: '次数',
        },
        series:{
          barMaxWidth: 50
        }
      },
      chartData:{
        columns: ['设备', '生产次数'],
        rows:[]
      }
    }
  },
  mounted(){
    this.getPUName()
  },
  methods:{
    //获取工艺段
    getPUName(){
      var params={
        tableName:'ProcessUnit',
      }
      this.axios.get('/api/CUID',{params:params}).then((res) => {
        var arr=res.data.data.rows
        this.ProcessData = arr
        this.PUCode = this.ProcessData[0].PUCode
      })
    },
    //获取task
    getTask(PUCode){
      this.PUCode = PUCode
      this.chartData.rows = []
      var params={
        tableName:'ZYTask',
        PUCode:PUCode,
      }
      this.axios.get("/api/CUID",{params: params}).then(res => {
        if(res.data.code === "200"){
          const objList = {}
          res.data.data.rows.forEach(item =>{
            if(objList[item.EQPName]){
              objList[item.EQPName]++
            }else{
              objList[item.EQPName] = 1
            }
          })
          for(var key in objList){
            this.chartData.rows.push({
              "设备":key,
              "生产次数":objList[key],
            })
          }
        }else{
          this.$message({
            type: 'info',
            message: res.data.message
          });
        }
      })
    },
  }
}
</script>
<style scoped>

</style>
