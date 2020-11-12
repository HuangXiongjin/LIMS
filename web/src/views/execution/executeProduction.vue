<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16 marginRight">选择批计划，查看是否可安排生产，确认执行后将下发备料</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="execute">确定执行</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" highlight-current-row border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
          <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="PlanStatus" label="计划状态">
            <template slot-scope="scope">
              <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'">{{ scope.row.PlanStatus }}</b>
              <b class="color-orange" v-else-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
              <b class="color-red" v-else-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
              <b class="color-lightgreen" v-else-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
              <b class="color-purple" v-else-if="scope.row.PlanStatus === '待执行'">{{ scope.row.PlanStatus }}</b>
              <b class="" v-else-if="scope.row.PlanStatus === '待备料'">{{ scope.row.PlanStatus }}</b>
              <b class="color-orange" v-else-if="scope.row.PlanStatus === '物料发送中'">{{ scope.row.PlanStatus }}</b>
              <b class="color-brown" v-else-if="scope.row.PlanStatus === '物料发送完成'">{{ scope.row.PlanStatus }}</b>
              <b class="color-success" v-else-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
              <b class="" v-else>{{ scope.row.PlanStatus }}</b>
            </template>
          </el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
           :total="PlanManagerTableData.total"
           :current-page="PlanManagerTableData.offset"
           :page-sizes="[10,20,30,50]"
           :page-size="PlanManagerTableData.limit"
           @size-change="handleSizeChangePlanManager"
           @current-change="handleCurrentChangePlanManager">
          </el-pagination>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "executeProduction",
    data(){
      return {
        PlanManagerTableData:{
          data:[],
          limit: 10,
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
      //批计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
          PlanStatus:"待执行",
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
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
      },
      execute(){

      },
    }
  }
</script>

<style scoped>

</style>
