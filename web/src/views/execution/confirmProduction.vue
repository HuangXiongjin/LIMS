<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16 marginRight">确认生产使用设备</span>
        <span class="sideState bg-gray"></span><span class="text-size-14">待确认</span>
        <span class="sideState bg-lightgreen"></span><span class="text-size-14">待复核</span>
        <span class="sideState bg-brown"></span><span class="text-size-14">开始投料</span>
        <span class="sideState bg-darkblue"></span><span class="text-size-14">生产中</span>
        <span class="sideState bg-success"></span><span class="text-size-14">已完成</span>
      </div>
      <div class="platformContainer">
        <el-row class="marginBottom" v-if="PlanManagerTableData.multipleSelection.length == 1">
          <el-col :span="24">
            <div v-for="(item, index) in ZYPlanTableData.data" :key="index" style="display: inline-block;margin-right:18px;vertical-align: top;">
              <div style="display: inline-block; text-align: center;" v-if="item.PUName === '备料'">
                <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':PlanManagerTableData.multipleSelection[0].PlanStatus === '待备料','bg-darkblue':PlanManagerTableData.multipleSelection[0].PlanStatus === '物料发送中','bg-success':PlanManagerTableData.multipleSelection[0].PlanStatus === '物料发送完成' || PlanManagerTableData.multipleSelection[0].PlanStatus === '已发送投料计划' }">
                  {{ item.PUName }}
                </div>
              </div>
              <div style="display: inline-block; text-align: center;" v-else>
                <div class="container-col text-size-14 bg-gray" :class="{'bg-gray':item.ZYPlanStatus === '待确认','bg-lightgreen':item.ZYPlanStatus === '待复核','bg-brown':item.ZYPlanStatus === '开始投料','bg-darkblue':item.ZYPlanStatus === '执行','bg-success':item.ZYPlanStatus === '已完成'}">
                  {{ item.PUName }}
                </div>
                <div class="text-center" style="display: inherit;">
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '开始投料' || item.ZYPlanStatus === '执行' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '待复核' || item.ZYPlanStatus === '开始投料' || item.ZYPlanStatus === '执行' ? 'dark':'plain'" @click="PUPlan(item,'设备确认')">设备确认</el-tag>
                  </p>
                  <p class="connectLine marginRight"></p>
                  <p class="marginRight">
                    <el-tag class="cursor-pointer" v-bind:type="item.ZYPlanStatus === '执行' || item.ZYPlanStatus === '开始投料' ? 'success':'info'" v-bind:effect="item.ZYPlanStatus === '执行' || item.ZYPlanStatus === '开始投料' ? 'dark':'plain'" @click="PUPlan(item,'复核')">复核</el-tag>
                  </p>
                </div>
              </div>
              <i class="fa fa-arrow-right" v-if="index != ZYPlanTableData.data.length -1" style="vertical-align: top;margin-top: 10px;margin-right:10px;"></i>
            </div>
          </el-col>
        </el-row>
        <el-form :inline="true">
          <el-form-item class="floatRight">
            <el-radio-group v-model="PlanStatus" size="small" @change="getPlanManagerTableData">
              <el-radio-button label="待备料"></el-radio-button>
              <el-radio-button label="物料发送中"></el-radio-button>
              <el-radio-button label="物料发送完成"></el-radio-button>
              <el-radio-button label="已发送投料"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="PlanManagerTableData.data" highlight-current-row border size="small" ref="multipleTablePlanManager" @select="handleSelectPlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
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
           :page-sizes="[10,20,30,40,50]"
           :page-size="PlanManagerTableData.limit"
           @size-change="handleSizeChangePlanManager"
           @current-change="handleCurrentChangePlanManager">
          </el-pagination>
        </div>
        <!--提取设备确认  物料对应设备-->
        <el-dialog title="设备确认" :visible.sync="EQTQDialogVisible" width="80%" :append-to-body="true" top="5vh">
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
          <p class="text-size-18 marginBottom marginTop">
            <span class="marginRight">批次物料对应提取设备</span>
          </p>
          <el-table :data="MaterialTableData.data" border size="small">
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="BrandName" label="品名"></el-table-column>
            <el-table-column prop="MATName" label="物料名称" width="300"></el-table-column>
            <el-table-column prop="BucketNum" label="桶号"></el-table-column>
            <el-table-column prop="BucketWeight" label="重量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
            <el-table-column prop="EQPCode" label="提取设备编码"></el-table-column>
            <el-table-column prop="EQPName" label="提取设备名称"></el-table-column>
            <el-table-column prop="Description" label="描述"></el-table-column>
            <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
            <el-table-column label="操作" fixed="right" width="120">
              <template slot-scope="scope">
                <el-button size="mini" type="primary" @click="EditMaterial(scope.$index, scope.row)" v-has="['设备确认']">设置投料</el-button>
              </template>
            </el-table-column>
          </el-table>
          <span slot="footer" class="dialog-footer">
            <el-button @click="EQTQDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="MaterialEQPass" v-has="['设备确认']">设备确认</el-button>
          </span>
        </el-dialog>
        <!--非提取设备确认-->
        <el-dialog title="设备确认" :visible.sync="EQConfirmDialogVisible" width="80%" :append-to-body="true" top="5vh">
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
          <el-form :inline="true">
            <el-form-item>
              <el-button type="primary" size="mini" @click="EQDialogVisible = true" v-has="['设备确认']">一键分配设备</el-button>
            </el-form-item>
          </el-form>
          <el-table :data="ZYTaskTableData" border size="small">
            <el-table-column prop="TaskID" label="任务单号"></el-table-column>
            <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
            <el-table-column prop="EQPName" label="设备名称"></el-table-column>
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
            <el-table-column prop="BrandName" label="品名名称"></el-table-column>
            <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
            <el-table-column prop="ActEndTime" label="实际结束时间"></el-table-column>
            <el-table-column label="操作" fixed="right" width="120">
              <template slot-scope="scope">
                <el-button size="mini" @click="handleDeleteEq(scope.$index, scope.row)" v-has="['设备确认']">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!--选择要使用的设备-->
          <el-dialog title="选择设备" :visible.sync="EQDialogVisible" width="40%" :append-to-body="true" top="5vh">
            <el-table border :data="ProductEquipmentData" size='small' @selection-change="handleEQSelectionChange">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
              <el-table-column prop="Number" label="设备编号"></el-table-column>
              <el-table-column prop="EQPName" label="设备名称"></el-table-column>
              <el-table-column prop="Desc" label="描述"></el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
              <el-button @click="EQDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveEQ">保存</el-button>
            </span>
          </el-dialog>
          <span slot="footer" class="dialog-footer">
            <el-button @click="EQConfirmDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="EQConfirm" v-has="['设备确认']">设备确认</el-button>
          </span>
        </el-dialog>
        <!--提取复核弹框-->
        <el-dialog title="复核" :visible.sync="confirmTQDialogVisible" width="80%" :append-to-body="true" top="5vh">
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
          <p class="text-size-18 marginBottom marginTop">
            <span class="marginRight">根据实际情况检查生产使用设备</span>
          </p>
          <el-table :data="MaterialTableData.data" border size="small">
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="BrandName" label="品名"></el-table-column>
            <el-table-column prop="MATName" label="物料名称" width="340"></el-table-column>
            <el-table-column prop="BucketNum" label="桶号"></el-table-column>
            <el-table-column prop="TaskTurn" label="轮次"></el-table-column>
            <el-table-column prop="BucketWeight" label="重量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
            <el-table-column prop="EQPCode" label="提取设备编码"></el-table-column>
            <el-table-column prop="EQPName" label="提取设备名称"></el-table-column>
            <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
            <el-table-column label="操作" fixed="right" width="120">
              <template slot-scope="scope">
                <el-button size="mini" type="primary" @click="EditMaterial(scope.$index, scope.row)" v-has="['设备复核']">修改设备</el-button>
              </template>
            </el-table-column>
          </el-table>
          <span slot="footer" class="dialog-footer">
            <el-button @click="confirmTQDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="CheckTQPass" v-has="['设备复核']">复核确认</el-button>
          </span>
        </el-dialog>
        <!--非提取复核弹框-->
        <el-dialog title="复核" :visible.sync="confirmDialogVisible" width="80%" :append-to-body="true" top="5vh">
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
          <p class="text-size-18 marginBottom marginTop">
            <span class="marginRight">根据实际情况检查生产使用设备</span>
          </p>
          <el-form :inline="true">
            <el-form-item>
              <el-button type="primary" size="mini" @click="EQDialogVisible = true" v-has="['设备确认']">一键分配设备</el-button>
            </el-form-item>
          </el-form>
          <el-table :data="ZYTaskTableData" border size="small">
            <el-table-column prop="TaskID" label="任务单号"></el-table-column>
            <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
            <el-table-column prop="EQPName" label="设备名称"></el-table-column>
            <el-table-column prop="BatchID" label="批次号"></el-table-column>
            <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
            <el-table-column prop="BrandName" label="品名名称"></el-table-column>
            <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
            <el-table-column prop="Unit" label="单位"></el-table-column>
            <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
            <el-table-column prop="ActEndTime" label="实际结束时间"></el-table-column>
          </el-table>
          <span slot="footer" class="dialog-footer">
            <el-button @click="confirmDialogVisible = false">关闭</el-button>
            <el-button type="primary" @click="CheckPass" v-has="['设备复核']">复核确认</el-button>
          </span>
        </el-dialog>
        <!--修改物料桶-->
        <el-dialog title="选择已分配的设备" :visible.sync="EQMaterialDialogVisible" width="40%" :append-to-body="true" v-if="EQMaterialDialogVisible" top="5vh">
          <el-form :model="MaterialTableData.formField" label-width="110px">
            <el-form-item label="批次号">
              <el-input v-model="PlanManagerTableData.multipleSelection[0].BatchID" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="品名">
              <el-input v-model="PlanManagerTableData.multipleSelection[0].BrandName" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="物料名称">
              <el-select v-model="MaterialTableData.formField.MATName" multiple placeholder="请选择" :disabled="true" style="width: 360px;">
                <el-option
                  v-for="item in MATNameOptions"
                  :key="item.value"
                  :label="item.MATName"
                  :value="item.MATName">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="桶投入顺序">
              <draggable :list="MaterialTableData.formField.BucketNum" v-bind="{group:'article', disabled: false,sort: true}"
                class="dragArea11" style="border: 1px dashed #B9B9B9;padding: 10px;">
                <div v-for="(item, index) in MaterialTableData.formField.BucketNum" :key="index" class="list-complete-item">
                  <div class="container-col">
                    <span class="text-size-14">第{{ index +1 }}桶：{{ item }}</span>
                  </div>
                </div>
              </draggable>
            </el-form-item>
            <el-form-item label="选择设备">
              <el-select v-model="MaterialEQPCode" placeholder="请选择" @change="selectMaterialEQPCode">
                <el-option v-for="(item,index) in ProductEquipmentData" :key="index" :label="item.Number" :value="item.EQPCode"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="描述">
              <el-input v-model="MaterialTableData.formField.Description"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="EQMaterialDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveMaterialEQ">保存</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import draggable from 'vuedraggable'
  export default {
    name:"confirmProduction",
    components:{draggable},
    data() {
      return {
        PlanStatus:"物料发送完成",
        PlanManagerTableData:{
          data:[],
          limit: 10,
          offset: 1,
          total: 0,
          multipleSelection: [],
        },
        ZYPlanTableData:{
          data:[]
        },
        EQConfirmDialogVisible:false,  //非提取确认设备弹框
        EQTQDialogVisible:false,  //提取确认设备弹框
        EQDialogVisible:false, //选设备弹框
        confirmDialogVisible:false, //非提取复核弹框
        confirmTQDialogVisible:false, //提取复核弹框
        ZYPlanPUData:{},
        ZYTaskTableData:[],
        ProductEquipmentData:[],  //工艺下所有设备
        ProductEquipmentSelection:[],  //选中设备
        MaterialTableData:{
          data:[],
          formField:{
            ID:"",
            MATName:[],
            BucketNum:[],
            Description:""
          }
        },
        EQMaterialDialogVisible:false,
        MATNameOptions:[],
        MaterialEQPCode:"",
        MaterialEQPName:"",
      }
    },
    mounted(){
      this.getPlanManagerTableData()
    },
    methods:{
      //选择批计划
      getPlanManagerTableData(){
        var that = this
        var flag = ""
        if(this.PlanStatus === "待备料"){
          flag = "待备料"
        }else if(this.PlanStatus === "物料发送中"){
          flag = "物料发送中"
        }else if(this.PlanStatus === "物料发送完成"){
          flag = "物料发送完成"
        }else if(this.PlanStatus === "已发送投料"){
          flag = "已发送投料计划"
        }
        var params = {
          tableName: "PlanManager",
          PlanStatus:flag,
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
      getZYPlanTableData(){  //获取批计划下的工艺 ZYPlan
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
        this.ZYPlanPUData = item
        if(type === "设备确认"){
          if(item.PUName === "提取（醇提）" || item.PUName === "提取（水提）" || item.PUName === "渗漏+醇提" || item.PUName === "浸渍提取"){
            this.EQTQDialogVisible = true
            this.getProductEquipment(this.ZYPlanPUData.PUName)
            this.getMaterialTableData()
          }else{
            this.EQConfirmDialogVisible = true
            this.getProductEquipment(this.ZYPlanPUData.PUName)
            this.getZYTaskTable()
          }
        }else if(type === "复核"){
          if(item.PUName === "提取（醇提）" || item.PUName === "提取（水提）" || item.PUName === "渗漏+醇提" || item.PUName === "浸渍提取"){
            this.confirmTQDialogVisible = true
            this.getMaterialTableData()
          }else{
            this.confirmDialogVisible = true
            this.getZYTaskTable()
          }
        }
      },
      getZYTaskTable(){  //获取工艺下选择的设备
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
      getProductEquipment(PUName){  //查询工艺下所有设备
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
      handleEQSelectionChange(row){
        this.ProductEquipmentSelection = row
      },
      handleDeleteEq(index,item){  //删除工艺下的设备
        var params = {tableName:"ZYTask"}
        var mulId = [{id:item.ID}]
        params.delete_data = JSON.stringify(mulId)
        this.$confirm('确定删除所选记录？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          this.axios.delete("/api/CUID",{
            params: params
          }).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
            }
            this.getZYTaskTable()
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      getMaterialTableData(){  //查询物料明细
        var that = this
        var params = {
          tableName: "BatchMaterialInfo",
          BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
          BrandCode:this.PlanManagerTableData.multipleSelection[0].BrandCode,
          SendFlag:"投料系统已接收",
          searchModes:"精确查询"
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MaterialTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //获取物料BOM
      getBOMData(){
        var that = this
        var params = {
          tableName: "MaterialBOM",
          BrandName:this.PlanManagerTableData.multipleSelection[0].BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MATNameOptions = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      saveEQ(){  //保存添加多条设备
        let that = this
        var EqpList = []
        this.ProductEquipmentSelection.forEach(item =>{
          EqpList.push({
            EQPCode:item.EQPCode,
            EQPName:item.Number
          })
        })
        var params = {
          ID:this.ZYPlanPUData.ID,
          EqpList:JSON.stringify(EqpList),
        }
        this.axios.post("/api/taskSaveEqpCheck",this.qs.stringify(params)).then(res => {
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
      //提取设备确认
      MaterialEQPass(){
        let that = this
        this.$confirm('是否确定当前物料桶信息和投放的设备？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          var params = {
            tableName: "ZYPlan",
            ID: this.ZYPlanPUData.ID,
            ZYPlanStatus: "待复核"
          }
          this.axios.put("/api/CUID", this.qs.stringify(params)).then(res => {
            if (res.data.code === "200") {
              this.$message({
                type: 'success',
                message: res.data.message
              })
              this.EQTQDialogVisible = false
              this.getZYPlanTableData()
            } else {
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      //非提取设备确认
      EQConfirm(){
        let that = this
        this.$confirm('确定选择好生产设备并确认吗？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          var params = {
            tableName: "ZYPlan",
            ID: this.ZYPlanPUData.ID,
            ZYPlanStatus: "待复核"
          }
          this.axios.put("/api/CUID", this.qs.stringify(params)).then(res => {
            if (res.data.code === "200") {
              this.$message({
                type: 'success',
                message: res.data.message
              })
              this.EQConfirmDialogVisible = false
              this.getZYPlanTableData()
            } else {
              that.$message({
                type: 'info',
                message: res.data.message
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      EditMaterial(index,row){ //物料桶选择设备、顺序
        this.EQMaterialDialogVisible = true
        this.getBOMData()
        this.MaterialTableData.formField = {
          ID:row.ID,
          MATName:row.MATName.split(","),
          BucketNum:row.BucketNum.split(","),
          Description:row.Description,
        }
        this.MaterialEQPCode = row.EQPCode
        this.selectMaterialEQPCode()
      },
      selectMaterialEQPCode(){ //选择设备后根据编码获取设备名称
        this.ProductEquipmentData.forEach(item =>{
          if(this.MaterialEQPCode === item.EQPCode){
            this.MaterialEQPName = item.Number
          }
        })
      },
      saveMaterialEQ(){ //保存选择投入物料的设备
        let that = this
        var params = {
          tableName:"BatchMaterialInfo",
          ID:this.MaterialTableData.formField.ID,
          BucketNum:this.MaterialTableData.formField.BucketNum.join(','),
          Description:this.MaterialTableData.formField.Description,
          EQPCode:this.MaterialEQPCode,
          EQPName:this.MaterialEQPName,
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res => {
          if(res.data.code === "200"){
            this.$message({
              type:'success',
              message:res.data.message
            })
            this.EQMaterialDialogVisible = false
            this.getMaterialTableData()
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //提取复核 生成task
      CheckTQPass(){
        let that = this
        if(this.ZYPlanPUData.ZYPlanStatus === "待复核") {
          this.$confirm('是否确定当前设备以及物料投放信息进行复核？确认后无法再复核', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            var params = {
              ID:this.ZYPlanPUData.ID,
            }
            this.axios.post("/api/taskSaveEqpCheck",this.qs.stringify(params)).then(res => {
              if(res.data.code === "200"){
                this.$message({
                  type:'success',
                  message:res.data.message
                })
                this.confirmTQDialogVisible = false
                this.getZYPlanTableData()
              }else{
                that.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消操作'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: "当前工序状态不能做复核操作"
          });
        }
      },
      //非提取复核
      CheckPass(){
        let that = this
        if(this.ZYPlanPUData.ZYPlanStatus === "待复核") {
          this.$confirm('是否确定当前设备进行复核？确认后无法再复核', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            var params = {
              tableName: "ZYPlan",
              ID: this.ZYPlanPUData.ID,
              ZYPlanStatus: "执行"
            }
            this.axios.put("/api/CUID",this.qs.stringify(params)).then(res => {
              if(res.data.code === "200"){
                this.$message({
                  type:'success',
                  message:res.data.message
                })
                this.confirmDialogVisible = false
                this.getZYPlanTableData()
              }else{
                that.$message({
                  type: 'info',
                  message: res.data.message
                });
              }
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消操作'
            });
          });
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
