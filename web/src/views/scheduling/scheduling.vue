<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="选择ERP计划"></el-step>
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
          <div class="platformContainer" style="min-height: 550px;">
            <p class="marginBottom" v-if="BrandActive">当前选择的是{{ BrandActive }}</p>
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
              <el-table-column prop="FinishTime" label="计划交付时间"></el-table-column>
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
                <el-form-item label="计划成品重量">
                  <el-input v-model="planTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="计划时长">
                  <el-input v-model="planTableData.formField.PlanTimeLen"></el-input>
                </el-form-item>
                <el-form-item label="计划交付时间">
                  <el-date-picker v-model="planTableData.formField.FinishTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期">
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
            <span>品名：{{ BrandActive }}</span>
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
              <el-table-column prop="PlanQuantity" label="计划成品重量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="BrandType" label="产品类型"></el-table-column>
              <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
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
                <el-form-item label="计划产量">
                  <el-input v-model="PlanManagerTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                  <el-select v-model="PlanManagerTableData.formField.Unit" placeholder="请选择">
                    <el-option v-for="(item,index) in unitOptions" :key="index" :label="item.UnitValue" :value="item.UnitValue">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="计划生产日期">
                  <el-date-picker v-model="PlanManagerTableData.formField.PlanDate" value-format="yyyy-MM-dd" type="date" placeholder="选择日期">
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
              <el-col :span="6" v-for="(item,index) in processList" :key="index">
                <div class="marginBottom text-size-20">{{ item.PUName }}</div>
                <el-popover
                  placement="right"
                  width="360"
                  trigger="click">
                  <el-checkbox v-for="eq in item.eqList" v-model="eq.isSelected" :key="eq.EQPCode" class="marginBottom-10">
                    {{ eq.EQPName }}-<span class="color-success" v-if="eq.EQPStatus === 'True'">可用</span><span class="color-orange" v-if="eq.EQPStatus === 'False'">等待</span>
                  </el-checkbox>
                  <el-button slot="reference" size="small">选择设备</el-button>
                </el-popover>
                <el-button type="primary" size="small">自动分配</el-button>
                <p class="marginTop marginBottom-10 text-size-16">已分配设备</p>
                <p class="marginBottom-10" v-for="eq in item.eqList" :key="eq.EQPCode" v-if="eq.isSelected">{{ eq.EQPName }}</p>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <el-col :span="24" style="text-align: right;">
        <el-button type="info" v-if="steps != 0" @click="resetStep">重置</el-button>
        <el-button type="info" v-if="steps == 2">保存</el-button>
        <el-button type="primary" @click="nextStep">下一步</el-button>
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
            FinishTime:"",
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
            {type:"danger",label:"删除"},
          ],
          dialogVisible:false,
          dialogTitle:"",
          formField:{
            BatchID:"",
            PlanQuantity:"",
            Unit:"",
            PlanDate:""
          },
        },
        processList:[],
      }
    },
    mounted(){
      this.getScheduleTableData()
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
        }else if(this.steps == 2){

        }
      },
      resetStep(){
        this.steps = 0
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
            FinishTime:this.planTableData.formField.FinishTime,
            Description:this.planTableData.formField.Description,
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
          tableName: "PlanManager",
          field:"PlanNum",
          fieldvalue:this.planTableData.multipleSelection[0].PlanNum,
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
            PlanDate:this.PlanManagerTableData.formField.PlanDate
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
        }
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
            console.log(that.processList)
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      changeEqCheckbox(val){
        console.log(val)
      }
    }
  }
</script>

<style scoped>

</style>
