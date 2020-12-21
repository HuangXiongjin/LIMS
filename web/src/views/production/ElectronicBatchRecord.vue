<template>
  <el-row :gutter="15">
    <el-col :span='24'>
      <div class="page-title">
        <span class="text-size-16">选择批计划，展示工艺，点击查看批记录</span>
      </div>
    </el-col>
    <el-col :span='24' v-if="currentBatch">
      <div class="platformContainer">
        <div v-for="(item, index) in ZYPlanData" :key="index" style="display: inline-block;margin-right:18px;vertical-align: top;" @click='ClickPU(item)'>
          <div style="display: inline-block; text-align: center;" v-if="item.PUName === '备料'">
            <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':PlanManagerTableData.data[0].PlanStatus === '待备料','bg-darkblue':PlanManagerTableData.data[0].PlanStatus === '物料发送中','bg-success':PlanManagerTableData.data[0].PlanStatus === '物料发送完成'}">
              {{ item.PUName }}
            </div>
          </div>
          <div style="display: inline-block; text-align: center;" v-else>
            <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':item.ZYPlanStatus === '待确认','bg-lightgreen':item.ZYPlanStatus === '待复核','bg-darkblue':item.ZYPlanStatus === '执行','bg-success':item.ZYPlanStatus === '已完成'}">
              {{ item.PUName }}
            </div>
          </div>
          <i class="fa fa-arrow-right" v-if="index != ZYPlanData.length -1" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
        </div>
        <el-form :inline="true">
          <el-form-item label="查询品名">
            <el-input v-model="PlanManagerTableData.BrandName" placeholder="请输入品名" size="small" @change="getPlanManagerTableData"></el-input>
          </el-form-item>
          <el-form-item label="查询批号">
            <el-input v-model="PlanManagerTableData.BatchID" placeholder="请输入批次号" size="small" @change="getPlanManagerTableData"></el-input>
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
    <el-col :span='24' v-if="!currentBatch">
      <div>
        <el-button @click="backTab" icon="el-icon-d-arrow-left" size='small'>返回列表</el-button>
        <el-button type="primary" @click="saveCellData" icon="el-icon-folder-opened" size='small'>保存</el-button>
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
          BatchID:"",
          BrandName:"",
        },
        ZYPlanData:[],
        currentBatch:true,//控制显示表格 boolen
        filebyte:"",
        BrandCode:"",
        BrandName:"",
        PUCode:"",
        BatchID:"",
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
          BatchID:this.PlanManagerTableData.BatchID,
          BrandName:this.PlanManagerTableData.BrandName,
          limit:this.PlanManagerTableData.limit,
          offset:this.PlanManagerTableData.offset - 1
        }
        this.axios.get("/api/PlanManagerSelect",{
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
        let that = this
        this.BrandCode = item.BrandCode
        this.BrandName = item.BrandName
        this.PUCode = item.PUCode
        this.BatchID = item.BatchID
        var params={
          PUCode:item.PUCode,
          BrandCode:item.BrandCode
        }
        this.axios.get('/api/batchmodelselect',{params:params}).then((res) => {
          if(res.data.code==='200'){
            this.currentBatch=false
            if(res.data.message.length!=0){
              this.filebyte=res.data.message[0].Parameter
              this.getBatchModelField()
              this.$nextTick(function () {
                $(".elementTable").find("td").each(function(){
                  if($(this).hasClass("isInput")){
                    if($(this).children("p").length == 1){ //判断单元格有几个p标签
                      $(this).find("p").attr("contenteditable","true")
                    }else if($(this).children("p").length == 0){
                      $(this).append("<p></p>")
                      $(this).find("p").attr("contenteditable","true")
                    }else{ //多个p标签的值合成一个
                      var html = ""
                      $(this).find("p").each(function(){
                       html += $(this).html()
                      })
                      $(this).html("")
                      $(this).append("<p></p>")
                      $(this).find("p").attr("contenteditable","true").html(html)

                    }
                  }else if($(this).attr("data-field") === "ProductName"){
                    $(this).html(that.BrandName)
                  }else if($(this).attr("data-field") === "BatchNo"){
                    $(this).html(that.BatchID)
                  }
                })
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
      // 获取录入保存的数据
      getBatchModelField(){
        var params = {
          BrandCode:this.BrandCode,
          PUCode:this.PUCode,
          BatchID:this.BatchID,
        }
        this.axios.get("/api/allUnitDataMutual",{
          params:params
        }).then(res =>{
          if(res.data.code === "200"){
            this.$nextTick(function () {
              for(let key  in res.data.data){
                $(".elementTable").find(".isInput").each(function(){
                  if($(this).attr("data-field") === key){
                    $(this).find("p").html(res.data.data[key])
                  }
                })
              }
              $(".elementTable").find("td input[type=checkbox]").each(function(){ //为复选框添加勾选
                if($(this).val() === "0"){
                  $(this).prop("checked",false)
                }else if($(this).val() === "1"){
                  $(this).prop("checked",true)
                }
              })
              $(".elementTable").find("td input[type=checkbox]").on("click",function(){ //为复选框添加点击事件
                if($(this).val() === "0"){
                  $(this).val("1")
                }else if($(this).val() === "1"){
                  $(this).val("0")
                }
              })
            })
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      //保存录入的数据
      saveCellData(){
        let that = this
        this.$confirm('是否保存当前批记录?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var params = {
            BrandCode:this.BrandCode,
            PUCode:this.PUCode,
            BatchID:this.BatchID,
          }
          this.$nextTick(function () {
            $(".elementTable").find(".isInput").each(function(){
              params[$(this).attr("data-field")] = $(this).find("p").html()
            })
            that.axios.post("/api/allUnitDataMutual",that.qs.stringify(params)).then(res =>{
              if(res.data.code === "200"){
                that.$message({
                  type: 'success',
                  message: res.data.message
                });
              }else{
                that.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
            },res =>{
              console.log("请求错误")
            })
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消保存'
          });
        });
      },
      backTab(){ //返回上一级下发表格
        this.currentBatch=true
      }
    }
  }
</script>

<style scoped>
   .container-col{
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
      cursor: pointer;
    }
</style>
