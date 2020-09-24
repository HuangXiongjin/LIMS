<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-18">生产调度信息</span>
      </div>
      <el-row :gutter="15">
        <el-col :span="4">
          <div class="platformContainer">
            <el-form>
              <el-form-item label="选择品名">
                <el-select v-model="BrandName" filterable placeholder="输入关键字" @change="getProductPlan">
                  <el-option
                    v-for="item in BrandOptions"
                    :key="item.ID"
                    :label="item.BrandName"
                    :value="item.BrandName">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="选择订单计划">
                <el-select v-model="PlanNum" filterable placeholder="选择计划编号" @change="getPlanManagerTable">
                  <el-option
                    v-for="item in ProductPlanTableData"
                    :key="item.ID"
                    :label="item.PlanNum"
                    :value="item.PlanNum">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="选择批次号">
                <el-select v-model="BatchID" filterable placeholder="选择批次号" @change="getZYPlanTable">
                  <el-option
                    v-for="item in PlanManagerTableData"
                    :key="item.ID"
                    :label="item.BatchID"
                    :value="item.BatchID">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </el-col>
        <el-col :span="20">
          <div class="platformContainer">
            工艺段计划
          </div>
          <div class="platformContainer">
            <el-table :data="ZYPlanTableData.data" border size="small" @selection-change="handleSelectionZYPlanTable">
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
            <el-table :data="ZYTaskTableData.data" border size="small" @selection-change="handleSelectionZYTaskTable">
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
        BrandName:"",
        BrandOptions:[],
        PlanNum:"",
        ProductPlanTableData:[],
        BatchID:"",
        PlanManagerTableData:[],
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
      this.getBrandTable()
    },
    methods:{
      getBrandTable(){
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.BrandOptions = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getProductPlan(){
        var that = this
        var params = {
          tableName: "product_plan",
          field:"BrandName",
          fieldvalue:this.BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ProductPlanTableData = data.rows
          }
        },res =>{
          console.log("请求错误")
        })
      },
      getPlanManagerTable(){
        var that = this
        var params = {
          tableName: "PlanManager",
          field:"PlanNum",
          fieldvalue:this.PlanNum,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PlanManagerTableData = data.rows
          }
        },res =>{
          console.log("请求错误")
        })
      },
      getZYPlanTable(){
        var that = this
        var params = {
          tableName: "ZYPlan",
          field:"BatchID",
          fieldvalue:this.BatchID,
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
      handleSelectionZYPlanTable(row){
        this.ZYPlanTableData.multipleSelection = row
      },
      handleSelectionZYTaskTable(row){
        this.ZYTaskTableData.multipleSelection = row
      }
    }
  }
</script>

<style scoped>

</style>
