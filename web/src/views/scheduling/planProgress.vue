<template>
   <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16 marginRight">选择批计划，查看计划工艺进展</span>
        <span class="sideState bg-gray"></span><span class="text-size-14">待生产</span>
        <span class="sideState bg-lightgreen"></span><span class="text-size-14">设备已审核</span>
        <span class="sideState bg-darkblue"></span><span class="text-size-14">设备已复核</span>
        <span class="sideState bg-success"></span><span class="text-size-14">已完成</span>
      </div>
      <div class="platformContainer">
        <el-row :gutter="15">
          <el-col :span="24">
            <div style="display:inline-block;margin-right:18px;">
              <div style="display: inline-block; text-align: center;">
                <div class="container-col text-size-14 bg-gray" :class="{'bg-success': PlanManagerTableData.PlanStatus === '待下发' || PlanManagerTableData.PlanStatus === '待执行' || PlanManagerTableData.PlanStatus === '待备料' || PlanManagerTableData.PlanStatus === '物料发送中' || PlanManagerTableData.PlanStatus === '发送物料完成' || PlanManagerTableData.PlanStatus === '已发送投料计划'}">审核计划</div>
              </div>
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
            </div>
            <div style="display:inline-block;margin-right:18px;">
              <div style="display: inline-block; text-align: center;">
                <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待执行' || PlanManagerTableData.PlanStatus === '待备料' || PlanManagerTableData.PlanStatus === '物料发送中' || PlanManagerTableData.PlanStatus === '发送物料完成' || PlanManagerTableData.PlanStatus === '已发送投料计划'}">下发计划</div>
              </div>
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;"></i>
            </div>
            <div style="display:inline-block;margin-right:18px;">
              <div style="display: inline-block; text-align: center;">
                <div class="container-col text-size-14 bg-gray" :class="{'bg-success':PlanManagerTableData.PlanStatus === '待备料' || PlanManagerTableData.PlanStatus === '物料发送中' || PlanManagerTableData.PlanStatus === '发送物料完成' || PlanManagerTableData.PlanStatus === '已发送投料计划'}">执行计划</div>
              </div>
            </div>
            <div v-for="(item, index) in ProcessSectionData" :key="index" style="display: inline-block;margin-right:18px;vertical-align: top;" @click="PUPlan(item)">
              <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
              <div style="display: inline-block; text-align: center;" v-if="item.PUName == '备料'">
                <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':PlanManagerTableData.PlanStatus === '待备料','bg-darkblue':PlanManagerTableData.PlanStatus === '物料发送中','bg-success':PlanManagerTableData.PlanStatus === '物料发送完成'}">
                  {{ item.PUName }}
                </div>
              </div>
              <div style="display: inline-block; text-align: center;" v-else>
                <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':item.ZYPlanStatus === '待确认','bg-lightgreen':item.ZYPlanStatus === '待审核','bg-orange':item.ZYPlanStatus === '待复核','bg-darkblue':item.ZYPlanStatus === '执行','bg-success':item.ZYPlanStatus === '已完成'}">
                  {{ item.PUName }}
                </div>
                <div class="text-center" style="display: inherit;">
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '待审核' || item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '执行' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '待审核' || item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '执行' ? 'dark':'plain'">设备确认</el-tag>
                  </p>
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '执行' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '执行' ? 'dark':'plain'">审核</el-tag>
                  </p>
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '执行' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '执行' ? 'dark':'plain'">复核</el-tag>
                  </p>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
        <el-form :inline="true" class="marginTop">
          <el-form-item label="查询日期">
            <el-date-picker type="date" v-model="PlanManagerTableData.searchDate" size="small" format="yyyy-MM-dd" value-format="yyyy-MM-dd" style="width: 160px;" @change="getPlanManagerTableData"></el-date-picker>
          </el-form-item>
          <el-form-item label="查询状态">
            <el-select v-model="PlanManagerTableData.searchPlanStatus" placeholder="请选择" size="small" @change="getPlanManagerTableData">
              <el-option v-for="(item,index) in PlanManagerTableData.searchFormData" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-button type="primary" size="small" icon='el-icon-refresh-right' @click="getPlanManagerTableData">刷新</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" highlight-current-row border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @select="handleSelectPlanManager" @row-click="handleRowClickPlanManager">
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
        <el-dialog title="工艺信息" :visible.sync="PUDialogVisible" width="80%" :append-to-body="true" v-if="PlanManagerTableData.multipleSelection.length > 0">
          <el-table :data="ZYPlanTableData.data" border size="small" class="marginBottom">
            <el-table-column prop="PlanNo" label="调度编号"></el-table-column>
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="PUCode" label="工艺段编码"></el-table-column>
            <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
            <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
            <el-table-column prop="BrandName" label="品名名称"></el-table-column>
            <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="ZYPlanStatus" label="计划状态"></el-table-column>
          </el-table>
          <el-row :gutter="15">
            <el-col :span="12">
              <p class="text-size-18 marginBottom">计划使用设备</p>
              <el-table :data="EquipmentBatchRunTimeTableData.data" border size="small">
                <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
                <el-table-column prop="EQPName" label="设备名称"></el-table-column>
                <el-table-column prop="StartTime" label="计划开始时间"></el-table-column>
                <el-table-column prop="EndTime" label="计划结束时间"></el-table-column>
              </el-table>
            </el-col>
            <el-col :span="12">
              <p class="text-size-18 marginBottom">实际使用设备</p>
              <el-table :data="ZYTaskTableData.data" border size="small" v-show="PlanManagerTableData.multipleSelection[0].PlanStatus === '已发送投料计划'">
                <el-table-column prop="TaskID" label="任务单号"></el-table-column>
                <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
                <el-table-column prop="EQPName" label="设备名称"></el-table-column>
                <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
                <el-table-column prop="ActEndTime" label="实际结束时间"></el-table-column>
              </el-table>
            </el-col>
          </el-row>
          <span slot="footer" class="dialog-footer">
            <el-button @click="PUDialogVisible = false">好 的</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
   </el-row>
</template>

<script>
  var moment = require('moment');
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
          searchDate:"",
          searchFormData:[
            {label:"全部",value:""},
            {label:"待审核",value:"待审核"},
            {label:"待下发",value:"待下发"},
            {label:"待执行",value:"待执行"},
            {label:"待备料",value:"待备料"},
            {label:"物料发送中",value:"物料发送中"},
            {label:"发送物料完成",value:"发送物料完成"},
            {label:"已发送投料计划",value:"已发送投料计划"},
            {label:"已完成",value:"已完成"},
          ]
        },
        ProcessSectionData:[], //品名的工艺段
        PUDialogVisible:false,
        ZYPlanTableData:{
          data:[],
        },
        ZYTaskTableData:{
          data:[]
        },
        EquipmentBatchRunTimeTableData:{
          data:[]
        }
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
          SchedulePlanCode:this.PlanManagerTableData.searchDate,
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
        this.PlanManagerTableData.PlanStatus=row.PlanStatus
        this.$refs.multipleTablePlanManager.clearSelection()
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
        this.$refs.multipleTablePlanManager.setCurrentRow(row)
        this.getZYPlanTableData()
      },
      handleRowClickPlanManager(row){
        this.PlanManagerTableData.PlanStatus=row.PlanStatus
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
            that.ProcessSectionData = res.data.data.rows.sort(compare('PlanSeq'))
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      PUPlan(item){
        this.PUDialogVisible = true
        var that = this
        var params = {
          tableName: "ZYPlan",
          BrandCode:item.BrandCode,
          PUCode:item.PUCode,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.ZYPlanTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
        var params1 = {
          tableName: "ZYTask",
          BrandCode:item.BrandCode,
          PUCode:item.PUCode,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params1
        }).then(res => {
          if(res.data.code === "200"){
            that.ZYTaskTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
        var params2 = {
          tableName: "EquipmentBatchRunTime",
          BrandCode:item.BrandCode,
          PUCode:item.PUCode,
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/CUID",{
          params: params2
        }).then(res => {
          if(res.data.code === "200"){
            that.EquipmentBatchRunTimeTableData.data = res.data.data.rows
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
