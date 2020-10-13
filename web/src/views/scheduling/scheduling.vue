<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="选择订单计划"></el-step>
        <el-step title="批计划管理"></el-step>
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
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
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
                <el-form-item label="计划产量">
                  <el-input v-model="planTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="计划完成时间">
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
            <span>计划产量：{{ planTableData.multipleSelection[0].PlanQuantity }}</span>
            <el-divider direction="vertical"></el-divider>
            <span>品名：{{ BrandActive }}</span>
          </div>
          <div class="platformContainer" style="min-height: 550px;">
            <el-form :inline="true" :model="formAllotBatch">
              <el-form-item label="批数">
                <el-input v-model="formAllotBatch.BatchSum" siBatchNumze="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="planschedul">自动分批</el-button>
              </el-form-item>
            </el-form>
            <el-form :inline="true">
              <el-form-item v-for="(item,index) in PlanManagerTableData.handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleFormPlanManager(item.label)">{{ item.label }}</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="PlanManagerTableData.data" border size="small" ref="multipleTablePlanManager" @selection-change="handleSelectionChangePlanManager" @row-click="handleRowClickPlanManager">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="PlanQuantity" label="每批计划产量"></el-table-column>
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
                <el-form-item label="每批计划产量">
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
      <el-row v-show="steps == 2">
        <el-col :span='24'>
          <div class="platformContainer" style="backgroundColor:#fff;">
            <div id="main" style="width:100%; height:750px;clear:both;overflow:hidden;" v-loading="loading"></div>
          </div>
        </el-col>
      </el-row>
      <el-col :span="24" style="text-align: right;">
        <el-button type="info" v-show="steps != 0" @click="resetStep">重置</el-button>
        <el-button type="primary" v-show="steps != 0" @click="lastStep">上一步</el-button>
        <el-button type="primary" v-show="steps != 3" @click="nextStep">下一步</el-button>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  import echarts from '@/assets/js/echarts.js'
  var moment = require('moment');
  export default {
    name: "scheduling",
    components:{},
    data(){
      return{
        loading:false,
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
        },
        processList:[],
        ActivePUName:"",
        ydata:[],
        PlanStartTime:[],
        PlanEndTime:[]
      }
    },
    mounted(){
      this.getScheduleTableData()
      this.getUnit()
    },
    methods:{
      SearchPicdata(){
        var params = {
            tableName: "PlanManager",
            PlanNum:this.planTableData.multipleSelection[0].PlanNum
          }
        this.axios.get("/api/CUID",{
              params: params
            }).then(res => {
              var arr=res.data.data.rows
                this.ydata=arr.map((res) => {
                  return res.BatchID
                })
                this.PlanStartTime=arr.map((res) => {
                  return new Date(res.PlanBeginTime.replace('-', '/'))
                })
                this.PlanEndTime=arr.map((res) => {
                  return new Date(res.PlanEndTime.replace('-', '/'))
                })
                this.drawPic(this.ydata,this.PlanStartTime,this.PlanEndTime)
        })
      },
    drawPic(ydata,planstarttime,planendtime) {
            var myCharts = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '排产进度表',
                    left: 10,
                    textStyle: {
                      color: '#666'  //设置title文字颜色
                  }
                },
                legend: {
                    y: 'top',
                    data: ['计划完成时间'], //修改的地方1,
                    textStyle: {
                      color: '#666' //设置图例文字颜色
                  }
                },
                grid: {
                    containLabel: true,
                    left: 20,
                    bottom:10
                },
                xAxis: {
                    name:'时间',
                    type: 'time',
                    axisLine: { lineStyle: { color: '#666' } } //控制x轴坐标文字颜色
                },
                yAxis: {
                    name:'批次',
                    data:[...ydata],
                    axisLine: { lineStyle: { color: '#666' } }  //控制y轴坐标文字颜色
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function(params) {
                        var res = params[0].name + "</br>"
                        var date0 = params[0].data;
                        var date1 = params[1].data;
                        date0 = date0.getFullYear() + "-" + (date0.getMonth() + 1) + "-" + (date0.getDate().toString().padStart(2,0))+ "  " + (date0.getHours().toString().padStart(2,0))+':'+(date0.getMinutes().toString().padStart(2,0))+':'+(date0.getSeconds().toString().padStart(2,0));
                        date1 = date1.getFullYear() + "-" + (date1.getMonth() + 1) + "-" + (date1.getDate().toString().padStart(2,0))+ "  " + (date1.getHours().toString().padStart(2,0))+':'+(date1.getMinutes().toString().padStart(2,0))+':'+(date1.getSeconds().toString().padStart(2,0));
                        res += params[0].seriesName + "~" + params[1].seriesName + ":</br>" + date0 + "~" + date1 + "</br>"
                        return res;
                    }

                },
                series: [
                    {
                        name: '计划开始时间',
                        type: 'bar',
                        stack: 'test1',
                        itemStyle: {
                            normal: {
                                color: 'rgba(0,0,0,0)'
                            }
                        },
                        data:planstarttime,
                        barMaxWidth: 30,
                    },
                    {
                        name: '计划完成时间',
                        type: 'bar',
                        stack: 'test1',
                        //修改地方2
                        itemStyle: {
                            normal: {
                                color: '#06ACB5'
                            }
                        },
                        data:planendtime,
                        barMaxWidth:20,
                    }
                ]
            };
            myCharts.setOption(option);
        },
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
        }else if(this.steps == 2){
          this.steps++
          this.SearchPicdata()
        }else{
          this.steps++
        }
      },
      lastStep(){
        if(this.steps == 2){
          this.steps--
          this.getPlanManagerTableData()
        }else if(this.steps == 3){
          this.steps--
          this.SearchPicdata()
        }else{
          this.steps--
        }
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
      clickBrandTag(BrandName,BrandCode,BrandType){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.BrandType = BrandType
        this.getPlanTableData(this.BrandActive)
      },
      getPlanTableData(BrandName){
        var that = this
        var params = {
          tableName: "product_plan",
          BrandName:BrandName,
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
          this.axios.get("/api/makePlan",{
            params:params
          }).then(res =>{
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
    }
  }
</script>

<style scoped>
   .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border:1px solid #228AD5;
    background:#fff;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
  .pactive{
    background-color:#228AD5;
    color:#fff;
  }
</style>
