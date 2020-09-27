<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-18">发送物料信息到WMS</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-button type="primary" size="small" @click="sendToWMS">发送物料信息</el-button>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-radio-group v-model="radioGroup" size="small" @change="Selectstatus">
              <el-radio-button v-for="(item,index) in status" :label="item.name" :key="index"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="MATCode" label="物料编码"></el-table-column>
          <el-table-column prop="MATName" label="物料名称"></el-table-column>
          <el-table-column prop="MATType" label="物料类型"></el-table-column>
          <el-table-column prop="Desc" label="物料描述"></el-table-column>
          <el-table-column prop="SendFlag" label="发送WMS标识"></el-table-column>
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
</template>

<script>
  export default {
    name: "sendMaterialInfo",
    data(){
      return{
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        status:[
          {name:"待发送"},
          {name:"已发送"},
        ],
        radioGroup:"待发送"
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      //批次计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "Material",
          field:"SendFlag",
          fieldvalue:this.radioGroup,
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
      Selectstatus(){
        this.getPlanManagerTableData()
      },
      sendToWMS(){
        if(this.PlanManagerTableData.multipleSelection.length > 0){
          var mulId = []
          var params = {}
          this.PlanManagerTableData.multipleSelection.forEach(item =>{
            mulId.push({id:item.ID});
          })
          params.sendData = JSON.stringify(mulId)
          this.$confirm('确定发送所选计划的物料信息到WMS？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.post("/api/WMS_SendMatilInfo",this.qs.stringify(params)).then(res =>{
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
            message: "请选择计划"
          });
        }
      }
    }
  }
</script>

<style scoped>

</style>
