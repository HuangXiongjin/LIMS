<template>
  <el-row>
    <el-col :span="24">
      <el-steps :active="steps" finish-status="success" align-center class="marginBottom">
        <el-step title="选择订单"></el-step>
        <el-step title="数据统计"></el-step>
        <el-step title="订单分批"></el-step>
      </el-steps>
      <el-row :gutter="15" v-show="steps == 0">
        <el-col :span="24">
          <el-collapse class="marginBottom">
            <el-collapse-item title="多条件查询订单">
              <el-form :model="planTableData.searchField" :inline="true" class="marginTop" label-width="110px">
                <el-form-item label="状态">
                   <el-select v-model="planTableData.searchField.PlanStatus" placeholder="请选择">
                    <el-option v-for="item in optionsPlanStatus" :key="item.value" :label="item.value" :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="创建/同步时间">
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
              <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="PlanStatus" label="状态">
                <template slot-scope="scope">
                  <span class="color-darkblue" v-if="scope.row.PlanStatus === '已分批'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-orange" v-if="scope.row.PlanStatus === '待分批'">{{ scope.row.PlanStatus }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="Description" label="描述"></el-table-column>
              <el-table-column prop="CreateTimeTime" label="创建/同步时间"></el-table-column>
            </el-table>
            <el-dialog :title="planTableData.dialogTitle" :visible.sync="planTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="planTableData.formField" label-width="110px">
                <el-form-item label="编号">
                  <el-input v-model="planTableData.formField.PlanNum"></el-input>
                </el-form-item>
                <el-form-item label="品名">
                  <el-select v-model="planTableData.formField.BrandCode" placeholder="请选择" @change="change">
                    <el-option v-for="item in scheduleData" :key="item.ID" :label="item.BrandName" :value="item.BrandCode">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="计划产量">
                  <el-input v-model="planTableData.formField.PlanQuantity"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                  <el-input v-model="planTableData.formField.Unit" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="描述">
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
      <el-row v-show="steps == 1">
        <el-col :span='24'>
          <div class="platformContainer">
            <p class="marginBottom text-size-20">已选中订单</p>
            <el-row v-for="(item,index) in selectPlanList" :key="index">
              <el-col :span="24">
                <el-col :span="4">
                  <p class="color-darkblue text-center text-size-18">{{ item.BrandName }}</p>
                </el-col>
                <el-col :span="4">
                  <p class="marginBottom">订单数</p>
                  <p class="marginBottom color-orange">{{ item.orderNum }}</p>
                </el-col>
                <el-col :span="4">
                  <p class="marginBottom">总需求量</p>
                  <p class="marginBottom color-success">{{ item.PlanQuantityTotal }}</p>
                </el-col>
                <el-col :span="4">
                  <p class="marginBottom">批生产能力</p>
                  <p class="marginBottom color-success">{{ item.BatchWeight }}</p>
                </el-col>
                <el-col :span="4">
                  <p class="marginBottom">单位</p>
                  <p class="marginBottom">{{ item.unit }}</p>
                </el-col>
                <el-col :span="4">
                  <p class="marginBottom">分配批数</p>
                  <p class="marginBottom color-lightgreen">{{ item.BatchNum }}</p>
                </el-col>
              </el-col>
            </el-row>
          </div>
          <div class="platformContainer">
            <p class="marginBottom text-size-20">未选中待分批的订单</p>
            <el-row v-for="(item,index) in unSelectPlanList" :key="index">
              <el-col :span="24" class="text-center">
                <el-col :span="6">
                  <p class="marginBottom">订单号</p>
                  <p class="marginBottom color-orange">{{ item.PlanNum }}</p>
                </el-col>
                <el-col :span="6">
                  <p class="marginBottom">品名</p>
                  <p class="marginBottom color-orange">{{ item.BrandName }}</p>
                </el-col>
                <el-col :span="6">
                  <p class="marginBottom">计划产量</p>
                  <p class="marginBottom color-orange">{{ item.PlanQuantity }}</p>
                </el-col>
                <el-col :span="6">
                  <p class="marginBottom">单位</p>
                  <p class="marginBottom color-orange">{{ item.Unit }}</p>
                </el-col>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15" v-if="steps == 2">
        <el-col :span="24">
          <div class="platformContainer">
            <el-row>
              <el-col :span="24">
                <p class="marginBottom">共选择<span>{{ selectPlanList.length }}</span>类品种，需生成批数<span>{{ selectPlanBatchTotal }}</span>批</p>
              </el-col>
            </el-row>
            <el-button type="primary" size="small" @click="planschedul">生成批计划</el-button>
          </div>
          <div class="platformContainer" style="min-height: 550px;">
            <el-form :inline="true">
              <el-form-item v-for="(item,index) in PlanManagerTableData.handleType" :key="index">
                <el-button :type="item.type" size="small" @click="handleFormPlanManager(item.label)">{{ item.label }}</el-button>
              </el-form-item>
              <el-form-item class="floatRight">
                <el-button type="primary" size="small" icon='el-icon-refresh-right' @click="getPlanManagerTableData">刷新</el-button>
              </el-form-item>
            </el-form>
            <el-table :data="PlanManagerTableData.data" border size="small">
              <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
              <el-table-column prop="Seq" label="顺序号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="SchedulePlanCode" label="调度编号"></el-table-column>
              <el-table-column prop="BrandCode" label="品名编码"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="BrandType" label="产品类型"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
              <el-table-column prop="Unit" label="单位"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态">
                <template slot-scope="scope">
                  <b class="color-red cursor-pointer" v-if="scope.row.PlanStatus === '审核未通过'" @click="seeDescription(scope.$index, scope.row)">{{ scope.row.PlanStatus }}</b>
                  <b class="color-orange" v-else-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-red" v-else-if="scope.row.PlanStatus === '撤回'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-lightgreen" v-else-if="scope.row.PlanStatus === '待下发'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-purple" v-else-if="scope.row.PlanStatus === '待执行'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-orange" v-else-if="scope.row.PlanStatus === '待备料'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-orange" v-else-if="scope.row.PlanStatus === '物料发送中'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-success" v-else-if="scope.row.PlanStatus === '物料发送完成'">{{ scope.row.PlanStatus }}</b>
                  <b class="color-brown" v-else-if="scope.row.PlanStatus === '已发送投料计划'">{{ scope.row.PlanStatus }}</b>
                  <b class="" v-else>{{ scope.row.PlanStatus }}</b>
                </template>
              </el-table-column>
              <el-table-column label="操作" fixed="right" width="150">
                <template slot-scope="scope">
                  <el-button size="mini" @click="handleEdit(scope.$index, scope.row)" v-if="scope.row.PlanStatus === '待审核' || scope.row.PlanStatus === '审核未通过'">编辑</el-button>
                  <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)" v-if="scope.row.PlanStatus === '待审核' || scope.row.PlanStatus === '审核未通过'">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
               :total="PlanManagerTableData.total"
               :current-page="PlanManagerTableData.offset"
               :page-sizes="[10,15,20,30,50]"
               :page-size="PlanManagerTableData.limit"
               @size-change="handlePlanManagerSizeChange"
               @current-change="handlePlanManagerCurrentChange">
              </el-pagination>
            </div>
            <el-dialog :title="PlanManagerTableData.dialogTitle" :visible.sync="PlanManagerTableData.dialogVisible" width="40%" :append-to-body="true">
              <el-form :model="PlanManagerTableData.formField" label-width="110px">
                <el-form-item label="订单编号">
                  <el-select v-model="PlanManagerTableData.formField.PlanNum" placeholder="请选择" @change="selectPlanNum" :disabled="PlanManagerTableData.dialogTitle === '编辑'">
                    <el-option v-for="(item,index) in selectPlanList" :key="index" :label="item.PlanNum" :value="item.PlanNum"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="品名">
                  <el-input v-model="PlanManagerTableData.formField.BrandName" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="批次号">
                  <el-input v-model="PlanManagerTableData.formField.BatchID"></el-input>
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
      <el-col :span="24" style="text-align: right;">
        <el-button type="primary" v-show="steps != 0" @click="lastStep">上一步</el-button>
        <el-button type="primary" v-show="steps != 2" @click="nextStep">下一步</el-button>
        <el-button type="primary" v-show="steps == 2" @click="$router.push('/planningScheduling')">去调度</el-button>
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
        optionsPlanStatus:[
          {value:"待分批"},
          {value:"已分批"},
        ],
        scheduleData:[],
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
            BrandCode:"",
            BrandName:"",
            Unit:"",
            PlanQuantity:"",
            Description:""
          },
          searchField:{
            PlanStatus:"",
            CreateTimeTime:"",
          }
        },
        selectPlanList:[],
        unSelectPlanList:[],
        selectPlanBatchTotal:0,
        PlanManagerTableData:{
          data:[],
          limit:10,
          offset:1,
          total:0,
          handleType:[
            {type:"primary",label:"添加"},
          ],
          dialogVisible:false,
          dialogTitle:"",
          handleRow:"",
          formField:{
            PlanNum:"",
            BatchID:"",
            BrandCode:"",
            BrandName:"",
          },
        },
      }
    },
    mounted(){
      this.getScheduleTableData()
      this.getPlanTableData()
    },
    methods:{
      change(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "ProductRule",
            BrandCode: this.planTableData.formField.BrandCode,
          }
        }).then(res => {
          if(res.data.code === "200"){
            this.planTableData.formField.BrandName = res.data.data.rows[0].BrandName
            this.planTableData.formField.Unit = res.data.data.rows[0].Unit
          }else{
            this.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      nextStep(){
        if(this.steps == 0){
          if(this.planTableData.multipleSelection.length > 0){
            this.steps++
            this.getselectpaichanrule()
            this.getUnSelectPlan()
          }else{
            this.$message({
              type: 'info',
              message: "请选择订单计划"
            });
          }
        }else if(this.steps == 1){
          this.steps++
          this.getPlanManagerTableData()
        }
      },
      lastStep(){
        this.steps--
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
            that.scheduleData = res.data.data.rows
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
          PlanStatus:this.planTableData.searchField.PlanStatus,
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
                this.getPlanTableData()
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
          this.planTableData.dialogVisible = false
          var params = {
            tableName:"product_plan",
            PlanNum:this.planTableData.formField.PlanNum,
            PlanQuantity:this.planTableData.formField.PlanQuantity,
            BrandName:this.planTableData.formField.BrandName,
            BrandCode:this.planTableData.formField.BrandCode,
            Unit:this.planTableData.formField.Unit,
            PlanStatus:"待分批",
            CreateTimeTime:moment().format("YYYY-MM-DD HH:mm:ss"),
          }
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
              this.getPlanTableData()
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
      //选中订单获取排产参数
      getselectpaichanrule(){
        var that = this
        var params = {
          selectPlanList:JSON.stringify(this.planTableData.multipleSelection),
        }
        this.axios.get("/api/selectpaichanrule",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            this.selectPlanList = res.data.data
            this.selectPlanBatchTotal = 0
            this.selectPlanList.forEach(item =>{
              this.selectPlanBatchTotal += Number(item.BatchNum)
            })
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      //获取未选中订单
      getUnSelectPlan(){
        this.unSelectPlanList = []
        this.planTableData.data.forEach(item => {
          if(!this.planTableData.multipleSelection.includes(item)){
            if(item.PlanStatus === "待分批"){
              this.unSelectPlanList.push(item)
            }
          }
        });
      },
      //批次计划
      getPlanManagerTableData(){
        var that = this
        var PlanNums = []
        this.selectPlanList.forEach(item =>{
          PlanNums.push(item.PlanNum)
        })
        var params = {
          PlanNums:JSON.stringify(PlanNums),
          limit:this.PlanManagerTableData.limit,
          offset:this.PlanManagerTableData.offset -1,
        }
        this.axios.get("/api/selectplanmanager",{
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
      handlePlanManagerSizeChange(limit){
        this.PlanManagerTableData.limit = limit
        this.getPlanManagerTableData()
      },
      handlePlanManagerCurrentChange(offset){
        this.PlanManagerTableData.offset = offset
        this.getPlanManagerTableData()
      },
      handleFormPlanManager(label){
        if(label === "添加"){
          this.PlanManagerTableData.dialogVisible = true
          this.PlanManagerTableData.dialogTitle = label
        }
      },
      selectPlanNum(){
        this.selectPlanList.forEach(item =>{
          if(item.PlanNum === this.PlanManagerTableData.formField.PlanNum){
            this.PlanManagerTableData.formField.BrandName = item.BrandName
            this.PlanManagerTableData.formField.BrandCode = item.BrandCode
          }
        })
      },
      handleEdit(index, row){
        this.PlanManagerTableData.dialogVisible = true
        this.PlanManagerTableData.dialogTitle = "编辑"
        this.PlanManagerTableData.handleRow = row
        this.PlanManagerTableData.formField = {
          BatchID:row.BatchID,
          PlanNum:row.PlanNum,
          BrandName:row.BrandName,
          BrandCode:row.BrandCode
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
        if(this.PlanManagerTableData.dialogTitle === "添加"){
          var params = {
            PlanNum:this.PlanManagerTableData.formField.PlanNum,
            BatchID:this.PlanManagerTableData.formField.BatchID,
            BrandCode:this.PlanManagerTableData.formField.BrandCode
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
        }else if(this.PlanManagerTableData.dialogTitle === "编辑"){
          var params = {
            ID:this.PlanManagerTableData.handleRow.ID,
            BatchID:this.PlanManagerTableData.formField.BatchID,
            PlanStatus:"待审核",
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
        var isFlag = true
        this.planTableData.multipleSelection.forEach(item =>{
          if(item.PlanStatus === "已分批"){
            isFlag = false
          }
        })
        if(isFlag){
          var params = {
            selectPlanList:JSON.stringify(this.selectPlanList),
          }
          this.$confirm('确定自动生成批计划？(将生成'+ this.selectPlanBatchTotal +'批)', '提示', {
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
        }else{
          this.$message({
            type: 'info',
            message: "只允许选择待分批计划生成"
          });
        }
      },
      seeDescription(index,row){ //查看未通过原因
        this.$alert(row.Description, '未通过原因', {
          confirmButtonText: '知道了',
          callback: action => {}
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
