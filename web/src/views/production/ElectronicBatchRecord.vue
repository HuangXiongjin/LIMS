<template>
  <el-row :gutter="15">
    <el-col :span='24'>
      <div class="page-title">
        <span class="text-size-16">选择批计划，展示工艺，点击查看批记录</span>
      </div>
    </el-col>
    <el-col :span='24' v-if="currentBatch">
      <div class="platformContainer">
        <div v-for="(item, index) in ZYPlanData" :key="index" style="display:inline-block;marginRight:18px;cursor:pointer" @click='ClickPU(item)'>
          <div class="container-col text-size-14 bg-gray" v-if="item.ZYPlanStatus === '待生产'">{{ item.PUName }}</div>
          <div class="container-col text-size-14 bg-success" v-if="item.ZYPlanStatus === '已完成'">{{ item.PUName }}</div>
          <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;" v-if="index != ZYPlanData.length -1"></i>
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
    <el-col :span='24' v-if="!currentBatch">
      <div>
        <el-button type="primary" @click="backTab" icon="el-icon-d-arrow-left" size='small'>返回列表</el-button>
        <el-button type="primary" icon="el-icon-folder-opened" size='small'>保存</el-button>
        <div class="platformContainer marginTop">
          <table class="elementTable" cellspacing="1" cellpadding="0" border="0" v-html="filebyte"></table>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"ElectronicBatchRecord",
    data(){
      return {
        PlanManagerTableData:{
          data:[],
          limit: 10,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        ZYPlanData:[],
        currentBatch:true,//控制显示表格 boolen
        filebyte:"",
      }
    },
    created(){
      this.getPlanManagerTableData()
    },
    methods:{
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
          PlanStatus:"已下发",
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
      ClickPU(item){ //点击工艺展示电子批记录
        var params={
          PUCode:item.PUCode,
          BrandCode:item.BrandCode
        }
        this.axios.get('/api/batchmodelselect',{params:params}).then((res) => {
          if(res.data.code==='200'){
            this.currentBatch=false
            if(res.data.message.length!==0){
              this.filebyte=res.data.message[0].Parameter
              this.$nextTick(function () {
                $(".elementTable").find("td").each(function(){
                  if($(this).html() === ""){
                    $(this).html("<p>-</p>")
                  }
                })
                $(".elementTable").find("p").attr("contenteditable","true")
                $(".elementTable").find("tbody").css("display","inline-table")
              })
            }else{
              this.filebyte=''
            }
          }else{
             this.$message({
              type: 'error',
              message: '获取批记录文档失败'
            });
          }
        })
      },
      backTab(){ //返回上一级下发表格
        this.currentBatch=true
      }
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
