<template>
  <el-row>
    <el-col :span='24'>
      <el-row :gutter='20'>
        <el-col :span='6'>
          <el-card class="marginBottom">
            <p class="marginBottom">本月订单数</p>
            <p class="color-darkblue">{{ planTableData.length }} 单</p>
          </el-card>
        </el-col>
        <el-col :span='6'>
          <el-card class="marginBottom">
            <p class="marginBottom">本月计划批数</p>
            <p class="color-darkblue">{{ PlanBatchNum }} 批</p>
          </el-card>
        </el-col>
        <el-col :span='6'>
          <el-card class="marginBottom">
            <p class="marginBottom">本月计划生产品种</p>
            <p class="color-darkblue">{{ BrandNum }} 种</p>
          </el-card>
        </el-col>
        <el-col :span='6'>
          <el-card class="marginBottom">
            <p class="marginBottom">待处理计划</p>
            <p class="color-darkblue">{{ PlanTableData.length }} 条</p>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter='20'>
        <el-col :span='16'>
          <div class="cardContainerHead">批计划状态瀑布图</div>
          <div class="cardContainer">
            <ve-waterfall :data="chartPlanData" :extend="chartPlanExtend" height="400px"></ve-waterfall>
          </div>
        </el-col>
        <el-col :span='8'>
          <div class="cardContainerHead">批计划待处理列表 <a href="javascript:;" class="floatRight text-size-14" @click="$router.push('/planningScheduling')">去调度</a></div>
          <div class="cardContainer">
            <el-table :data="PlanTableData" border size="small" height="400px">
              <el-table-column prop="PlanNum" label="编号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态">
                <template slot-scope="scope">
                  <span class="color-lightgreen" v-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "board",
    data(){
      return {
        planTableData:[],
        PlanBatchNum:"",
        BrandNum:"",
        chartPlanExtend:{
          grid: {
            top: 30,
            bottom:10
          },
          series:{
            barMaxWidth:50
          }
        },
        chartPlanData: {
          columns: ['状态', '批数'],
          rows: []
        },
        PlanTableData:[]
      }
    },
    mounted(){
      this.getPlanTableData()
      this.getPlanNum()
      this.searchPlan()
    },
    methods:{
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
          }
        })
      },
      searchPlan(){
        var that = this
        var params = {
          tableName:"PlanManager",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            var PlanStatus1 = 0
            var PlanStatus2 = 0
            var PlanStatus3 = 0
            var PlanStatus4 = 0
            var PlanStatus5 = 0
            var PlanStatus6 = 0
            var PlanStatus7 = 0
            var PlanStatus8 = 0
            var PlanStatus9 = 0
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
              if(item.PlanStatus === "已完成"){
                PlanStatus9 = PlanStatus9 + 1
              }
              if(item.PlanStatus === "待审核" || item.PlanStatus === "待下发"){
                that.PlanTableData.push(item)
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
              {"状态":"已完成","批数":PlanStatus9},
            ]
          }else{
            that.$message({
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
