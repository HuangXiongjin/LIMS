<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="选择订单计划"></el-step>
        <el-step title="批计划管理"></el-step>
        <el-step title="甘特图"></el-step>
        <el-step title="计划清单"></el-step>
      </el-steps>
      <el-row :gutter="15" v-show="steps == 0">
        <el-col :span="24">
          <el-collapse class="marginBottom">
            <el-collapse-item title="多条件查询订单计划">
              <el-form :model="planTableData.searchField" :inline="true" label-width="110px">
                <el-form-item label="计划交付时间">
                   <el-date-picker v-model="planTableData.searchField.PlanFinishTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="计划创建时间">
                   <el-date-picker v-model="planTableData.searchField.CreateTimeTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="small" @click="getPlanTableData">查询</el-button>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>
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
              <el-table-column prop="Description" label="描述"></el-table-column>
              <el-table-column prop="CreateTimeTime" label="创建时间"></el-table-column>
            </el-table>
            <el-dialog :title="planTableData.dialogTitle" :visible.sync="planTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="planTableData.formField" label-width="110px">
                <el-form-item label="编号">
                  <el-input v-model="planTableData.formField.PlanNum"></el-input>
                </el-form-item>
                <el-form-item label="计划产量">
                  <el-input v-model="planTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="计划完成时间">
                  <el-date-picker v-model="planTableData.formField.PlanFinishTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择时间">
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
            <el-form :inline="true" :model="formAllotBatch">
              <el-form-item label="共选择订单数">
                <span>{{ planTableData.multipleSelection.length }}项</span>
              </el-form-item>
              <el-form-item label="选择订单查看参数">
                <el-select v-model="planTableData.selectMultiple" placeholder="请选择" @change="getselectpaichanrule">
                  <el-option v-for="(item,index) in planTableData.multipleSelection" :key="index" :label="item.PlanNum" :value="item.PlanNum">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
          <div class="platformContainer">
            <el-form :inline="true" :model="formAllotBatch" label-width="120px">
              <el-form-item label="计划单号">
                <el-input v-model="formAllotBatch.PlanNum" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="品名">
                <el-input v-model="formAllotBatch.BrandName" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="药品类型">
                <el-input v-model="formAllotBatch.BrandType" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="计划交付时间">
                <el-input v-model="formAllotBatch.PlanFinishTime" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="计划产量">
                <el-input v-model="formAllotBatch.PlanQuantity" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="每批产量">
                <el-input v-model="formAllotBatch.BatchWeight" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="批数">
                <el-input v-model="formAllotBatch.batchSum" size="small" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="可用生产线">
                <el-input type="textarea" v-model="formAllotBatch.AvalProductLine" size="small" :disabled="true"></el-input>
              </el-form-item>
            </el-form>
            <el-form :inline="true" :model="formAllotBatch">
              <el-form-item label="计划开始时间">
                <el-date-picker v-model="formAllotBatch.StartTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择时间">
                </el-date-picker>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="planschedul">确定生成计划</el-button>
              </el-form-item>
            </el-form>
            <p class="color-grayblack text-size-12">选择所有选择订单的计划生产时间，生成时自动根据相应参数排产，再次生成时会自动清空上次生成的计划</p>
          </div>
          <div class="platformContainer" style="min-height: 550px;">
            <el-form :inline="true">
              <el-form-item v-for="(item,index) in SchedulingTableData.handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleFormPlanManager(item.label)">{{ item.label }}</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="SchedulingTableData.data" border size="small">
              <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="PlanQuantity" label="每批计划产量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="BrandType" label="产品类型"></el-table-column>
              <el-table-column prop="PlanBeginTime" label="计划开始时间"></el-table-column>
              <el-table-column prop="PlanEndTime" label="计划完成时间"></el-table-column>
              <el-table-column prop="PLineName" label="生产线名称"></el-table-column>
              <el-table-column prop="Describtion" label="描述"></el-table-column>
              <el-table-column label="操作" fixed="right" width="150">
                <template slot-scope="scope">
                  <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                  <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-dialog :title="SchedulingTableData.dialogTitle" :visible.sync="SchedulingTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="SchedulingTableData.formField" label-width="110px">
                <el-form-item label="批次号">
                  <el-input v-model="SchedulingTableData.formField.BatchID"></el-input>
                </el-form-item>
                <el-form-item label="每批计划产量">
                  <el-input v-model="SchedulingTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                  <el-select v-model="SchedulingTableData.formField.Unit" placeholder="请选择">
                    <el-option v-for="(item,index) in unitOptions" :key="index" :label="item.UnitValue" :value="item.UnitValue">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="计划开始时间">
                  <el-date-picker v-model="SchedulingTableData.formField.PlanBeginTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="计划完成时间">
                  <el-date-picker v-model="SchedulingTableData.formField.PlanEndTime" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="SchedulingTableData.dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="savePlanManager">保 存</el-button>
              </span>
            </el-dialog>
          </div>
        </el-col>
      </el-row>
      <el-row v-show="steps == 2">
        <el-col :span='24'>
          <div class="platformContainer">
            <div id="main" style="width:100%; height:750px;clear:both;overflow:hidden;" v-loading="loading"></div>
          </div>
        </el-col>
      </el-row>
      <el-row v-show="steps == 3">
        <el-col :span='24'>
          <el-collapse class="marginBottom">
            <el-collapse-item title="多条件查询计划">
              <el-form :model="PlanTableList.searchField" :inline="true" label-width="110px">
                <el-form-item label="计划单号">
                  <el-input v-model="PlanTableList.searchField.PlanNum"></el-input>
                </el-form-item>
                <el-form-item label="批次号">
                  <el-input v-model="PlanTableList.searchField.BatchID"></el-input>
                </el-form-item>
                <el-form-item label="品名">
                  <el-input v-model="PlanTableList.searchField.BrandName"></el-input>
                </el-form-item>
                <el-form-item label="产品类型">
                  <el-input v-model="PlanTableList.searchField.BrandType"></el-input>
                </el-form-item>
                <el-form-item label="计划状态">
                  <el-input v-model="PlanTableList.searchField.PlanStatus"></el-input>
                </el-form-item>
                <el-form-item label="计划开始时间">
                   <el-date-picker v-model="PlanTableList.searchField.PlanBeginTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="计划完成时间">
                   <el-date-picker v-model="PlanTableList.searchField.PlanEndTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="small" @click="searchPlan">查询</el-button>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>
          <div class="platformContainer">
            <el-table :data="PlanTableList.data" border size="small">
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
               :total="PlanTableList.total"
               :current-page="PlanTableList.offset"
               :page-sizes="[5,10,20]"
               :page-size="PlanTableList.limit"
               @size-change="handlePlanTableListSizeChange"
               @current-change="handlePlanTableListCurrentChange">
              </el-pagination>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-col :span="24" style="text-align: right;">
        <el-button type="info" v-show="steps != 0" @click="resetStep">重新选择</el-button>
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
          multipleSelection: [],
          selectMultiple:"",
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
          searchField:{
            PlanFinishTime:"",
            CreateTimeTime:""
          }
        },
        unitOptions:[],
        SchedulingTableData:{
          data:[],
          handleType:[
            {type:"primary",label:"添加"},
          ],
          dialogVisible:false,
          dialogTitle:"",
          handleRow:"",
          formField:{
            BatchID:"",
            PlanQuantity:"",
            Unit:"",
            PlanBeginTime:"",
            PlanEndTime:"",
          },
        },
        formAllotBatch:{ //排产前参数
          PlanNum:"",
          PlanQuantity:"",
          batchSum:"",
          PlanFinishTime:"",
          BrandName:"",
          BrandType:"",
          BatchWeight:"",
          AvalProductLine:"",
          StartTime:""
        },
        processList:[],
        ActivePUName:"",
        ydata:[],
        PlanStartTime:[],
        PlanEndTime:[],
        PlanTableList:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
          searchField:{
            PlanNum:"",
            BatchID:"",
            BrandName:"",
            BrandType:"",
            PlanStatus:"",
            PlanBeginTime:"",
            PlanEndTime:"",
          },
        }
      }
    },
    mounted(){
      this.getPlanTableData()
      this.getUnit()
    },
    methods:{
      SearchPicdata(){
        var PlanNum=this.planTableData.multipleSelection[0].PlanNum
        var api="/api/CUID?tableName=PlanManager&PlanNum="+PlanNum
        this.axios.get(api).then(res => {
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
            right:40,
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
            this.getSchedulingTableData()
          }else{
            this.$message({
              type: 'info',
              message: "请选择一条ERP计划"
            });
          }
        }else if(this.steps == 1){
          this.steps++
          this.SearchPicdata()
        }else if(this.steps == 2){
          this.steps++
          this.searchPlan()
        }
      },
      lastStep(){
        if(this.steps == 2){
          this.steps--
          this.getSchedulingTableData()
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
      //获取订单计划表
      getPlanTableData(){
        var that = this
        var params = {
          tableName: "product_plan",
          PlanFinishTime:this.planTableData.searchField.PlanFinishTime,
          CreateTimeTime:this.planTableData.searchField.CreateTimeTime,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.planTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSelectionChange(row){
        this.planTableData.multipleSelection = row
      },
      handleRowClick(row){
        this.$refs.multipleTable.toggleRowSelection(row)
      },
      handleForm(label){
        if(label === "添加"){
          this.planTableData.dialogVisible = true
          this.planTableData.dialogTitle = label
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
      //获取排产参数
      getselectpaichanrule(){
        var that = this
        var params = {
          ID:this.planTableData.multipleSelection[0].ID,
        }
        this.axios.get("/api/selectpaichanrule",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.formAllotBatch = {
              PlanNum:res.data.data.PlanNum,
              PlanQuantity:res.data.data.PlanQuantity,
              BatchWeight:res.data.data.BatchWeight,
              batchSum:res.data.data.batchSum,
              PlanFinishTime:res.data.data.PlanFinishTime,
              BrandName:res.data.data.BrandName,
              BrandType:res.data.data.BrandType,
            }
            that.formAllotBatch.AvalProductLine = res.data.data.AvalProductLine.join(',')
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //批次计划
      getSchedulingTableData(){
        var that = this
        var params = {
          tableName:"Scheduling",
          PlanNum:this.planTableData.multipleSelection[0].PlanNum,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.SchedulingTableData.data = res.data.data.rows
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleFormPlanManager(label){
        if(label === "添加"){
          if(this.BrandActive){
            this.SchedulingTableData.dialogVisible = true
            this.SchedulingTableData.dialogTitle = label
          }else{
            this.$message({
              type: 'info',
              message: '请选择品名'
            });
          }
        }
      },
      handleEdit(index, row){
        this.SchedulingTableData.dialogVisible = true
        this.SchedulingTableData.dialogTitle = "编辑"
        this.SchedulingTableData.handleRow = row
        this.SchedulingTableData.formField = {
          BatchID:row.BatchID,
          PlanQuantity:row.PlanQuantity,
          Unit:row.Unit,
          PlanBeginTime:row.PlanBeginTime,
          PlanEndTime:row.PlanEndTime,
        }
      },
      handleDelete(index, row) {
        var params = {tableName:"PlanManager"}
        var mulId = [{id:row.ID}]
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
      },
      savePlanManager(){
        if(this.SchedulingTableData.dialogTitle === "添加"){
          var params = {
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            BrandType:this.BrandType,
            PlanNum:this.planTableData.multipleSelection[0].PlanNum,
            BatchID:this.SchedulingTableData.formField.BatchID,
            PlanQuantity:this.SchedulingTableData.formField.PlanQuantity,
            Unit:this.SchedulingTableData.formField.Unit,
            PlanBeginTime:this.SchedulingTableData.formField.PlanBeginTime,
            PlanEndTime:this.SchedulingTableData.formField.PlanEndTime,
          }
          this.axios.post("/api/makePlan",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.SchedulingTableData.dialogVisible = false
              this.getSchedulingTableData()
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }else if(this.SchedulingTableData.dialogTitle === "编辑"){
          var params = {
            ID:this.SchedulingTableData.handleRow.ID,
            BrandName:this.BrandActive,
            BrandCode:this.BrandCode,
            BrandType:this.BrandType,
            PlanNum:this.planTableData.multipleSelection[0].PlanNum,
            BatchID:this.SchedulingTableData.formField.BatchID,
            PlanQuantity:this.SchedulingTableData.formField.PlanQuantity,
            Unit:this.SchedulingTableData.formField.Unit,
            PlanBeginTime:this.SchedulingTableData.formField.PlanBeginTime,
            PlanEndTime:this.SchedulingTableData.formField.PlanEndTime,
          }
          this.axios.get("/api/makePlan",{
            params:params
          }).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.SchedulingTableData.dialogVisible = false
              this.getSchedulingTableData()
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
        var mulId = []
        this.planTableData.multipleSelection.forEach(item =>{
          mulId.push({id:item.ID});
        })
        var params = {
          IDs:JSON.stringify(mulId),
          StartTime:this.formAllotBatch.StartTime
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
              this.getSchedulingTableData()
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
      searchPlan(){
        var that = this
        var params = {
          tableName:"PlanManager",
          limit:this.PlanTableList.limit,
          offset:this.PlanTableList.offset - 1,
        }
        if(this.PlanTableList.searchField.PlanNum){
          params.PlanNum = this.PlanTableList.searchField.PlanNum
        }
        if(this.PlanTableList.searchField.BatchID){
          params.BatchID = this.PlanTableList.searchField.BatchID
        }
        if(this.PlanTableList.searchField.BrandName){
          params.BrandName = this.PlanTableList.searchField.BrandName
        }
        if(this.PlanTableList.searchField.BrandType){
          params.BrandType = this.PlanTableList.searchField.BrandType
        }
        if(this.PlanTableList.searchField.PlanStatus){
          params.PlanStatus = this.PlanTableList.searchField.PlanStatus
        }
        if(this.PlanTableList.searchField.PlanBeginTime){
          params.PlanBeginTime = this.PlanTableList.searchField.PlanBeginTime
        }
        if(this.PlanTableList.searchField.PlanEndTime){
          params.PlanEndTime = this.PlanTableList.searchField.PlanEndTime
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.PlanTableList.data = res.data.data.rows
            that.PlanTableList.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handlePlanTableListSizeChange(limit){ //每页条数切换
        this.PlanTableList.limit = limit
        this.searchPlan()
      },
      handlePlanTableListCurrentChange(offset) { // 页码切换
        this.PlanTableList.offset = offset
        this.searchPlan()
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
