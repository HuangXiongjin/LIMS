<template>
  <el-row>
    <el-col :span='24'>
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="新增计划" @click.native="toStep(0)"></el-step>
        <el-step title="审核计划" @click.native="toStep(1)"></el-step>
        <el-step title="下发计划" @click.native="toStep(2)"></el-step>
        <el-step title="设备选择" @click.native="toStep(3)"></el-step>
      </el-steps>
      <el-row v-if='steps==0'>
        <el-col :span='22' class="platformContainer scheduleForm">
          <el-form :inline="true" :model="scheduleform" class="demo-form-inline" label-width='120px'>
            <el-form-item label="制定计划日期">
              <el-date-picker type="date" placeholder="选择日期" v-model="scheduleform.PlanBeginTime" style="width: 200px;"></el-date-picker>
            </el-form-item>
            <el-form-item label="批次号">
               <el-input v-model="scheduleform.BatchID" placeholder="批次号"></el-input>
            </el-form-item>
            <el-form-item label="品名">
              <el-input v-model="scheduleform.BrandName" placeholder="品名"></el-input>
            </el-form-item>
            <el-form-item label="计划重量">
               <el-input v-model="scheduleform.PlanQuantity" placeholder="计划重量"></el-input>
            </el-form-item>
            <el-form-item label="生产线">
              <el-input v-model="scheduleform.PLineName" placeholder="生产线"></el-input>
            </el-form-item>
            <el-form-item label="单位">
              <el-input v-model="scheduleform.Unit" placeholder="单位"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveScheduling" style="marginLeft:40px;">保存</el-button>
            </el-form-item>
          </el-form>
          
        </el-col>
        <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">排产列表</div>
              <el-table
                  :data="planTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="multipleTable"
                  @selection-change="handleSelectionChange" 
                  @row-click="TabCurrentChange"
                  style="width: 100%">
                  <el-table-column type="selection"></el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="planTableData.total"
                  :current-page="planTableData.offset"
                  :page-size="planTableData.limit"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
      </el-row>
       <el-row v-if='steps==1'>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">批次列表</div>
              <el-table
                  :data="batchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable"
                  @selection-change="batchHandleSelectionChange" 
                  @row-click="batchTabCurrentChange"
                  style="width: 100%">
                  <el-table-column type="selection"></el-table-column>
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='success'
                        @click="checkPass(scope.$index, scope.row)">通过</el-button>
                      <el-button
                        size="mini"
                        type="primary"
                        @click="checkNopass(scope.$index, scope.row)">不通过</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="batchTableData.total"
                  :current-page="batchTableData.offset"
                  :page-size="batchTableData.limit"
                  @size-change="batchHandleSizeChange"
                  @current-change="batchHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
       </el-row>
    </el-col>
  </el-row>
</template>

<script>
var moment=require('moment')
  export default {
    name: "planningScheduling",
    data(){
      return {
        steps:0,
        scheduleform:{
          PlanBeginTime:'',
          BatchID:'',
          BrandName:'',
          PlanQuantity:'',
          PLineName:'',
          Unit:''
        },
        planTableData:{ //排产列表
            tableName:"Scheduling",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        batchTableData:{ //批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        multipleSelection:[],
        batchmultipleSelection:[],
        tableconfig:[{prop:'PlanBeginTime',label:"计划开始时间"},{prop:'BatchID',label:'批次号'},{prop:'BrandName',label:'品名'},{prop:'PlanQuantity',label:'计划重量'},{prop:'PLineName',label:'生产线名称'},{prop:'Unit',label:'单位'}],//排产列表
        batchtableconfig:[{prop:'PlanBeginTime',label:"计划开始时间"},{prop:'BatchID',label:'批次号'},{prop:'BrandName',label:'品名'},{prop:'PlanQuantity',label:'计划重量'},{prop:'PLineName',label:'生产线名称'},{prop:'Unit',label:'单位'}],//批次列表
      }
    },
    created(){
      this.getBatchTable()
    },
    mounted(){
    },
    methods:{
      checkPass(index,row){
        var id=row.ID
        this.$confirm('此操作将审核通过此批次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
           var params={
            PlanStatus:'待下发',
            Describtion:'',
            ID:id
          }
          this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: '审核成功'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      },
      checkNopass(index,row){
        var id=row.ID
        this.$prompt('请输入未通过的原因', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType:'text',
        }).then(({ value }) => {
          var params={
            PlanStatus:'审核未通过',
            Describtion:value,
            ID:id
          }
          this.axios.post('/api/checkPlanManager',this.qs.stringify(params)).then((res) => {
            if(res.data.code==='200'){
               this.$message({
                type: 'success',
                message: '提交成功'
              });
            }else{
                this.$message({
                type: 'error',
                message: '提交失败，请重试'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });       
        });
      },
      toStep(index){
        this.steps=index
        if(this.steps===1){
          this.getPlanManager()
        }
      },
      getPlanManager(){ //获取批次列表
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit,
          // PlanStatus:'待下发'
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.batchTableData.data = data.rows
            this.batchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      saveScheduling(){ //保存修改的scheduling表
        var params={
          tableName:"PlanManager",
        }
      for(var key in this.scheduleform){
        params[key]=this.scheduleform[key]
      }
      this.axios.post("/api/CUID",this.qs.stringify(params)).then((res) => {
        if(res.data.code==='200'){
          this.$message({
            type:'success',
            message:res.data.message
          })
        }else{
          this.$message({
            type:'error',
            message:'保存失败'
          })
        }
      })
      },
      getBatchTable(){ //初始化获取排产批次表
        var params={
          tableName:"Scheduling",
          offset:this.planTableData.offset - 1,
          limit:this.planTableData.limit
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
          if(res.data.code === "200"){
            var data = res.data.data
            this.planTableData.data = data.rows
            this.planTableData.total = data.total
          }
        },err=>{
           console.log("请求错误")
        })
      },
      handleSelectionChange(row){
        this.multipleSelection = row
      },
      batchHandleSelectionChange(row){
        this.batchmultipleSelection = row
      },
      TabCurrentChange(e){ //排产 点击显示当前的tab行显示详细信息
        this.scheduleform={
              PlanBeginTime:e.PlanBeginTime,
              BatchID:e.BatchID,
              BrandName:e.BrandName,
              PlanQuantity:e.PlanQuantity,
              PLineName:e.PLineName,
              Unit:e.Unit
        }
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(e)
      },
      handleSizeChange(limit){ //排产 每页条数切换
        this.planTableData.limit = limit
        this.getBatchTable()
      },
       handleCurrentChange(offset) { //排产 页码切换
        this.planTableData.offset = offset
        this.getBatchTable()
      },
       batchTabCurrentChange(e){ //批次计划 点击显示当前的tab行显示详细信息
        this.$refs.batchmultipleTable.clearSelection();
        this.$refs.batchmultipleTable.toggleRowSelection(e)
      },
      batchHandleSizeChange(limit){ //批次计划 每页条数切换
        this.batchTableData.limit = limit
        this.getPlanManager()
      },
       batchHandleCurrentChange(offset) { //批次计划 页码切换
        this.batchTableData.offset = offset
        this.getPlanManager()
      }
    }
  }
</script>

<style scoped>

</style>
