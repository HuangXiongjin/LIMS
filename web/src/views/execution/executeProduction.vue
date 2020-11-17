<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16 marginRight">选择批计划，查看是否可安排生产，确认执行后将下发备料</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="execute" v-has="['计划执行']">确定执行</el-button>
          </el-form-item>
        </el-form>
        <el-form :inline="true">
          <el-form-item label="查询品名">
            <el-input v-model="BrandName" placeholder="请输入品名" size="small" @change="getPlanManagerTableData"></el-input>
          </el-form-item>
          <el-form-item label="查询批号">
            <el-input v-model="BatchID" placeholder="请输入批次号" size="small" @change="getPlanManagerTableData"></el-input>
          </el-form-item>
          <el-form-item label="查询日期">
            <el-date-picker type="date" v-model="searchDate" size="small" format="yyyy-MM-dd" value-format="yyyy-MM-dd" style="width: 160px;" @change="getPlanManagerTableData"></el-date-picker>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-radio-group v-model="PlanPlanStatus" size="small" @change="getPlanManagerTableData">
              <el-radio-button label="待执行"></el-radio-button>
              <el-radio-button label="待备料"></el-radio-button>
            </el-radio-group>
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
        BrandName:"",
        BatchID:"",
        searchDate:"",
        PlanPlanStatus:"待执行",
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
          PlanStatus:this.PlanPlanStatus,
          SchedulePlanCode:this.searchDate,
          BatchID:this.BatchID,
          BrandName:this.BrandName,
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
        if(this.PlanManagerTableData.multipleSelection.length > 0){
          var datalist = []
          this.PlanManagerTableData.multipleSelection.forEach(item =>{
            datalist.push(item.ID)
          })
          var params={
            PlanStatus:'待备料',
            IDs:JSON.stringify(datalist)
          }
          this.$confirm('是否下发勾选的批次, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.axios.post('/api/createZYPlanZYtask',this.qs.stringify(params)).then((res) => {
             if(res.data.code==='200'){
               this.$message({
                 type:'success',
                 message:'执行成功'
               })
              this.getPlanManagerTableData()
             }
           })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: '请选择要执行的计划'
          });
        }
      },
    }
  }
</script>

<style scoped>

</style>
