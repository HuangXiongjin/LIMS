<template>
  <el-row>
    <el-col :span="24">
      <el-collapse class="marginBottom">
        <el-collapse-item title="多条件查询订单计划">
          <el-form :model="searchField" :inline="true" label-width="110px">
            <el-form-item label="计划开始时间">

            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="getZYPlanTable">查询</el-button>
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>
      <el-row :gutter="15">
        <el-col :span="24">
          <div class="platformContainer">
            工艺段计划
          </div>
          <div class="platformContainer">
            <el-table :data="ZYPlanTableData.data" border size="small">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PUName" label="工艺名称"></el-table-column>
              <el-table-column prop="PlanDate" label="计划日期"></el-table-column>
              <el-table-column prop="PlanNo" label="制药计划单号"></el-table-column>
              <el-table-column prop="ERPOrderNo" label="ERP订单号"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
              <el-table-column prop="ActQuantity" label="实际重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
              <el-table-column prop="PlanEndTime" label="计划结束时间"></el-table-column>
              <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
              <el-table-column prop="ActEndTime" label="实际完成时间"></el-table-column>
              <el-table-column prop="ZYPlanStatus" label="计划状态"></el-table-column>
            </el-table>
          </div>
          <div class="platformContainer">
            设备任务
          </div>
          <div class="platformContainer">
            <el-table :data="ZYTaskTableData.data" border size="small">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PUName" label="工艺名称"></el-table-column>
              <el-table-column prop="EQPName" label="设备名称"></el-table-column>
              <el-table-column prop="PlanDate" label="计划日期"></el-table-column>
              <el-table-column prop="TaskID" label="制药任务单号"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
              <el-table-column prop="ActQuantity" label="实际重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
              <el-table-column prop="PlanEndTime" label="计划结束时间"></el-table-column>
              <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
              <el-table-column prop="ActEndTime" label="实际完成时间"></el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"ProcessPlanTask",
    data(){
      return {
        searchField:{

        },
        ZYPlanTableData:{
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[]
        },
        ZYTaskTableData:{
          data:[],
          limit:5,
          offset:1,
          total:0,
          multipleSelection:[]
        },
      }
    },
    created(){

    },
    methods:{
      getZYPlanTable(){
        var that = this
        var params = {
          tableName: "ZYPlan",
          BatchID:this.BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ZYPlanTableData.data = data.rows
          }
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>

</style>
