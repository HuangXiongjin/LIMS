<template>
  <el-row>
    <el-col :span='24'>
      <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
        <el-step title="审核计划" @click.native="toStep(0)" class="cursor-pointer"></el-step>
        <el-step title="设备配置" @click.native="toStep(1)" class="cursor-pointer"></el-step>
        <el-step title="执行计划列表" @click.native="toStep(2)" class="cursor-pointer"></el-step>
      </el-steps>
       <el-row v-if='steps==0'>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">批次列表</div>
              <el-table
                  :data="batchTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable"
                  style="width: 100%">
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column label="操作" fixed="right" width='160'>
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
       <el-row v-if='steps==1'>
          <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">待配置列表</div>
              <el-table
                  :data="xfTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="xfmultipleTable"
                  @row-click="xfTabCurrentChange"
                  style="width: 100%">
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                  <el-table-column label="操作">
                    <template slot-scope="scope">
                      <el-button
                        size="mini"
                        type='primary'
                        @click="Eqconfig(scope.$index, scope.row)">生产配置</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="xfTableData.total"
                  :current-page="xfTableData.offset"
                  :page-size="xfTableData.limit"
                  @size-change="xfHandleSizeChange"
                  @current-change="xfHandleCurrentChange">
                  </el-pagination>
            </div>
            <el-dialog title="工艺段配置计划" :visible.sync="dialogTableVisible" width='95%'>
              <el-row :gutter='20'>
              <el-col :span='4'>
                  <el-steps :active="configactive" direction="vertical" finish-status="wait" space='100px'>
                    <el-step title="基础配置" @click.native="Activeconfig(0)"></el-step>
                    <el-step v-for='(item,index) in inProcessList' :key='index' :title="item.PUName" @click.native="Activeconfig(index+1)"></el-step>
                  </el-steps>
              </el-col>
              <el-col :span='20' v-if='configactive===0'>
                  <div style="fontSize:18px;fontWeight:700;">备料配置</div>
                  <el-row style="marginTop:24px;">
                    <el-col :span='10'>
                      <span class="mgr">备料</span>
                      <el-date-picker
                        v-model="value1"
                        value-format='yyyy-MM-dd'
                        type="date"
                        size='small'
                        placeholder="选择日期">
                      </el-date-picker>
                      <el-radio-group v-model="radio1" size="small">
                          <el-radio-button label="早"></el-radio-button>
                          <el-radio-button label="中"></el-radio-button>
                          <el-radio-button label="晚"></el-radio-button>
                      </el-radio-group>
                    </el-col>
                    <el-col :span='10'>
                      <span class="mgr">批量</span>
                      <el-tag type='info'>200万粒</el-tag>
                    </el-col>
                    </el-row>
                    <el-row style="marginTop:24px;">
                    <el-col :span='4'>
                      <span class="mgr">成品量</span>
                      <el-tag type='info'>2000kg</el-tag>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">取样量</span>
                      <el-tag type='info'>2000kg</el-tag>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">总料量</span>
                      <el-tag type='info'>2000kg</el-tag>
                    </el-col>
                    <el-col :span='4'>
                      <span class="mgr">得率</span>
                      <el-tag type='info'>2000kg</el-tag>
                    </el-col>
                  </el-row>
              </el-col>
              <el-col v-for='(item,index) in inProcessList' :key='index+1' :span='20'>
                <el-col v-if='configactive===index+1'>
                    <div style="fontSize:18px;fontWeight:700;">{{item.PUName}}配置</div>
                    <el-row style="marginTop:24px;">
                      <el-col :span='24' style="marginTop:18px;">
                        <el-row>
                          <el-col :span='24'  v-for="(item,index) in inProcessList[index].eqList" :key='index' class="marginBottom">
                            <el-checkbox v-model="item.isSelected"></el-checkbox>
                            <span style="margin:0 30px;">{{item.EQPCode}}</span>
                            <span style="margin:0 30px;">{{item.EQPName}}</span>
                            <el-date-picker
                              v-model="item.StartTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.StartBC" size="small">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                            <span style="margin:0 30px;">至</span>
                            <el-date-picker
                              v-model="item.EndTime"
                              value-format='yyyy-MM-dd'
                              type="date"
                              size='small'
                              placeholder="选择日期">
                            </el-date-picker>
                            <el-radio-group v-model="item.EndBC" size="small">
                              <el-radio-button label="早"></el-radio-button>
                              <el-radio-button label="中"></el-radio-button>
                              <el-radio-button label="晚"></el-radio-button>
                            </el-radio-group>
                          </el-col>
                        </el-row>
                      </el-col>
                    </el-row>
                </el-col>
              </el-col>
              </el-row>
              <span slot="footer" class="dialog-footer">
              <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveSelectedEq">确 定</el-button>
              </span>
            </el-dialog>
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
        configactive:0,
        batchTableData:{ //批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        xfTableData:{ //批次列表
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        batchmultipleSelection:[],
        xfmultipleSelection:[],
        BrandCode:'',
        BatchID:'',
        value1:'',
        radio1:'早',
        ID:0,
        dialogTableVisible:false,
        inProcessList:[],
        batchtableconfig:[{prop:'PlanBeginTime',label:"计划开始时间"},{prop:'BatchID',label:'批次号'},{prop:'BrandName',label:'品名'},{prop:'PlanQuantity',label:'计划重量'},{prop:'Unit',label:'单位'},{prop:'PlanStatus',label:'批次状态'}],//批次列表
      }
    },
    created(){
      this.getPlanManager()
    },
    mounted(){
    },
    methods:{
      saveSelectedEq(){ //保存所选设备触发
        this.dialogTableVisible = false
        var params={
          processList:JSON.stringify(this.inProcessList),
          ID:this.ID
        }
        this.axios.post('/api/addEquipmentBatchRunTime',this.qs.stringify(params)).then((res) => {
          console.log(res)
        })

      },
      getEq(BatchID,BrandCode){ //获取设备
         var params = {
                BatchID: BatchID,
                BrandCode:BrandCode
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
                this.inProcessList = res.data.data.processList.sort(compare('Seq'))
                }})
      },
      Activeconfig(index){ //配置进度条设置
          this.configactive=index
      },
      Eqconfig(){//点击设备配置
        this.dialogTableVisible=true
      },
      checkPass(index,row){
        var id=row.ID
        this.BatchID=row.BatchID
        this.BrandCode=row.BrandCode
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
              this.getPlanManager()
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
               this.getPlanManager()
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
        if(this.steps===0){
          this.getPlanManager()
        }else if(this.steps===1){
          this.getConfigbatch()
        }else if(this.steps===2){

        }else{

        }
      },
      getPlanManager(){ //获取批次列表
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit,
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
      getConfigbatch(){ //获取下发列表配置
         var params={
          tableName:'PlanManager',
          offset:this.xfTableData.offset-1,
          limit:this.xfTableData.limit,
          PlanStatus:'待下发'
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.xfTableData.data = data.rows
            this.xfTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      batchHandleSizeChange(limit){ //批次计划 每页条数切换
        this.batchTableData.limit = limit
        this.getPlanManager()
      },
       batchHandleCurrentChange(offset) { //批次计划 页码切换
        this.batchTableData.offset = offset
        this.getPlanManager()
      },
       xfTabCurrentChange(e){ //下发批次计划 点击显示当前的tab行显示详细信息
        this.getEq(e.BatchID,e.BrandCode)
        this.ID=e.ID
        this.$refs.xfmultipleTable.clearSelection();
        this.$refs.xfmultipleTable.toggleRowSelection(e)
      },
      xfHandleSizeChange(limit){ //下发批次计划 每页条数切换
        this.xfTableData.limit = limit
        this.getConfigbatch()
      },
       xfHandleCurrentChange(offset) { //下发批次计划 页码切换
        this.xfTableData.offset = offset
        this.getConfigbatch()
      }
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
  .mgr{
    font-size:16px;
    font-weight:700;
    margin-right:15px;
  }
</style>
