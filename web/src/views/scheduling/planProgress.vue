<template>
   <el-row>
    <el-col :span="24">
      <div class="platformContainer">
        <div class="page-title">
          <span class="text-size-16">选择批计划，查看计划工艺进展</span>
        </div>
        <el-row>
          <el-col :span="24">
            <div style="display:inline-block;marginRight:18px;cursor:pointer">
              <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待配置' || PlanManagerTableData.PlanStatus === '待下发' || PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">审核计划</div>
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
            </div>
            <div style="display:inline-block;marginRight:18px;cursor:pointer">
              <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待下发' || PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">工艺配置</div>
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
            </div>
            <div style="display:inline-block;marginRight:18px;cursor:pointer">
              <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">下发计划</div>
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
            </div>
            <div style="display:inline-block;cursor:pointer">
              <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '已发送物料明细'}">发送投料计划</div>
            </div>
            <div v-for="(item, index) in ProcessSectionData" :key="index" style="display:inline-block;marginRight:18px;cursor:pointer">
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
              <div class="container-col text-size-14 bg-gray">{{ item.PUName }}</div>
            </div>
          </el-col>
        </el-row>
        <el-form :inline="true">
          <el-form-item label="查询状态">
            <el-select v-model="PlanManagerTableData.searchPlanStatus" placeholder="请选择" @change="getPlanManagerTableData">
              <el-option v-for="(item,index) in PlanManagerTableData.searchFormData" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
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
    name: "planProgress",
    data(){
      return {
        PlanManagerTableData:{
          data:[],
          limit: 10,
          offset: 1,
          total: 0,
          multipleSelection: [],
          PlanStatus:"",
          searchPlanStatus:"",
          searchFormData:[
            {label:"全部",value:""},
            {label:"待审核",value:"待审核"},
            {label:"待配置",value:"待配置"},
            {label:"待下发",value:"待下发"},
            {label:"已下发",value:"已下发"},
            {label:"已发送投料计划",value:"已发送投料计划"},
            {label:"已发送物料明细",value:"已发送物料明细"},
            {label:"已完成",value:"已完成"},
          ]
        },
        ProcessSectionData:[], //品名的工艺段
      }
    },
    created(){
      this.getPlanManagerTableData()
    },
    methods:{
      //批计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
          PlanStatus:this.PlanManagerTableData.searchPlanStatus,
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
        this.PlanManagerTableData.PlanStatus=row.PlanStatus
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.getProcessSection()
      },
      getProcessSection(){
        var that = this
        var params = {
          tableName: "ProductUnit",
          BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            function compare(property){
              return function(a,b){
                var value1 = a[property];
                var value2 = b[property];
                return value1 - value2;
              }
            }
            that.ProcessSectionData = res.data.data.rows.sort(compare('Seq'))
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
  .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
</style>
