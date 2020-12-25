<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <el-row :gutter='20'>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">系统运行天数</p>
            <p class="marginBottom color-darkblue">{{ runDays }} 天</p>
          </el-card>
        </el-col>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">共生产品种</p>
            <p class="marginBottom color-darkblue">{{ BrandNum }} 种</p>
          </el-card>
        </el-col>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">本月订单数</p>
            <p class="marginBottom color-darkblue">{{ planTableData.length }} 单</p>
          </el-card>
        </el-col>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">本月计划批数</p>
            <p class="marginBottom color-darkblue">{{ PlanBatchNum }} 批</p>
          </el-card>
        </el-col>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">共运输物料</p>
            <p class="marginBottom color-darkblue">{{ BucketNum }} 桶</p>
          </el-card>
        </el-col>
        <el-col :span='4'>
          <el-card class="marginBottom">
            <p class="marginBottom">已使用生产罐</p>
            <p class="marginBottom color-darkblue">{{ EqRunNum }} 罐</p>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter='20'>
        <el-col :span="18">
          <div class="cardContainerHead">设备运行统计</div>
          <div class="cardContainer">
            <ve-histogram :data="chartEqData" :extend="chartExtend"></ve-histogram>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="cardContainerHead">批计划状态饼图</div>
          <div class="cardContainer">
            <ve-ring :data="chartPlanData" :extend="chartPlanExtend"></ve-ring>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>
<script>
  import draggable from 'vuedraggable'
  var moment = require('moment');
  export default {
    name: "index",
    components:{draggable},
    data(){
      return {
        runDays:moment().diff(moment("2020-11-10"),'days'),
        BrandNum:0,
        planTableData:[],
        PlanBatchNum:0,
        BucketNum:0,
        EqRunNum:0,
        chartPlanExtend:{
          legend:{
            show:false
          },
          series:{
            radius:"50%",
            labelLine:{
              length:10,
              length2:10,
            }
          }
        },
        chartPlanData:{
          columns: ['状态', '批数'],
          rows: []
        },
        chartExtend:{
          'yAxis.0':{
            name: '次数',
          },
          series:{
            barMaxWidth: 50
          }
        },
        chartEqData:{
          columns: ['设备', '生产次数'],
          rows: []
        }
      }
    },
    created(){

    },
    mounted(){
      this.getPlanTableData()
      this.getBrandNum()
      this.getPlanNum()
      this.getBatchMaterialInfo()
      this.getZYTask()
    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      //获取订单计划表
      getPlanTableData(){
        var that = this
        var params = {
          tableName: "product_plan",
          CreateTimeTime:moment().format("YYYY-MM"),
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.planTableData = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getPlanNum(){
        var that = this
        var params = {
          tableName:"PlanManager",
          SchedulePlanCode:moment().format("YYYY-MM")
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if (res.data.code === "200") {
            that.PlanBatchNum = res.data.data.rows.length
          }
        })
      },
      getBrandNum(){
        var that = this
        var params = {
          tableName:"PlanManager"
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if (res.data.code === "200") {
            const objList = {}
            res.data.data.rows.forEach(item =>{
              if(objList[item.BrandName]){
                objList[item.BrandName]++
              }else{
                objList[item.BrandName] = 1
              }
            })
            var count = 0;
            for(var i in objList){
              if(objList.hasOwnProperty(i)){
                count++
              }
            }
            that.BrandNum = count
            //统计状态
            var PlanStatus1 = 0
            var PlanStatus2 = 0
            var PlanStatus3 = 0
            var PlanStatus4 = 0
            var PlanStatus5 = 0
            var PlanStatus6 = 0
            var PlanStatus7 = 0
            var PlanStatus8 = 0
            res.data.data.rows.forEach(item =>{
              if(item.PlanStatus === "待审核"){
                PlanStatus1 = PlanStatus1 + 1
              }
              if(item.PlanStatus === "审核未通过"){
                PlanStatus2 = PlanStatus2 + 1
              }
              if(item.PlanStatus === "待下发"){
                PlanStatus3 = PlanStatus3 + 1
              }
              if(item.PlanStatus === "待执行"){
                PlanStatus4 = PlanStatus4 + 1
              }
              if(item.PlanStatus === "撤回"){
                PlanStatus5 = PlanStatus5 + 1
              }
              if(item.PlanStatus === "待备料"){
                PlanStatus6 = PlanStatus6 + 1
              }
              if(item.PlanStatus === "物料发送中"){
                PlanStatus7 = PlanStatus7 + 1
              }
              if(item.PlanStatus === "物料发送完成"){
                PlanStatus8 = PlanStatus8 + 1
              }
            })
            that.chartPlanData.rows = [
              {"状态":"待审核","批数":PlanStatus1},
              {"状态":"审核未通过","批数":PlanStatus2},
              {"状态":"待下发","批数":PlanStatus3},
              {"状态":"待执行","批数":PlanStatus4},
              {"状态":"撤回","批数":PlanStatus5},
              {"状态":"待备料","批数":PlanStatus6},
              {"状态":"发送物料中","批数":PlanStatus7},
              {"状态":"发送物料完成","批数":PlanStatus8},
            ]
          }
        })
      },
      getBatchMaterialInfo(){
        var that = this
        var params = {
          tableName:"BatchMaterialInfo",
          SendFlag:"投料系统已接收",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if (res.data.code === "200") {
            that.BucketNum = 0
            res.data.data.rows.forEach(item =>{
              if(Array.isArray(item.BucketNum.split(","))){
                that.BucketNum += item.BucketNum.split(",").length
              }
            })
          }
        })
      },
      getZYTask(){
        var that = this
        var params = {
          tableName:"ZYTask",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if (res.data.code === "200") {
            const objList = {}
            res.data.data.rows.forEach(item =>{
              if(objList[item.EQPName]){
                objList[item.EQPName]++
              }else{
                objList[item.EQPName] = 1
              }
            })
            that.EqRunNum = 0
            for(var key in objList){
              that.EqRunNum++
              this.chartEqData.rows.push({
                "设备":key,
                "生产次数":objList[key],
              })
            }
          }
        })
      },
    }
  }
</script>
<style scoped>

</style>
