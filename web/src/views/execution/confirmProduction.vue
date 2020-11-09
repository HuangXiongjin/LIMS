<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16 marginRight">审核批次使用设备</span>
        <span class="sideState bg-gray"></span><span class="text-size-14">待生产</span>
        <span class="sideState bg-lightgreen"></span><span class="text-size-14">设备已审核</span>
        <span class="sideState bg-darkblue"></span><span class="text-size-14">设备已复核</span>
        <span class="sideState bg-success"></span><span class="text-size-14">已完成</span>
      </div>
      <div class="platformContainer">
        <el-row class="marginBottom">
          <el-col :span="24">
            <div v-for="(item, index) in ZYPlanTableData.data" :key="index" style="display: inline-block;margin-right:18px;vertical-align: top;">
              <div style="display: inline-block; text-align: center;">
                <div class="container-col text-size-14 bg-white" :class="{'bg-gray':item.ZYPlanStatus === '待生产','bg-lightgreen':item.ZYPlanStatus === '设备已审核','bg-darkblue':item.ZYPlanStatus === '设备已复核','bg-success':item.ZYPlanStatus === '已完成'}">{{ item.PUName }}</div>
                <div class="text-center" style="display: inherit;" v-show="item.PUName != '备料'">
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '设备已审核' || item.ZYPlanStatus === '设备已复核' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '设备已审核' || item.ZYPlanStatus === '设备已复核' ? 'dark':'plain'" @click="PUPlan(item,'审核')">审核</el-tag>
                  </p>
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '设备已复核' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '设备已复核' ? 'dark':'plain'" @click="PUPlan(item,'复核')">复核</el-tag>
                  </p>
                </div>
              </div>
              <i class="fa fa-arrow-right" v-if="index != ZYPlanTableData.data.length -1" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
            </div>
          </el-col>
        </el-row>
        <el-form :inline="true">
          <el-form-item>
            <el-radio-group v-model="sendPlanPlanStatus" size="small" @change="getPlanManagerTableData">
              <el-radio-button label="已下发"></el-radio-button>
              <el-radio-button label="物料发送完成"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" highlight-current-row border size="small" ref="multipleTablePlanManager" @select="handleSelectPlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
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
           :page-sizes="[5,10,20]"
           :page-size="PlanManagerTableData.limit"
           @size-change="handleSizeChangePlanManager"
           @current-change="handleCurrentChangePlanManager">
          </el-pagination>
        </div>
        <el-dialog :title="ZYPlanPUData.PUName+ '设备' + PUDialogType" :visible.sync="PUDialogVisible" width="80%" :append-to-body="true">
          <el-col :span="24">
            <el-form :inline="true">
              <el-form-item label="当前状态："><label class="marginRight color-darkblue">{{ ZYPlanPUData.ZYPlanStatus }}</label></el-form-item>
              <el-form-item label="调度编号："><label class="marginRight color-darkblue">{{ ZYPlanPUData.PlanNo }}</label></el-form-item>
              <el-form-item label="工艺段名称："><label class="marginRight color-darkblue">{{ ZYPlanPUData.PUName }}</label></el-form-item>
              <el-form-item label="品名名称："><label class="marginRight color-darkblue">{{ ZYPlanPUData.BrandName }}</label></el-form-item>
              <el-form-item label="计划产量："><label class="marginRight color-darkblue">{{ ZYPlanPUData.PlanQuantity }}</label></el-form-item>
              <el-form-item label="单位："><label class="color-darkblue">{{ ZYPlanPUData.Unit }}</label></el-form-item>
            </el-form>
          </el-col>
          <p class="text-size-18 marginBottom">
            <span class="marginRight">工艺计划使用设备</span>
          </p>
          <el-table :data="ZYTaskTableData" border size="small">
            <el-table-column prop="TaskID" label="任务单号"></el-table-column>
            <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
            <el-table-column prop="EQPName" label="设备名称"></el-table-column>
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
            <el-table-column prop="BrandName" label="品名名称"></el-table-column>
            <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="PlanStartTime" label="计划开始时间"></el-table-column>
            <el-table-column prop="PlanEndTime" label="计划结束时间"></el-table-column>
            <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
            <el-table-column prop="ActEndTime" label="实际结束时间"></el-table-column>
            <el-table-column label="操作" fixed="right" width="150">
              <template slot-scope="scope">
                <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-dialog title="更换设备" :visible.sync="EQDialogVisible" width="40%" :append-to-body="true">
            <el-form>
              <el-form-item label="选择设备">
                <el-select v-model="EQPCode" placeholder="请选择" @change="selectEQPCode">
                  <el-option v-for="(item,index) in ProductEquipmentData" :key="index" :label="item.EQPCode +'-'+ item.EQPName" :value="item.EQPCode"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="EQDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveEQ">保存</el-button>
            </span>
          </el-dialog>
          <span slot="footer" class="dialog-footer">
            <el-button @click="PUDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="AuditPass" v-if="PUDialogType === '审核'">审核确认</el-button>
            <el-button type="primary" @click="CheckPass" v-if="PUDialogType === '复核'">复核确认</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"confirmProduction",
    data() {
      return {
        sendPlanPlanStatus:"已下发",
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        ZYPlanTableData:{
          data:[]
        },
        PUDialogVisible:false,
        PUDialogType:"",
        EQDialogVisible:false,
        ZYPlanPUData:{},
        ZYTaskTableData:[],
        ProductEquipmentData:[],  //工艺下所有设备
        EQPCode:"",
        EQPName:"",
        EQPID:"",
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          tableName: "PlanManager",
          PlanStatus:this.sendPlanPlanStatus,
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
      handleSelectPlanManager(selection,row){  //勾选时只能单选
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.$refs.multipleTablePlanManager.setCurrentRow(row)
        this.getZYPlanTableData()
      },
      handleRowClickPlanManager(row){
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.getZYPlanTableData()
      },
      getZYPlanTableData(){
        var that = this
        var params = {
          tableName: "ZYPlan",
          BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
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
            that.ZYPlanTableData.data = res.data.data.rows.sort(compare('PlanSeq'))
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      PUPlan(item,type){
        this.PUDialogVisible = true
        this.PUDialogType = type
        this.ZYPlanPUData = item
        this.getProductEquipment(this.ZYPlanPUData.PUName)
        this.getZYTaskTable()
      },
      getZYTaskTable(){
        let that = this
        var params = {
          tableName:"ZYTask",
          BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
          PUName:this.ZYPlanPUData.PUName,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.ZYTaskTableData = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getProductEquipment(PUName){
        let that = this
        var params = {
          tableName:"ProductEquipment",
          PUName:PUName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.ProductEquipmentData = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      selectEQPCode(){
        this.ProductEquipmentData.forEach(item =>{
          if(this.EQPCode === item.EQPCode){
            this.EQPName = item.EQPName
          }
        })
      },
      handleEdit(index,row){
        this.EQDialogVisible = true
        this.EQPCode = row.EQPCode
        this.EQPID = row.ID
      },
      saveEQ(){
        let that = this
        var params = {
          tableName:"ZYTask",
          ID:this.EQPID,
          EQPCode:this.EQPCode,
          EQPName:this.EQPName,
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res => {
          if(res.data.code === "200"){
            this.$message({
              type:'success',
              message:res.data.message
            })
            this.EQDialogVisible = false
            this.getZYTaskTable()
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      AuditPass(){
        let that = this
        if(this.ZYPlanPUData.ZYPlanStatus === "待生产") {
          var params = {
            tableName: "ZYPlan",
            ID: this.ZYPlanPUData.ID,
            ZYPlanStatus: "设备已审核"
          }
          this.axios.put("/api/CUID", this.qs.stringify(params)).then(res => {
            if (res.data.code === "200") {
              this.$message({
                type: 'success',
                message: res.data.message
              })
              this.PUDialogVisible = false
              this.getZYPlanTableData()
            } else {
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }else{
          this.$message({
            type: 'info',
            message: "当前工序状态不能做审核操作"
          });
        }
      },
      CheckPass(){
        let that = this
        if(this.ZYPlanPUData.ZYPlanStatus === "设备已审核") {
          var params = {
            tableName: "ZYPlan",
            ID: this.ZYPlanPUData.ID,
            ZYPlanStatus: "设备已复核"
          }
          this.axios.put("/api/CUID", this.qs.stringify(params)).then(res => {
            if (res.data.code === "200") {
              this.$message({
                type: 'success',
                message: res.data.message
              })
              this.PUDialogVisible = false
              this.getZYPlanTableData()
            } else {
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }else{
          this.$message({
            type: 'info',
            message: "当前工序状态不能做复核操作"
          });
        }
      },
    }
  }
</script>

<style scoped>
  .container-col{
    clear: both;
    overflow: hidden;
    border-radius: 4px;
    padding: 0 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
  .connectLine{
    display: inherit;
    width: 1px;
    height: 15px;
    margin-top: 5px;
    background: #ccc;
  }
</style>
