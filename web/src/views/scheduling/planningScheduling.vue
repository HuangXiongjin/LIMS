<template>
  <el-row>
    <el-col :span="24">
      <div class="platformContainer">
        <div class="page-title">
          <span class="text-size-16">选择批计划，查看计划工艺进展</span>
        </div>
        <div style="display:inline-block;marginRight:18px;cursor:pointer" @click='shPlan'>
          <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待配置' || PlanManagerTableData.PlanStatus === '待下发' || PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">审核计划</div>
          <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
        </div>
        <div style="display:inline-block;marginRight:18px;cursor:pointer" @click='chooseEq'>
          <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待下发' || PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">工艺配置</div>
          <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
        </div>
        <div style="display:inline-block;marginRight:18px;cursor:pointer" @click='distributionPlan'>
          <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '已下发' || PlanManagerTableData.PlanStatus === '已发送投料计划' || PlanManagerTableData.PlanStatus === '已发送物料明细'}">下发计划</div>
          <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
        </div>
        <div style="display:inline-block;cursor:pointer" @click='sendWMS'>
          <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '已发送物料明细'}">发送到WMS</div>
        </div>
        <div v-for="(item, index) in ZYPlanData" :key="index" style="display:inline-block;marginRight:18px;cursor:pointer" @click='ClickPU(item)'>
          <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
          <div class="container-col text-size-14 bg-gray" v-if="item.ZYPlanStatus === '待生产'">{{ item.PUName }}</div>
          <div class="container-col text-size-14 bg-success" v-if="item.ZYPlanStatus === '已完成'">{{ item.PUName }}</div>
        </div>
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
    name: "planningScheduling",
    data(){
      return{
        PlanManagerTableData:{
          data:[],
          limit: 10,
          offset: 1,
          total: 0,
          multipleSelection: [],
          PlanStatus:""
        },
        ZYPlanData:[],
      }
    },
    created(){
      this.getPlanManagerTableData()
    },
    methods:{
      shPlan(){
        this.$router.push('/CheckscPlan')
      },
      chooseEq(){
        this.$router.push('/EquipmentChoose')
      },
      distributionPlan(){
        this.$router.push('/DistributionPlan')
      },
      sendWMS(){
        this.$router.push('/sendWMS')
      },
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
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
        this.getZYPlan()
      },
      getZYPlan(){
        var that = this
        var params = {
          tableName: "ZYPlan",
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
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
            that.ZYPlanData = res.data.data.rows.sort(compare('PlanSeq'))
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      ClickPU(item){
       
      },
    }
  }
</script>

<style scoped>
  .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border:1px solid #999;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
</style>
