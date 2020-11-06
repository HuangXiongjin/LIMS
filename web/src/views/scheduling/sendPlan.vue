<template>
  <el-row>
    <el-col :span='24' class="marginBottom"><el-button type="primary" size="small" @click="back">返回主线程</el-button></el-col>
    <el-col :span="24">
      <el-row :gutter="15">
        <el-col :span="24">
          <div class="page-title">
            <span class="text-size-16">选择批计划，给WMS发送此计划的投料计划</span>
          </div>
          <div class="platformContainer">
            <el-form :inline="true">
              <el-form-item>
                <el-button type="primary" size="small" @click="sendPlan">发送投料计划</el-button>
              </el-form-item>
              <el-form-item class="floatRight">
                <el-radio-group v-model="sendPlanPlanStatus" size="small" @change="getPlanManagerTableData">
                  <el-radio-button label="待发送"></el-radio-button>
                  <el-radio-button label="已发送"></el-radio-button>
                </el-radio-group>
              </el-form-item>
            </el-form>
            <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
              <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="PlanManagerTableData.total"
               :current-page="PlanManagerTableData.offset"
               :page-sizes="[5,10,20]"
               :page-size="PlanManagerTableData.limit"
               @size-change="handleSizeChangePlanManager"
               @current-change="handleCurrentChangePlanManager">
              </el-pagination>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "sendWMS",
    data(){
      return{
        sendPlanPlanStatus:"待发送",
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      back(){ //返回上一步
        this.$router.push('/planProgress')
      },
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var PlanStatus = ""
        if(this.sendPlanPlanStatus === "待发送"){
          PlanStatus = "已下发"
        }else if(this.sendPlanPlanStatus === "已发送"){
          PlanStatus = "已发送投料计划"
        }
        var params = {
          tableName: "PlanManager",
          PlanStatus:PlanStatus,
          limit:this.PlanManagerTableData.limit,
          offset:this.PlanManagerTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.PlanManagerTableData.data = res.data.data.rows
            that.PlanManagerTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChangePlanManager(limit){ //每页条数切换
        this.PlanManagerTableData.limit = limit
        this.getPlanManagerTableData()
      },
      handleCurrentChangePlanManager(offset) { // 页码切换
        this.PlanManagerTableData.offset = offset
        this.getPlanManagerTableData()
      },
      handleSelectionChangePlanManager(row){
        this.PlanManagerTableData.multipleSelection = row
      },
      handleRowClickPlanManager(row){
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
      },
      //发送投料计划到WMS
      sendPlan(){
        if(this.PlanManagerTableData.multipleSelection.length == 1){
          var mulId = []
          mulId.push({id:this.PlanManagerTableData.multipleSelection[0].ID});
          var params = {}
          params.sendData = JSON.stringify(mulId)
          this.$confirm('确定发送此批的投料计划到WMS吗？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.post("/api/WMS_SendPlan",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "200"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
              }
              this.getPlanManagerTableData()
            },res =>{
              console.log("请求错误")
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消发送'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: "请选择一条计划"
          });
        }
      },
    }
  }
</script>

<style scoped>

</style>
