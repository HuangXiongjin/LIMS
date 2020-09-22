<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="选择订单计划"></el-step>
        <el-step title="选择批次计划"></el-step>
        <el-step title="生产配置"></el-step>
        <el-step title="甘特图"></el-step>
        <el-step title="排产清单"></el-step>
      </el-steps>
      <el-row :gutter="15" v-show="steps == 0">
        <el-col :span="4">
          <div class="platformContainer">
            <p class="marginBottom">请根据品名查询计划</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in scheduleList" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode,item.BrandType)">{{item.BrandName}}</el-tag>
          </div>
        </el-col>
        <el-col :span="20">
          <div class="platformContainer" v-if="BrandActive">
            <p>当前选择的是{{ BrandActive }}</p>
          </div>
          <div class="platformContainer">
            <el-form :inline="true">
              <el-form-item v-for="(item,index) in planTableData.handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleForm(item.label)">{{ item.label }}</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="planTableData.data" border size="small" ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PlanNum" label="编号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="BrandType" label="药品类型"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产值"></el-table-column>
              <el-table-column prop="PlanTimeLen" label="计划时长"></el-table-column>
              <el-table-column prop="PlanFinishTime" label="计划交付时间"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
              <el-table-column prop="Description" label="备注"></el-table-column>
              <el-table-column prop="CreateTimeTime" label="创建时间"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="planTableData.total"
               :current-page="planTableData.offset"
               :page-sizes="[5,10,20]"
               :page-size="planTableData.limit"
               @size-change="handleSizeChange"
               @current-change="handleCurrentChange">
              </el-pagination>
            </div>
            <el-dialog :title="planTableData.dialogTitle" :visible.sync="planTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="planTableData.formField" label-width="110px">
                <el-form-item label="编号">
                  <el-input v-model="planTableData.formField.PlanNum"></el-input>
                </el-form-item>
                <el-form-item label="计划产值">
                  <el-input v-model="planTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="计划时长">
                  <el-input v-model="planTableData.formField.PlanTimeLen"></el-input>
                </el-form-item>
                <el-form-item label="计划交付时间">
                  <el-date-picker v-model="planTableData.formField.PlanFinishTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="备注">
                  <el-input v-model="planTableData.formField.Description"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="planTableData.dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="save">保 存</el-button>
              </span>
            </el-dialog>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="steps == 1">
        <el-col :span="24">
          <div class="platformContainer">
            <span>计划单号：{{ planTableData.multipleSelection[0].PlanNum }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>计划产值：{{ planTableData.multipleSelection[0].PlanQuantity }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>品名：{{ BrandActive }}</span>
          </div>
          <div class="platformContainer">
            <el-form :inline="true" :model="formAllotBatch">
              <el-form-item label="批数">
                <el-input v-model="formAllotBatch.BatchSum" siBatchNumze="small"></el-input>
              </el-form-item>
              <el-form-item label="每批间隔时间">
                <el-input v-model="formAllotBatch.BatchDuration" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="planschedul">自动分批</el-button>
              </el-form-item>
            </el-form>
            <p class="text-size-14 color-grayblack">可估算参数，自动分配批次计划</p>
          </div>
          <div class="platformContainer" style="min-height: 550px;">
            <el-form :inline="true">
              <el-form-item v-for="(item,index) in PlanManagerTableData.handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleFormPlanManager(item.label)">{{ item.label }}</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PlanNum" label="计划编号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="PlanQuantity" label="批次计划重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="BrandType" label="产品类型"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态"></el-table-column>
              <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
              <el-table-column prop="PlanEndTime" label="计划完成时间"></el-table-column>
              <el-table-column prop="Describtion" label="描述"></el-table-column>
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
            <el-dialog :title="PlanManagerTableData.dialogTitle" :visible.sync="PlanManagerTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="PlanManagerTableData.formField" label-width="110px">
                <el-form-item label="批次号">
                  <el-input v-model="PlanManagerTableData.formField.BatchID"></el-input>
                </el-form-item>
                <el-form-item label="批次计划重量">
                  <el-input v-model="PlanManagerTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                  <el-select v-model="PlanManagerTableData.formField.Unit" placeholder="请选择">
                    <el-option v-for="(item,index) in unitOptions" :key="index" :label="item.UnitValue" :value="item.UnitValue">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="计划开始时间">
                  <el-date-picker v-model="PlanManagerTableData.formField.PlanBeginTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="计划完成时间">
                  <el-date-picker v-model="PlanManagerTableData.formField.PlanEndTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="PlanManagerTableData.dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="savePlanManager">保 存</el-button>
              </span>
            </el-dialog>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="steps == 2">
        <el-col :span="24">
          <div class="platformContainer">
            <span>计划单号：{{ planTableData.multipleSelection[0].PlanNum }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>品名：{{ BrandActive }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>批次号：{{ PlanManagerTableData.multipleSelection[0].BatchID }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>产品类型：{{ PlanManagerTableData.multipleSelection[0].BrandType }}</span>
          </div>
          <div class="platformContainer">
            <el-row :gutter="15">
              <el-col :span="5" v-for="(item,index) in processList" :key="index">
                <div class="marginBottom text-size-20">{{ item.PUName }}</div>
                <el-popover
                  placement="right"
                  width="360"
                  trigger="click">
                  <el-checkbox border v-for="eq in item.eqList" v-model="eq.isSelected" :key="eq.EQPCode" class="marginBottom-10">
                    {{ eq.EQPName }}-<span class="color-success" v-if="eq.EQPStatus">可用</span><span class="color-orange" v-if="!eq.EQPStatus">等待</span>
                  </el-checkbox>
                  <el-button slot="reference" size="small">选择设备</el-button>
                </el-popover>
                <el-button type="primary" size="small">自动分配</el-button>
                <p class="marginTop marginBottom-10 text-size-16">已分配设备</p>
                <div class="marginBottom-10" v-for="eq in item.eqList" :key="eq.EQPCode" v-if="eq.isSelected">
                  <p class="text-size-14 color-darkblue">{{ eq.EQPName }}</p>
                  <el-form label-width="72px">
                    <el-form-item label="等待时长">
                      <el-input type="text" v-model="eq.waitTime" size="mini" style="width: 60px"></el-input>
                    </el-form-item>
                  </el-form>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <el-col :span="24" style="text-align: right;">
        <el-button type="info" v-show="steps != 0" @click="resetStep">重置</el-button>
        <el-button type="primary" v-show="steps != 0" @click="lastStep">上一步</el-button>
        <el-button type="primary" v-show="steps == 2" @click="savePlanEq">保存</el-button>
        <el-button type="primary" v-show="steps != 4" @click="nextStep">下一步</el-button>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "scheduling",
    components:{},
    data(){
      return{
        steps:0,
        productName:"",
        scheduleTableData:[],
        scheduleList:[],
        BrandActive:"",
        BrandCode:"",
        BrandType:"",
        planTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
          handleType:[
            {type:"primary",label:"添加"},
            {type:"danger",label:"删除"},
          ],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            PlanNum:"",
            PlanQuantity:"",
            PlanTimeLen:"",
            PlanFinishTime:"",
            Description:""
          },
        },
        unitOptions:[],
        PlanManagerTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          multipleSelection: [],
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            BatchID:"",
            PlanQuantity:"",
            Unit:"",
            PlanBeginTime:"",
            PlanEndTime:"",
          },
        },
        formAllotBatch:{
          BatchSum:"",
          BatchDuration:""
        },
        processList:[],
      }
    },
    mounted(){
      this.getScheduleTableData()
      this.getUnit()
    },
    methods:{
      nextStep(){
        if(this.steps == 0){
          if(this.planTableData.multipleSelection.length == 1){
            this.steps++
            this.getPlanManagerTableData()
          }else{
            this.$message({
              type: 'info',
              message: "请选择一条ERP计划"
            });
          }
        }else if(this.steps == 1){
          if(this.PlanManagerTableData.multipleSelection.length == 1){
            this.steps++
            this.getBrandProcess()
          }else{
            this.$message({
              type: 'info',
              message: "请选择一条批次计划"
            });
          }
        }else{
          this.steps++
        }
      },
      lastStep(){
        this.steps--
      },
      resetStep(){
        this.steps = 0
      },
      getUnit(){
        var that = this
        var params = {
          tableName: "Unit",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.unitOptions = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getScheduleTableData(){ //获取品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.scheduleTableData = res.data.data.rows
            that.scheduleList = that.scheduleTableData
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleChangeProductName(queryString){
        if(queryString != ""){
          this.scheduleList = this.scheduleTableData.filter((string) =>{
            return Object.keys(string).some(function(key) {
              return String(string[key]).toLowerCase().indexOf(queryString) > -1
            })
          })
        }else{
          this.scheduleList = this.scheduleTableData
        }
      },
      clickBrandTag(BrandName,BrandCode){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.getPlanTableData(this.BrandActive)
      },
      getPlanTableData(BrandName){
        var that = this
        var params = {
          tableName: "product_plan",
          field:"BrandName",
          fieldvalue:BrandName,
          limit:this.planTableData.limit,
          offset:this.planTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.planTableData.data = res.data.data.rows
            that.planTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.getPlanTableData(this.BrandActive)
      },
      handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.getPlanTableData(this.BrandActive)
      },
      handleSelectionChange(row){
        this.planTableData.multipleSelection = row
      },
      handleRowClick(row){
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)
      },
      handleForm(label){
        if(label === "添加"){
          if(this.BrandActive){
            this.planTableData.dialogVisible = true
            this.planTableData.dialogTitle = label
          }else{
            this.$message({
              type: 'info',
              message: '请选择品名'
            });
          }
        }else if(label === "删除"){
          var params = {tableName:"product_plan"}
          var mulId = []
          if(this.planTableData.multipleSelection.length >= 1){
            this.planTableData.multipleSelection.forEach(item =>{
              mulId.push({id:item.ID});
            })
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
                this.getPlanTableData(this.BrandActive)
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          }else{
            this.$message({
              message: '至少选择一条数据进行删除',
              type: 'warning'
            });
          }
        }
      },
      save(){
        if(this.planTableData.dialogTitle === "添加"){
          var params = {
            tableName:"product_plan",
            PlanNum:this.planTableData.formField.PlanNum,
            PlanQuantity:this.planTableData.formField.PlanQuantity,
            PlanTimeLen:this.planTableData.formField.PlanTimeLen,
            PlanFinishTime:this.planTableData.formField.PlanFinishTime,
            Description:this.planTableData.formField.Description,
            CreateTimeTime:moment().format("YYYY-MM-DD HH:mm:ss"),
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            BrandType:this.BrandType,
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.planTableData.dialogVisible = false
              this.getPlanTableData(this.BrandActive)
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }
      },
      //批次计划
      getPlanManagerTableData(){
        var that = this
        var params = {
          PlanNum:this.planTableData.multipleSelection[0].PlanNum,
          limit:this.PlanManagerTableData.limit,
          offset:this.PlanManagerTableData.offset - 1
        }
        this.axios.get("/api/selectPlanmanager",{
          params: params
        }).then(res => {
          console.log(res.data)
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
        this.$refs.multipleTablePlanManager.clearSelection();
        this.$refs.multipleTablePlanManager.toggleRowSelection(row)
      },
      handleFormPlanManager(label){
        if(label === "添加"){
          if(this.BrandActive){
            this.PlanManagerTableData.dialogVisible = true
            this.PlanManagerTableData.dialogTitle = label
          }else{
            this.$message({
              type: 'info',
              message: '请选择品名'
            });
          }
        }else if(label === "修改"){
          if(this.PlanManagerTableData.multipleSelection.length == 1){
            this.PlanManagerTableData.dialogVisible = true
            this.PlanManagerTableData.dialogTitle = label
            this.PlanManagerTableData.formField = {
              BatchID:this.PlanManagerTableData.multipleSelection[0].BatchID,
              PlanQuantity:this.PlanManagerTableData.multipleSelection[0].PlanQuantity,
              Unit:this.PlanManagerTableData.multipleSelection[0].Unit,
              PlanBeginTime:this.PlanManagerTableData.multipleSelection[0].PlanBeginTime,
              PlanEndTime:this.PlanManagerTableData.multipleSelection[0].PlanEndTime,
            }
          }else{
            this.$message({
              type: 'info',
              message: '请选择批次'
            });
          }
        }else if(label === "删除"){
          var params = {tableName:"PlanManager"}
          var mulId = []
          if(this.PlanManagerTableData.multipleSelection.length >= 1){
            this.PlanManagerTableData.multipleSelection.forEach(item =>{
              mulId.push({id:item.ID});
            })
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
                this.getPlanManagerTableData()
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          }else{
            this.$message({
              message: '至少选择一条数据进行删除',
              type: 'warning'
            });
          }
        }
      },
      savePlanManager(){
        if(this.PlanManagerTableData.dialogTitle === "添加"){
          var params = {
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            BrandType:this.BrandType,
            PlanNum:this.planTableData.multipleSelection[0].PlanNum,
            BatchID:this.PlanManagerTableData.formField.BatchID,
            PlanQuantity:this.PlanManagerTableData.formField.PlanQuantity,
            Unit:this.PlanManagerTableData.formField.Unit,
            PlanBeginTime:this.PlanManagerTableData.formField.PlanBeginTime,
            PlanEndTime:this.PlanManagerTableData.formField.PlanEndTime,
          }
          this.axios.post("/api/makePlan",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.PlanManagerTableData.dialogVisible = false
              this.getPlanManagerTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }else if(this.PlanManagerTableData.dialogTitle === "修改"){
          var params = {
            ID:this.PlanManagerTableData.multipleSelection[0].ID,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            BrandType:this.BrandType,
            PlanNum:this.planTableData.multipleSelection[0].PlanNum,
            BatchID:this.PlanManagerTableData.formField.BatchID,
            PlanQuantity:this.PlanManagerTableData.formField.PlanQuantity,
            Unit:this.PlanManagerTableData.formField.Unit,
            PlanBeginTime:this.PlanManagerTableData.formField.PlanBeginTime,
            PlanEndTime:this.PlanManagerTableData.formField.PlanEndTime,
          }
          this.axios.get("/api/makePlan",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.PlanManagerTableData.dialogVisible = false
              this.getPlanManagerTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }
      },
      planschedul(){
        var that = this
        var params = {
          PlanNum:this.planTableData.multipleSelection[0].PlanNum,
          BatchSum: this.formAllotBatch.BatchSum,
          BatchDuration: this.formAllotBatch.BatchDuration,
        }
        this.$confirm('确定自动排产所选计划？', '提示', {
          distinguishCancelAndClose:true,
          type: 'warning'
        }).then(()  => {
          this.axios.post("/api/planschedul",this.qs.stringify(params)).then(res => {
            if(res.data.code === "200"){
              that.$message({
                type: 'success',
                message: res.data.message
              });
              this.getPlanManagerTableData()
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
            message: '已取消排产'
          });
        });
      },
      //获取工艺段
      getBrandProcess(){
        var that = this
        var params = {
          BatchID: this.PlanManagerTableData.multipleSelection[0].BatchID,
        }
        this.axios.get("/api/batchequimentselect",{
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
            that.processList = res.data.data.processList.sort(compare('Seq'))
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      savePlanEq(){
        var that = this
        var params = {
          BatchID: this.PlanManagerTableData.multipleSelection[0].BatchID,
          processList:JSON.stringify(this.processList)
        }
        this.axios.post("/api/addEquipmentBatchRunTime",this.qs.stringify(params)).then(res => {
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
        })
      }
    }
  }
</script>

<style scoped>

</style>
